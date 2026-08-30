from sqlalchemy import (
    Column,
    Integer,
    Float,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database.database import Base


# ======================================================
# ATS ANALYSIS MODEL
# ======================================================

class ATSAnalysis(Base):

    __tablename__ = "ats_analyses"

    # --------------------------------------------------
    # Primary Key
    # --------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # --------------------------------------------------
    # Resume Reference
    #
    # One Resume → One ATS Analysis
    # --------------------------------------------------

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False,
        unique=True
    )

    # --------------------------------------------------
    # Overall ATS Score
    # --------------------------------------------------

    ats_score = Column(
        Float,
        nullable=False,
        default=0
    )

    # --------------------------------------------------
    # Section Scores + Extracted Skills
    #
    # Stored as JSON text.
    # --------------------------------------------------

    section_scores = Column(
        Text,
        nullable=True
    )

    # --------------------------------------------------
    # Created Time
    # --------------------------------------------------

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # --------------------------------------------------
    # Relationship with Resume
    # --------------------------------------------------

    resume = relationship(
        "Resume",
        back_populates="ats_analysis",
        uselist=False
    )

