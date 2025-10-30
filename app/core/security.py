from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.models import BlacklistedToken, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# 비밀번호를 암호화 하기 위한 설정
pwd_context = CryptContext(
    schemes=["bcrypt"],  # 사용할 해싱 알고리즘 목록
    deprecated="auto",  # 오래된 알고리즘 자동 감지 후 업데이트
)


# 입력받은 비밀번호를 해시값으로 반환하는 함수
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# 입력받은 비밀번호를 검증하기 위해 저장된 해시값이랑 비교하는 함수
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)  # 결과값은 bood


# JWT 토큰 생성 함수
def create_access_token(data: dict | None = None) -> str:
    to_encode = data.copy()  # 원본 변형 방지
    now = datetime.now(timezone.utc)  # 현재 시간 명시
    expire = now + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )  # 만료시간 = 현재시간 + 토큰 유효시간
    to_encode.update(
        {
            "iat": int(now.timestamp()),  # 발급시간
            "exp": int(expire.timestamp()),  # 만료시간
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 현재 사용자 의존성 (토큰 검증)
async def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        # 블랙리스트 먼저 확인
        blacklisted = await BlacklistedToken.get_or_none(token=token)
        if blacklisted:
            raise HTTPException(status_code=401, detail="로그인 유효시간이 만료되었습니다.")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        # 페이로드에서 주체로 저장된 사용자 식별자 확인 없으면 에러
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="잘못된 회원정보 입니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await User.get_or_none(username=username)  # DB에서 해당 사용자를 비동기 조회합니다

        if not user:  # 없으면 탈퇴/삭제/비활성화 등일 수 있으므로 401 처리.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="잘못된 회원 정보 입니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user  # 있으면 반환

    except ExpiredSignatureError as e:  # 토큰 만료
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인 시간이 만료되었습니다",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    except JWTError as j:  # 디코드 실패(서명 위조, 토큰 변조, 포맷 오류 등) 전부 401로 응답.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        ) from j
