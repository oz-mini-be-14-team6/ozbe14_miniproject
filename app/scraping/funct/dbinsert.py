import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_batch

# .env 파일에서 환경 변수 로드
load_dotenv()

# AWS에선 이렇게?
# ENVIRONMENT=production
# DB_HOST=mydb.c1a2b3c4d5e6.ap-northeast-2.rds.amazonaws.com
# DB_PORT=5432
# DB_PASSWORD=strong_password


# PostgreSQL 데이터베이스 관리 클래스
class DatabaseManager:

    def __init__(self, dbname, user, password, host="localhost", port=5432, sslmode="prefer"):
        """DB 연결 초기화
        Args:
            dbname: 데이터베이스 이름
            user: 사용자명
            password: 비밀번호
            host: 호스트 주소 (AWS RDS 엔드포인트 등)
            port: 포트 번호 (기본 5432)
            sslmode: SSL 모드 ('disable', 'prefer', 'require')
        """
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
            "sslmode": sslmode,  # AWS RDS: SSL 필수
            "connect_timeout": 10,  # 연결 타임아웃 설정
        }
        self.conn = None
        self.cursor = None

    """
    데이터베이스 연결
    """

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cursor = self.conn.cursor()
            print(f"✅ DB 연결 성공: {self.conn_params['host']}")
        except Exception as e:
            print(f"❌ DB 연결 실패: {e}")
            raise

    def close(self):
        """연결 종료"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("✅ DB 연결 종료")

    # 테이블 생성 (없을 경우에만)
    def create_tables(self):
        try:
            # quotes 테이블
            self.cursor.execute(
                """
                                CREATE TABLE IF NOT EXISTS quotes (
                                id SERIAL PRIMARY KEY,
                                quote TEXT NOT NULL,
                                author VARCHAR(200) NOT NULL,
                                CREATE_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )
                                """
            )

            # reflection_questions 테이블
            self.cursor.execute(
                """
                                CREATE TABLE IF NOT EXISTS reflection_questions(
                                id SERIAL PRIMARY KEY,
                                question TEXT NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )
                                """
            )

            self.conn.commit()
            print("✅ 테이블 생성/확인 완료")
        except Exception as e:
            print(f"❌ 테이블 생성 실패: {e}")
            self.conn.rollback()

    # 명언 데이터 일괄삽입
    def insert_quotes(self, quotes_list):
        try:
            insert_query = """
                           INSERT INTO quotes (quote, author)
                           VALUES (%s, %s) ON CONFLICT (question) DO NOTHING
                           """

            data = [(item["quote"], item["author"]) for item in quotes_list]
            execute_batch(self.cursor, insert_query, data)

            self.conn.commit()
            print(f"✅ {len(quotes_list)}개의 명언 저장 완료")
            return self.cursor.rowcount
        except Exception as e:
            print(f"❌ 명언 저장 실패: {e}")
            self.conn.rollback()
            return 0

    # 질문 데이터 일괄 삽입 (중복 자동 제거)
    def insert_questions(self, questions_list):
        try:
            insert_query = """
                           INSERT INTO reflection_questions (question)
                           VALUES (%s) ON CONFLICT (question) DO NOTHING
                           """

            data = [(question,) for question in questions_list]
            execute_batch(self.cursor, insert_query, data)

            self.conn.commit()
            print(f"✅ {len(questions_list)}개의 질문 저장 완료")
            return self.cursor.rowcount
        except Exception as e:
            print(f"❌ 질문 저장 실패: {e}")
            self.conn.rollback()
            return 0

    # 테이블 삭제
    def drop_tables(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS quotes CASCADE")
            self.cursor.execute("DROP TABLE IF EXISTS reflection_questions CASCADE")
            self.conn.commit()
            print("✅ 테이블 삭제 완료")
        except Exception as e:
            print(f"❗ 테이블 삭제 실패: {e}")
            self.conn.rollback()


def get_db_config():
    """환경 변수에서 DB 설정 읽기

    환경에 따라 자동으로 적절한 설정 반환:
    - 로컬 개발: localhost
    - 배포 환경: AWS RDS 등
    """
    # 환경 변수 확인
    env = os.getenv("ENVIRONMENT", "development")

    if env == "production":
        # 프로덕션 환경 (AWS RDS 등)
        return {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),  # AWS RDS 엔드포인트
            "port": int(os.getenv("DB_PORT", 5432)),
            "sslmode": "require",  # AWS RDS는 SSL 필수
        }
    else:
        # 개발 환경 (로컬)
        return {
            "dbname": os.getenv("DB_NAME", "mydb"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "password"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", 5432)),
            "sslmode": "prefer",
        }
