import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from tortoise.transactions import in_transaction

from app.models.models import User
from app.schemas.user import UserCreate

# 환견변수 읽기
load_dotenv()

router = APIRouter()

# 환경변수에서 값 가져오기
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# 비밀번호를 암호화 하기 위한 설정
pwd_context = CryptContext(
    schemes=["bcrypt"],  # 사용할 해싱 알고리즘 목록
    deprecated="auto",  # 오래된 알고리즘 자동 감지 후 업데이트
)
# JWT 인증을 위한 토큰 발급
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# 회원 가입시 비밀번호를 암호화해서 DB에 저장
def hash_password(password):
    return pwd_context.hash(password)


# 로그인시 입력한 비밀번호를 DB에 저장된 해시값과 검증
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)  # bool로 결과가 나옴


# JWT 유틸 함수
def create_access_token(data: dict | None = None) -> str:
    to_encode = data.copy()  # 원본 변형 방지
    now = datetime.now(timezone.utc)  # 현재 시간 명시
    expire = now + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )  # 현재시간 + 토큰 유효시간 = 만료시간

    to_encode.update(  # 페이로드에 클레임 추가
        {
            "iat": int(now.timestamp()),  # 발급시간
            "nbf": int(now.timestamp()),  # 이 시간 이전에는 유효 아님
            "exp": int(expire.timestamp()),  # 만료시간
        }
    )

    # JWT 암호화 해서 반환
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 현재 사용자 의존성 (토큰 검증)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        # 페이로드에서 주체로 저장된 사용자 식별자 확인 없으면 에러
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await User.get_or_none(username=username)  # DB에서 해당 사용자를 비동기 조회합니다

        if not user:  # 없으면 탈퇴/삭제/비활성화 등일 수 있으므로 401 처리.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user  # 있으면 반환

    except ExpiredSignatureError as e:  # 토큰 만료
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    except JWTError as j:  # 디코드 실패(서명 위조, 토큰 변조, 포맷 오류 등) 전부 401로 응답.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        ) from j


# 사용 예시
# @router.get("/me")
# async def me(current_user: User = Depends(get_current_user)):
# return {"username": current_user.username}


# 회원가입 엔드포인트
@router.post("/register")
async def register_user(user: UserCreate):
    # 유저가 보낸 id,pw 스키마를 받습니다 예시) { "username": "alice", "password": "S3cure!pwd" }
    async with (
        in_transaction()
    ):  # 하나의 트랜잭션으로 아래 DB 작업을 묶습니다 중간에 예외가 나면 롤백, 모두 성공하면 커밋됩니다.
        # 같은 아이디가 있는지 확인
        exists = await User.get_or_none(username=user.username)
        # 있으면 에러
        if exists:
            raise HTTPException(status_code=400, detail="Username already exists")
        # 아니면 비번은 해쉬값으로 변경
        hashed_pw = hash_password(user.password)
        # 그리고 DB에 저장
        new_user = await User.create(username=user.username, password=hashed_pw)
        # 성공 메세지와 신규 유저의 pk 반환
        return {"message": "User created successfully", "id": new_user.id}


# 로그인 엔드포인트
@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):  # noqa: B008
    # DB에서 해당 username을 가진 사용자를 비동기로 조회합니다 없으면 None을 반환합니다.
    user = await User.get_or_none(username=form_data.username)
    # 유저가 없거나, 비밀번호가 틀린 경우를 같은 메시지로 처리합니다
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # 토큰 생성
    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user)):  # noqa: B008
    return {"username": current_user.username}


@router.post("/logout")
async def logout():
    return {"message": "클라이언트에서 토큰 삭제로 로그아웃 처리"}
