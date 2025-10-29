from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.diary import Diary
from app.schemas.diary import DiaryCreate, DiaryUpdate


def create_diary(db: Session, diary: DiaryCreate, userid: int):
    db_diary = Diary(userid=userid, diary_title=diary.diary_title)
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    return db_diary


def get_diary_by_id(db: Session, diary_id: int):
    return db.query(Diary).filter(Diary.id == diary_id).first()


def get_user_diaries(db: Session, userid: int, skip: int = 0, limit: int = 10, search: str = None):
    query = db.query(Diary).filter(Diary.userid == userid)
    if search:
        query = query.filter(Diary.diary_title.contains(search))
    return query.order_by(desc(Diary.created_date)).offset(skip).limit(limit).all()


def update_diary(db: Session, diary_id: int, diary_update: DiaryUpdate):
    db_diary = get_diary_by_id(db, diary_id)
    if not db_diary:
        return None
    if diary_update.diary_title:
        db_diary.diary_title = diary_update.diary_title
    db.commit()
    db.refresh(db_diary)
    return db_diary


def delete_diary(db: Session, diary_id: int):
    db_diary = get_diary_by_id(db, diary_id)
    if db_diary:
        db.delete(db_diary)
        db.commit()
    return db_diary
