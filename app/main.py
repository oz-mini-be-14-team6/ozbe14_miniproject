from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.api import auth
from app.db.database import TORTOISE_ORM

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
