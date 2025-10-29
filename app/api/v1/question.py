from fastapi import APIRouter
from app.models.question import Question
import random

router = APIRouter()

@router.get("/random-question")
async def get_random_question():
    total = await Question.all().count()
    if total == 0:
        return {"message": "질문 데이터가 없습니다."}
    random_index = random.randint(0, total - 1)
    question = await Question.all().offset(random_index).limit(1).first()
    return {"question": question.text}
