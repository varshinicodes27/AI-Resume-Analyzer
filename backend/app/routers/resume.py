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
# AI / RESUME ANALYSIS
# ======================================================

from app.ai.ats_engine import calculate_section_scores

from app.ai.job_matcher import (
    extract_jd_skills,
    calculate_job_match
)

from app.ai.ai_resume_parser import parse_resume_with_ai


# ======================================================
# PDF
# ======================================================

from app.utils.pdf_reader import extract_text_from_pdf


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
    # 1. Validate uploaded file
    # --------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was selected."
        )

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
            repr(e)
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
    # 4. Save temporary PDF
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
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to save the uploaded resume."
        )

    # --------------------------------------------------
    # Everything below requires cleanup
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
                repr(e)
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

        if len(extracted_text.strip()) < 50:

            raise HTTPException(
                status_code=422,
                detail=(
                    "The uploaded resume contains too little "
                    "readable text to analyze."
                )
            )

        # ==================================================
        # 7. SAVE RESUME
        # ==================================================

        try:

            resume = Resume(
                user_id=current_user.id,
                file_name=file.filename,
                file_path=file_path,
                extracted_text=extracted_text
            )

            db.add(resume)
            db.commit()
            db.refresh(resume)

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
                repr(e)
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
                repr(e)
            )

            raise HTTPException(
                status_code=502,
                detail=(
                    "Resume analysis service is temporarily "
                    "unavailable. Please try again."
                )
            )

        # ==================================================
        # 9. VALIDATE AI RESPONSE
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
        # 10. GET PARSED SECTIONS
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
        # Ensure correct data types
        # --------------------------------------------------

        candidate = (
            candidate
            if isinstance(candidate, dict)
            else {}
        )

        education = (
            education
            if isinstance(education, list)
            else []
        )

        projects = (
            projects
            if isinstance(projects, list)
            else []
        )

        skills = (
            skills
            if isinstance(skills, list)
            else []
        )

        experience = (
            experience
            if isinstance(experience, list)
            else []
        )

        certifications = (
            certifications
            if isinstance(certifications, list)
            else []
        )

        # ==================================================
        # 11. CALCULATE ATS REPORT
        # ==================================================

        try:

            ats_report = calculate_section_scores(
                parsed_data
            )

        except Exception as e:

            print(
                "ATS calculation error:",
                repr(e)
            )

            raise HTTPException(
                status_code=500,
                detail="Unable to calculate the ATS score."
            )

        # ==================================================
        # 12. SAVE ATS ANALYSIS
        # ==================================================

        try:

            overall_score = float(
                ats_report.get(
                    "overall_score",
                    0
                )
            )

            section_scores = ats_report.get(
                "section_scores",
                {}
            )

            if not isinstance(
                section_scores,
                dict
            ):

                section_scores = {}

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
                repr(e)
            )

            raise HTTPException(
                status_code=500,
                detail="Unable to save ATS analysis."
            )

        # ==================================================
        # 13. RETURN COMPLETE ANALYSIS
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
        # 14. CLEANUP TEMPORARY PDF
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
                repr(e)
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
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve resume history."
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
                Resume.user_id == current_user.id
            )
            .first()
        )

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
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve resume details."
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
        # Find user's resume
        # --------------------------------------------------

        resume = (
            db.query(Resume)
            .filter(
                Resume.id == resume_id,
                Resume.user_id == current_user.id
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
                ATSAnalysis.resume_id == resume.id
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
        # Convert JSON safely
        # --------------------------------------------------

        try:

            section_scores = (
                json.loads(
                    analysis.section_scores
                )
                if analysis.section_scores
                else {}
            )

        except (
            json.JSONDecodeError,
            TypeError
        ):

            section_scores = {}

        if not isinstance(
            section_scores,
            dict
        ):

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
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve ATS analysis."
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
            detail="Please provide a job description."
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

        print(
            "JD Skills:",
            jd_skills
        )

    except Exception as e:

        print(
            "Job description skill extraction error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to analyze the job description."
        )

    # --------------------------------------------------
    # 3. Get latest analyzed resume
    # --------------------------------------------------

    try:

        latest_resume = (
            db.query(Resume)
            .join(
                ATSAnalysis,
                Resume.id == ATSAnalysis.resume_id
            )
            .filter(
                Resume.user_id == current_user.id
            )
            .order_by(
                Resume.uploaded_at.desc()
            )
            .first()
        )

        if not latest_resume:

            raise HTTPException(
                status_code=400,
                detail=(
                    "No analyzed resume was found. "
                    "Please upload and analyze your "
                    "resume first."
                )
            )

        # --------------------------------------------------
        # Get ATS analysis
        # --------------------------------------------------

        analysis = (
            db.query(ATSAnalysis)
            .filter(
                ATSAnalysis.resume_id == latest_resume.id
            )
            .first()
        )

        if not analysis:

            raise HTTPException(
                status_code=400,
                detail=(
                    "No ATS analysis was found for "
                    "your latest resume."
                )
            )

        # --------------------------------------------------
        # Read stored section scores
        # --------------------------------------------------

        try:

            analysis_data = (
                json.loads(
                    analysis.section_scores
                )
                if analysis.section_scores
                else {}
            )

        except (
            json.JSONDecodeError,
            TypeError
        ):

            raise HTTPException(
                status_code=500,
                detail=(
                    "Stored resume analysis data is invalid. "
                    "Please upload and analyze your resume again."
                )
            )

        if not isinstance(
            analysis_data,
            dict
        ):

            analysis_data = {}

        # --------------------------------------------------
        # Extract skills from ATS analysis
        # --------------------------------------------------

        skills_section = analysis_data.get(
            "skills",
            {}
        )

        if isinstance(
            skills_section,
            dict
        ):

            resume_skills = skills_section.get(
                "skills_list",
                []
            )

        elif isinstance(
            skills_section,
            list
        ):

            resume_skills = skills_section

        else:

            resume_skills = []

        # --------------------------------------------------
        # Normalize resume skills
        # --------------------------------------------------

        if not isinstance(
            resume_skills,
            list
        ):

            resume_skills = []

        resume_skills = [
            str(skill).strip()
            for skill in resume_skills
            if str(skill).strip()
        ]

        print(
            "Current User ID:",
            current_user.id
        )

        print(
            "Latest Resume ID:",
            latest_resume.id
        )

        print(
            "Resume Skills:",
            resume_skills
        )

    except HTTPException:
        raise

    except Exception as e:

        print(
            "Resume skill retrieval error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve your resume skills."
        )

    # --------------------------------------------------
    # 4. Validate resume skills
    # --------------------------------------------------

    if not resume_skills:

        raise HTTPException(
            status_code=400,
            detail=(
                "No skills were found in your analyzed resume. "
                "Please upload and analyze your resume again."
            )
        )

    # --------------------------------------------------
    # 5. Validate JD skills
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
    # 6. Calculate job match
    # --------------------------------------------------

    try:

        result = calculate_job_match(
            resume_skills,
            jd_skills
        )

    except Exception as e:

        print(
            "Job matching calculation error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to calculate the job match."
        )

    # --------------------------------------------------
    # 7. Add metadata
    # --------------------------------------------------

    result["user_id"] = current_user.id

    result["resume_id"] = latest_resume.id

    result["job_description_skills"] = sorted(
        jd_skills
    )

    # --------------------------------------------------
    # 8. Return result
    # --------------------------------------------------

    return result

