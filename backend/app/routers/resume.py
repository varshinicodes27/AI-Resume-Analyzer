from pydantic import BaseModel

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from sqlalchemy.orm import Session

import json
import os
import uuid


# ======================================================
# DATABASE
# ======================================================

from app.database.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.ats_analysis import ATSAnalysis


# ======================================================
# AUTH
# ======================================================

from app.dependencies.auth import get_current_user


# ======================================================
# AI
# ======================================================

from app.ai.ats_engine import calculate_section_scores

from app.ai.job_matcher import (
    extract_jd_skills,
    calculate_job_match
)

from app.utils.pdf_reader import extract_text_from_pdf

from app.ai.ai_resume_parser import parse_resume_with_ai


# ======================================================
# ROUTER
# ======================================================

router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"]
)


# ======================================================
# REQUEST SCHEMA
# ======================================================

class JobDescriptionRequest(BaseModel):

    job_description: str


# ======================================================
# UPLOAD CONFIGURATION
# ======================================================

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# Maximum resume size: 5 MB

MAX_FILE_SIZE = 5 * 1024 * 1024


# ======================================================
# RESUME UPLOAD & ANALYSIS
# ======================================================

@router.post("/upload")
async def upload_resume(

    file: UploadFile = File(...),

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    # --------------------------------------------------
    # 1. Validate file
    # --------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file was selected."
        )

    # Only PDF files

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF resume files are supported."
        )

    # --------------------------------------------------
    # 2. Read file safely
    # --------------------------------------------------

    try:

        file_content = await file.read()

        if not file_content:

            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty."
            )

        if len(file_content) > MAX_FILE_SIZE:

            raise HTTPException(
                status_code=413,
                detail=(
                    "Resume file is too large. "
                    "Maximum allowed size is 5 MB."
                )
            )

    except HTTPException:

        raise

    except Exception as e:

        print(
            "File reading error:",
            e
        )

        raise HTTPException(
            status_code=400,
            detail="Unable to read the uploaded file."
        )

    # --------------------------------------------------
    # 3. Create safe unique filename
    # --------------------------------------------------

    safe_filename = (
        f"{uuid.uuid4().hex}_resume.pdf"
    )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        safe_filename
    )

    # --------------------------------------------------
    # 4. Save temporary uploaded PDF
    # --------------------------------------------------

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(
                file_content
            )

    except Exception as e:

        print(
            "File save error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to save the uploaded resume."
        )

    # --------------------------------------------------
    # Everything below this point needs cleanup
    # --------------------------------------------------

    try:

        # ==================================================
        # 5. Extract PDF text
        # ==================================================

        try:

            extracted_text = extract_text_from_pdf(
                file_path
            )

        except Exception as e:

            print(
                "PDF extraction error:",
                e
            )

            raise HTTPException(
                status_code=422,
                detail=(
                    "Unable to read this PDF. "
                    "Please upload a valid resume PDF."
                )
            )

        # ==================================================
        # 6. Validate extracted text
        # ==================================================

        if (
            not extracted_text
            or not extracted_text.strip()
        ):

            raise HTTPException(
                status_code=422,
                detail=(
                    "No readable text was found in the PDF. "
                    "Please upload a text-based resume."
                )
            )

        # Prevent extremely tiny documents

        if len(extracted_text.strip()) < 50:

            raise HTTPException(
                status_code=422,
                detail=(
                    "The uploaded resume contains too little "
                    "readable text to analyze."
                )
            )

        # ==================================================
        # 7. SAVE RESUME IN DATABASE
        # ==================================================

        try:

            resume = Resume(
                user_id=current_user.id,
                file_name=file.filename,
                file_path=file_path,
                extracted_text=extracted_text
            )

            db.add(
                resume
            )

            db.commit()

            db.refresh(
                resume
            )

            print(
                "Resume saved successfully."
            )

            print(
                "Resume ID:",
                resume.id
            )

            print(
                "User ID:",
                current_user.id
            )

        except Exception as e:

            db.rollback()

            print(
                "Resume database error:",
                e
            )

            raise HTTPException(
                status_code=500,
                detail="Unable to save resume information."
            )

        # ==================================================
        # 8. AI RESUME PARSING
        # ==================================================

        try:

            parsed_data = parse_resume_with_ai(
                extracted_text
            )

        except Exception as e:

            print(
                "AI parsing error:",
                e
            )

            raise HTTPException(
                status_code=502,
                detail=(
                    "Resume analysis service is temporarily "
                    "unavailable. Please try again."
                )
            )

        # ==================================================
        # 9. Validate AI response
        # ==================================================

        if not isinstance(
            parsed_data,
            dict
        ):

            raise HTTPException(
                status_code=502,
                detail=(
                    "AI returned an invalid "
                    "resume analysis response."
                )
            )

        # ==================================================
        # 10. Get parsed sections safely
        # ==================================================

        candidate = parsed_data.get(
            "candidate",
            {}
        )

        education = parsed_data.get(
            "education",
            []
        )

        projects = parsed_data.get(
            "projects",
            []
        )

        skills = parsed_data.get(
            "skills",
            []
        )

        experience = parsed_data.get(
            "experience",
            []
        )

        certifications = parsed_data.get(
            "certifications",
            []
        )

        # --------------------------------------------------
        # Make sure arrays are actually arrays
        # --------------------------------------------------

        education = (
            education
            if isinstance(
                education,
                list
            )
            else []
        )

        projects = (
            projects
            if isinstance(
                projects,
                list
            )
            else []
        )

        skills = (
            skills
            if isinstance(
                skills,
                list
            )
            else []
        )

        experience = (
            experience
            if isinstance(
                experience,
                list
            )
            else []
        )

        certifications = (
            certifications
            if isinstance(
                certifications,
                list
            )
            else []
        )

        # ==================================================
        # 11. Calculate ATS report
        # ==================================================

        try:

            ats_report = calculate_section_scores(
                parsed_data
            )

        except Exception as e:

            print(
                "ATS calculation error:",
                e
            )

            raise HTTPException(
                status_code=500,
                detail="Unable to calculate the ATS score."
            )

        # ==================================================
        # 13. SAVE ATS ANALYSIS IN DATABASE
        # ==================================================

        try:

            # Get overall ATS score safely

            overall_score = float(
                ats_report.get(
                    "overall_score",
                    0
                )
            )

            # Get section scores

            section_scores = (
                ats_report.get(
                    "section_scores",
                    {}
                )
            )

            # Convert section scores dictionary
            # into JSON text for MySQL

            section_scores_json = json.dumps(
                section_scores
            )

            ats_analysis = ATSAnalysis(
                resume_id=resume.id,
                ats_score=overall_score,
                section_scores=section_scores_json
            )

            db.add(
                ats_analysis
            )

            db.commit()

            db.refresh(
                ats_analysis
            )

            print(
                "ATS analysis saved successfully."
            )

            print(
                "ATS Analysis ID:",
                ats_analysis.id
            )

            print(
                "ATS Score:",
                overall_score
            )

        except Exception as e:

            db.rollback()

            print(
                "ATS analysis database error:",
                e
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "Unable to save ATS analysis."
                )
            )

        # ==================================================
        # 14. RETURN COMPLETE ANALYSIS
        # ==================================================

        return {

            "message":
                "Resume analyzed successfully",

            "resume_id":
                resume.id,

            "ats_analysis_id":
                ats_analysis.id,

            "filename":
                file.filename,

            "candidate":
                candidate,

            "education":
                education,

            "projects":
                projects,

            "experience":
                experience,

            "certifications":
                certifications,

            "skills":
                skills,

            "ats_report":
                ats_report
        }

    finally:

        # ==================================================
        # 15. Cleanup temporary PDF
        # ==================================================

        try:

            if os.path.exists(
                file_path
            ):

                os.remove(
                    file_path
                )

                print(
                    "Temporary PDF deleted."
                )

        except Exception as e:

            print(
                "Temporary file cleanup failed:",
                e
            )

