from fastapi import APIRouter

from app.scraping.funct.dbinsert import DatabaseManager, get_db_config

router = APIRouter()


@router.get("/random")
def get_random_quote():
    db = DatabaseManager(**get_db_config())

    try:
        db.connect()

        # quotes 테이블에서 랜덤 1개 선택
        db.cursor.execute("SELECT quote, author FROM quotes ORDER BY RANDOM() LIMIT 1;")
        row = db.cursor.fetchone()

        if row:
            quote, author = row
            return {
                "quote": quote,
                "author": author,
            }
        else:
            return None

    except Exception as e:
        print(f"db error: {e}")
        return None
    finally:
        db.close()


@router.get("/question")
def get_random_question():
    db = DatabaseManager(**get_db_config())

    try:
        db.connect()

        # reflection_questions 테이블에서 랜덤 1개 선택
        db.cursor.execute("SELECT question FROM reflection_questions ORDER BY RANDOM() LIMIT 1;")
        row = db.cursor.fetchone()

        if row:
            question = row[0]  # 튜플의 첫 번째 값이 question
            return {"question": question}
        else:
            return None

    except Exception as e:
        print(f"db error: {e}")
        return None
    finally:
        db.close()
