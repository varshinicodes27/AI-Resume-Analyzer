from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database.database import Base


# ======================================================
# RESUME MODEL
# ======================================================

class Resume(Base):

    __tablename__ = "resumes"

    # --------------------------------------------------
    # Primary Key
    # --------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # --------------------------------------------------
    # User Reference
    # --------------------------------------------------

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # --------------------------------------------------
    # Original Uploaded File Name
    # --------------------------------------------------

    file_name = Column(
        String(255),
        nullable=False
    )

    # --------------------------------------------------
    # Uploaded File Path
    # --------------------------------------------------

    file_path = Column(
        String(500),
        nullable=False
    )

    # --------------------------------------------------
    # Extracted Resume Text
    # --------------------------------------------------

    extracted_text = Column(
        Text,
        nullable=True
    )

    # --------------------------------------------------
    # Upload Timestamp
    # --------------------------------------------------

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # ==================================================
    # RELATIONSHIPS
    # ==================================================

    # --------------------------------------------------
    # User → Resumes
    # --------------------------------------------------

    user = relationship(
        "User",
        back_populates="resumes"
    )

    # --------------------------------------------------
    # Resume → ATS Analysis
    #
    # One Resume → One ATS Analysis
    # --------------------------------------------------

    ats_analysis = relationship(
        "ATSAnalysis",
        back_populates="resume",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )

