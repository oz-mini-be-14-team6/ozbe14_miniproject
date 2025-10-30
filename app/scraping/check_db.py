from funct.dbinsert import DatabaseManager, get_db_config

# DB 상태 스크립트
# 저장된 데이터 개수, 샘플 보여주기


def check_db():
    DB_CONFIG = get_db_config()
    db = DatabaseManager(**DB_CONFIG)

    try:
        db.connect()

        # 테이블 존재여부 check
        db.cursor.execute(
            """
                          SELECT tablename
                          from pg_tables
                          WHERE schemaname = 'public'
                            AND tablename IN ('quotes', 'reflection_questions')
                          """
        )
        tables = [row[0] for row in db.cursor.fetchall()]

        print("table status: ")
        print(f"    quotes: {'exist' if 'quotes' in tables else 'not exist'}")
        print(
            f"    reflection_questions: {'exist' if 'reflection_questions' in tables else 'not exist'}"
        )

        db.cursor.execute("SELECT COUNT(*) FROM quotes")
        quotes_count = db.cursor.fetchone()[0]

        db.cursor.execute("SELECT COUNT(*) FROM reflection_questions")
        reflection_questions_count = db.cursor.fetchone()[0]

        print("db status")
        print(f"    quotes_count: {quotes_count}")
        print(f"    reflection_questions_count: {reflection_questions_count}")

        if quotes_count > 0:
            db.cursor.execute("SELECT quote, author FROM quotes LIMIT 5")
            quotes = db.cursor.fetchall()
            print("SAMPLE: QUOTES")
            for i, (quote, author) in enumerate(quotes, 1):
                print(f"    {i}. {quote}    ─ {author}")
            print()

        if reflection_questions_count > 0:
            db.cursor.execute("SELECT question FROM reflection_questions LIMIT 5")
            questions = db.cursor.fetchall()
            print("SAMPLE: QUESTIONS")
            for i, question in enumerate(questions, 1):
                print(f"    {i}. {question}")
            print()

    except Exception as e:
        print(f"db error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    check_db()
