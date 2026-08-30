from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.resume import router as resume_router
from app.database.database import Base, engine
from app.models.user import User
from app.models.resume import Resume
from app.models.ats_analysis import ATSAnalysis


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="ResumeIQ API",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",

    # Vercel deployments
    "https://ai-resume-analyzer-zeta-mocha.vercel.app",
    "https://ai-resume-analyzer-kvoyna1dl-resume-iq2.vercel.app",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth_router)
app.include_router(resume_router)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to ResumeIQ 🚀"
    }