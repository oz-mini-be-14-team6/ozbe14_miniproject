import os

from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # aerich.models 포함
            "default_connection": "default",
        }
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()  # 초기 개발용 (Aerich 적용 시 삭제 가능)
