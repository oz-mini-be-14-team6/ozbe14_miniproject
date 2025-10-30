import os

from dotenv import load_dotenv

# 환경변수 읽기
load_dotenv()

# 환경변수에서 값 가져오기
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

DB_NAME = (os.getenv("DB_NAME", "diary"),)
USER = (os.getenv("DB_USER", "postgres"),)
PASSWORD = (os.getenv("DB_PASSWORD", "alerpT@j0y"),)
HOST = (os.getenv("DB_HOST", "localhost"),)
PORT = (int(os.getenv("DB_PORT", 5432)),)
