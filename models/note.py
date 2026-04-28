from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from db.base import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())