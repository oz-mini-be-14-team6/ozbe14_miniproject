from sqlalchemy.orm import Session

from app.models.bookmark import Bookmark
from app.schemas.bookmark import BookmarkCreate


def create_bookmark(db: Session, bookmark: BookmarkCreate):
    db_bookmark = Bookmark(userid=bookmark.userid, quotesid=bookmark.quotesid)
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


def get_bookmarks_by_user(db: Session, userid: int):
    return db.query(Bookmark).filter(Bookmark.userid == userid).all()


def delete_bookmark(db: Session, bookmark_id: int):
    db_bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if db_bookmark:
        db.delete(db_bookmark)
        db.commit()
    return db_bookmark
