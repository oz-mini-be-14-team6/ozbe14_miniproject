from fastapi import FastAPI
from app.db.database import init_db, close_db
from app.api.v1 import question   # 👈 질문 API 라우터 import

app = FastAPI()

# -------------------------------
# DB 연결 이벤트
# -------------------------------
@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# -------------------------------
# 기본 라우트
# -------------------------------
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI + PostgreSQL + TortoiseORM!"}

# -------------------------------
# 랜덤 질문 라우트 등록
# -------------------------------
app.include_router(
    question.router,
    prefix="/api/v1/questions",
    tags=["questions"]
)

