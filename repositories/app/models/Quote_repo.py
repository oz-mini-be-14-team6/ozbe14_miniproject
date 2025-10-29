from sqlalchemy.orm import Session

from app.models.quote import Quote
from app.schemas.quote import QuoteCreate, QuoteUpdate


def create_quote(db: Session, quote: QuoteCreate):
    db_quote = Quote(content=quote.content)
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote


def get_quote_by_id(db: Session, quote_id: int):
    return db.query(Quote).filter(Quote.id == quote_id).first()


def get_all_quotes(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Quote).offset(skip).limit(limit).all()


def update_quote(db: Session, quote_id: int, quote_update: QuoteUpdate):
    db_quote = get_quote_by_id(db, quote_id)
    if not db_quote:
        return None
    if quote_update.content:
        db_quote.content = quote_update.content
    db.commit()
    db.refresh(db_quote)
    return db_quote


def delete_quote(db: Session, quote_id: int):
    db_quote = get_quote_by_id(db, quote_id)
    if db_quote:
        db.delete(db_quote)
        db.commit()
    return db_quote
