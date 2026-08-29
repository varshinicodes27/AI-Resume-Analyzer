from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.database.database import Base, engine
from app.models.user import User
from app.models.resume import Resume
from app.models.ats_analysis import ATSAnalysis
from app.routers.resume import router as resume_router


# Create all tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ResumeIQ API",
    version="1.0.0"
)


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(auth_router)
app.include_router(resume_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to ResumeIQ 🚀"
    }