# ======================================================
# RESUME HISTORY
# ======================================================

@router.get("/history")
def get_resume_history(

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    try:

        resumes = (
            db.query(Resume)
            .filter(
                Resume.user_id == current_user.id
            )
            .order_by(
                Resume.uploaded_at.desc()
            )
            .all()
        )

        history = []

        for resume in resumes:

            # Get ATS analysis
            analysis = (
                db.query(ATSAnalysis)
                .filter(
                    ATSAnalysis.resume_id == resume.id
                )
                .first()
            )

            ats_score = (
                analysis.ats_score
                if analysis
                else None
            )

            history.append({

                "resume_id":
                    resume.id,

                "file_name":
                    resume.file_name,

                "uploaded_at":
                    (
                        resume.uploaded_at.isoformat()
                        if resume.uploaded_at
                        else None
                    ),

                "ats_score":
                    ats_score
            })

        return {

            "message":
                "Resume history retrieved successfully",

            "resumes":
                history
        }

    except Exception as e:

        print(
            "Resume history error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to retrieve resume history."
            )
        )

# ======================================================
# RESUME DETAILS
# ======================================================

@router.get("/{resume_id}")
def get_resume_details(

    resume_id: int,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    try:

        resume = (
            db.query(Resume)
            .filter(
                Resume.id == resume_id,
                Resume.user_id
                == current_user.id
            )
            .first()
        )

        # Resume doesn't exist OR
        # doesn't belong to current user

        if not resume:

            raise HTTPException(
                status_code=404,
                detail="Resume not found."
            )

        return {

            "message":
                "Resume details retrieved successfully",

            "resume": {

                "resume_id":
                    resume.id,

                "user_id":
                    resume.user_id,

                "file_name":
                    resume.file_name,

                "file_path":
                    resume.file_path,

                "uploaded_at":
                    (
                        resume.uploaded_at.isoformat()
                        if resume.uploaded_at
                        else None
                    ),

                "extracted_text":
                    resume.extracted_text
            }
        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            "Resume details error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to retrieve resume details."
            )
        )


# ======================================================
# ATS ANALYSIS DETAILS
# ======================================================

