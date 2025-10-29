from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class Bookmark(Base):
    __tablename__ = "bookmark"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    quotesid = Column(Integer, ForeignKey("quotes.id", ondelete="CASCADE"))

    # Relationships
    user = relationship("User", back_populates="bookmarks")
    quote = relationship("Quote", back_populates="bookmarks")
