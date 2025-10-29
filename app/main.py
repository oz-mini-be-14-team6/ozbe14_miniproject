import asyncio

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.api import auth
from app.api.auth import cleanup_blacklist
from app.db.database import TORTOISE_ORM, init_db

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # 마이그레이션 사용 시 False
    add_exception_handlers=True,
)


@app.get("/")
async def root():
    return {"message": "FastAPI + PostgreSQL + TortoiseORM OK"}


app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.on_event("startup")
async def startup_event():
    await init_db()  # DB 초기화

    # cleanup 블랙리스트 주기적 실행
    async def periodic_cleanup():
        while True:
            await cleanup_blacklist()  # 블랙리스트에서 기간 만료된 토큰 삭제
            await asyncio.sleep(3600)  # 1시간마다 실행

    asyncio.create_task(periodic_cleanup())
