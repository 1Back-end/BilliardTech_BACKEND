from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.main.models.db.base_class import Base


class Program(Base):
    __tablename__ = "programs"

    uuid = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)

    added_by = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[added_by])

    academic_year_uuid = Column(String, ForeignKey("academic_years.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=True)
    academic_year = relationship("AcademicYear", foreign_keys=[academic_year_uuid])

    

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
