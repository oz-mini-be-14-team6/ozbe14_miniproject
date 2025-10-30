from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.security import get_current_user
from app.models import User
from app.schemas.user import UserCreate
from app.services.auth_service import authenticate_user, blacklist_token, register_user_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# 회원가입 엔드포인트
@router.post("/register")
async def register_user(user: UserCreate):

    new_user = await register_user_service(user.username, user.password)

    return {"message": "회원 가입에 성공하셨습니다.", "id": new_user.id}


# 로그인 엔드포인트
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    token = await authenticate_user(form_data.username, form_data.password)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user)):  # noqa: B008
    return {"username": current_user.username}


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)
):

    await blacklist_token(token)
    return {"message": f"User '{current_user.username}' logged out successfully"}


# ruff: noqa: B008
