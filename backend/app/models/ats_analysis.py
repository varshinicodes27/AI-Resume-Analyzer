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


class ATSAnalysis(Base):
    __tablename__ = "ats_analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False,
        unique=True
    )

    ats_score = Column(
        Float,
        nullable=False
    )

    section_scores = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    resume = relationship(
        "Resume",
        back_populates="ats_analysis"
    )