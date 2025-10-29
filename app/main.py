import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise

from app.api.v1 import auth, diary
from app.db.database import TORTOISE_ORM, init_db
from app.services.auth_service import cleanup_blacklist

app = FastAPI(title="FastAPI Mini Project")

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(diary.router, prefix="/diary", tags=["Diary"])

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # 마이그레이션 사용 시 False
    add_exception_handlers=True,
)


@app.on_event("startup")
async def startup_event():
    await init_db()  # DB 초기화

    # cleanup 블랙리스트 주기적 실행
    async def periodic_cleanup():
        while True:
            await cleanup_blacklist()  # 블랙리스트에서 기간 만료된 토큰 삭제
            await asyncio.sleep(3600)  # 1시간마다 실행

    asyncio.create_task(periodic_cleanup())


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})
