from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.security import get_current_user
from app.models import Diary, User
from app.schemas.diary import DiaryCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# 일기 작성
@router.post("/create")
async def create_diary(diary: DiaryCreate, current_user: User = Depends(get_current_user)):
    await Diary.create(user=current_user, diary_title=diary.title, diary_content=diary.content)
    return {"message": "Diary created"}


# 일기 목록 조회
@router.get("/list")
async def list_diaries(
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="현재 페이지 번호"),
):
    skip = (page - 1) * 5

    diaries = (
        await Diary.filter(user=current_user)
        .order_by("-created_at")
        .offset(skip)
        .limit(5)
        .values("id", "diary_title", "diary_content", "created_at")
    )

    total = await Diary.filter(user=current_user).count()  # 전체 일기 개수
    has_next = total > page * 5  # 다음 페이지 존재 여부

    return {"page": page, "total": total, "has_next": has_next, "items": diaries}


# ruff: noqa: B008
