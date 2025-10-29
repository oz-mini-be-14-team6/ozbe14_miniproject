from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String(500), nullable=True)

    bookmarks = relationship("Bookmark", back_populates="quote", cascade="all, delete-orphan")
