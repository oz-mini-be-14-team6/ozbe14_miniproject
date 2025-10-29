from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Diary(Base):
    __tablename__ = "diary"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    diary_title = Column(String(255), nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="diaries")
