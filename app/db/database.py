import os

from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],  # aerich.models 포함
            "default_connection": "default",
        }
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