@router.get("/{resume_id}/analysis")
def get_resume_analysis(

    resume_id: int,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    try:

        # --------------------------------------------------
        # Find resume belonging to logged-in user
        # --------------------------------------------------

        resume = (
            db.query(Resume)
            .filter(
                Resume.id == resume_id,
                Resume.user_id
                == current_user.id
            )
            .first()
        )

        if not resume:

            raise HTTPException(
                status_code=404,
                detail="Resume not found."
            )

        # --------------------------------------------------
        # Find ATS analysis
        # --------------------------------------------------

        analysis = (
            db.query(ATSAnalysis)
            .filter(
                ATSAnalysis.resume_id
                == resume.id
            )
            .first()
        )

        if not analysis:

            raise HTTPException(
                status_code=404,
                detail=(
                    "ATS analysis not found "
                    "for this resume."
                )
            )

        # --------------------------------------------------
        # Convert section scores JSON
        # back to dictionary
        # --------------------------------------------------

        try:

            section_scores = (
                json.loads(
                    analysis.section_scores
                )
                if analysis.section_scores
                else {}
            )

        except Exception:

            section_scores = {}

        # --------------------------------------------------
        # Return analysis
        # --------------------------------------------------

        return {

            "message":
                "ATS analysis retrieved successfully",

            "resume_id":
                resume.id,

            "file_name":
                resume.file_name,

            "ats_analysis": {

                "analysis_id":
                    analysis.id,

                "ats_score":
                    analysis.ats_score,

                "section_scores":
                    section_scores,

                "created_at":
                    (
                        analysis.created_at.isoformat()
                        if analysis.created_at
                        else None
                    )
            }
        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            "ATS analysis retrieval error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to retrieve ATS analysis."
            )
        )


# ======================================================
# JOB MATCHING
# ======================================================

@router.post("/job_match")
def match_resume(

    request: JobDescriptionRequest,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    # --------------------------------------------------
    # 1. Validate job description
    # --------------------------------------------------

    if not request.job_description:

        raise HTTPException(
            status_code=400,
            detail=(
                "Please provide a job description."
            )
        )

    job_description = (
        request.job_description.strip()
    )

    if len(job_description) < 20:

        raise HTTPException(
            status_code=400,
            detail=(
                "Job description is too short. "
                "Please provide a complete job description."
            )
        )

    # --------------------------------------------------
    # 2. Extract JD skills
    # --------------------------------------------------

    try:

        jd_skills = extract_jd_skills(
            job_description
        )

    except Exception as e:

        print(
            "Job description skill extraction error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to analyze the job description."
            )
        )

    # --------------------------------------------------
    # 3. Get current user's latest analyzed resume skills from DB
    # --------------------------------------------------

    try:

        latest_resume = (
            db.query(Resume)
            .join(ATSAnalysis, Resume.id == ATSAnalysis.resume_id)
            .filter(
                Resume.user_id == current_user.id
            )
            .order_by(
                Resume.uploaded_at.desc()
            )
            .first()
        )

        if not latest_resume or not latest_resume.ats_analysis:

            raise HTTPException(
                status_code=400,
                detail=(
                    "No analyzed resume was found. "
                    "Please upload and analyze your "
                    "resume first."
                )
            )

        analysis_data = (
            json.loads(
                latest_resume.ats_analysis.section_scores
            )
            if latest_resume.ats_analysis.section_scores
            else {}
        )

        resume_skills = (
            analysis_data.get("skills", {}).get("skills_list", [])
        )

        if not resume_skills and "skills" in analysis_data and isinstance(analysis_data["skills"], list):
            resume_skills = analysis_data["skills"]

    except HTTPException:

        raise

    except Exception as e:

        print(
            "Resume skill retrieval error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to retrieve your resume skills."
            )
        )

    # --------------------------------------------------
    # 4. Make sure resume exists
    # --------------------------------------------------

    if not resume_skills:

        raise HTTPException(
            status_code=400,
            detail=(
                "No analyzed resume was found. "
                "Please upload and analyze your "
                "resume first."
            )
        )

    # --------------------------------------------------
    # 5. Make sure JD contains recognizable skills
    # --------------------------------------------------

    if not jd_skills:

        raise HTTPException(
            status_code=400,
            detail=(
                "No recognizable technical skills "
                "were found in the job description."
            )
        )

    # --------------------------------------------------
    # 6. Debug information
    # --------------------------------------------------

    print(
        "Current User ID:",
        current_user.id
    )

    print(
        "JD Skills:",
        jd_skills
    )

    print(
        "Resume Skills:",
        resume_skills
    )

    # --------------------------------------------------
    # 7. Calculate job match
    # --------------------------------------------------

    try:

        result = calculate_job_match(
            resume_skills,
            jd_skills
        )

    except Exception as e:

        print(
            "Job matching calculation error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to calculate the job match."
            )
        )

    # --------------------------------------------------
    # 8. Add metadata
    # --------------------------------------------------

    result["user_id"] = current_user.id

    result["job_description_skills"] = sorted(
        jd_skills
    )

    # --------------------------------------------------
    # 9. Return result
    # --------------------------------------------------

    return result