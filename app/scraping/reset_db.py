from funct.dbinsert import DatabaseManager, get_db_config

# DB 리셋 스크립트


# db 리셋
def reset_db():
    print("resetting db")
    print("❗모든 데이터가 삭제됩니다.")

    confirm_db_delete = input("계속하시겠습니까? (yes/no)").lower()
    if confirm_db_delete != "yes":
        print("리셋 취소")
        return

    DB_CONFIG = get_db_config()
    db = DatabaseManager(**DB_CONFIG)

    try:
        db.connect()

        db.drop_tables()
        db.create_tables()

    except Exception as e:
        print(f"Reset db error: {e}")

    finally:
        db.close()


# 실행
if __name__ == "__main__":
    reset_db()
