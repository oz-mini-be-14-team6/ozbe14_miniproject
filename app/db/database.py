from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {
        "default": "postgres://postgres@localhost:5432/oz_diary"
    },
    "apps": {
        "models": {
            # 우리가 만든 모델들을 여기에 등록
            "models": [
                "app.models.question",  # 질문 모델
                "aerich.models",        # aerich (필수)
            ],
            "default_connection": "default",
        },
    },
}

# -------------------------------
# DB 초기화
# -------------------------------
async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

# -------------------------------
# DB 종료
# -------------------------------
async def close_db():
    await Tortoise.close_connections()
