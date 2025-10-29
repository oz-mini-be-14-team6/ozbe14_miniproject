import os

from dotenv import load_dotenv

# 환경변수 읽기
load_dotenv()

# 환경변수에서 값 가져오기
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
