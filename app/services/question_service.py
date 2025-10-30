import random
from app.models.question import Question

# 랜덤 질문을 반환하는 함수
async def get_random_question():
    total = await Question.all().count()
    if total == 0:
        return None  # 질문이 없을 경우
    random_index = random.randint(0, total - 1)
    question = await Question.all().offset(random_index).limit(1).first()
    return question.text
