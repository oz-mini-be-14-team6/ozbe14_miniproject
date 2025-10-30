from datetime import datetime, timedelta, timezone

from fastapi import HTTPException

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import create_access_token, hash_password, verify_password
from app.models import BlacklistedToken, User


async def register_user_service(username: str, password: str):
    # 아이디 중복 검증
    exists = await User.get_or_none(username=username)
    if exists:
        raise HTTPException(status_code=400, detail="사용 중인 아이디 입니다.")

    # 비밀번호를 해쉬값으로 변경
    hashed_pw = hash_password(password)

    new_user = await User.create(username=username, password=hashed_pw)
    return new_user


async def authenticate_user(username: str, password: str):
    # 존재하는 아이디인지 검증
    user = await User.get_or_none(username=username)
    # 아이디가 없거나 / 비밀번호 검증 값이 false일 경우 에러
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="잘못된 회원 정보입니다.")

    token = create_access_token({"sub": user.username})

    return token


async def blacklist_token(token: str):
    # 블랙리스트에 존재하는 토큰인지 검증
    exists = await BlacklistedToken.get_or_none(token=token)

    if not exists:
        await BlacklistedToken.create(token=token)


async def cleanup_blacklist():
    expire_time = datetime.now(timezone.utc) - timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    await BlacklistedToken.filter(blacklisted_at__lt=expire_time).delete()
