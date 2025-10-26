from fastapi import FastAPI
from database import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # 마이그레이션 사용 시 False
    add_exception_handlers=True
)

@app.get("/")
async def root():
    return {"message": "FastAPI + PostgreSQL + TortoiseORM OK"}
