from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "quotes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "author" VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL UNIQUE,
    "password" VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "bookmarks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "quote_id" INT NOT NULL REFERENCES "quotes" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "diaries" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "diary_title" VARCHAR(100) NOT NULL,
    "diary_content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmG1vmzAQx79KxKtO6qY265P2jjx0zdomW0u3qlWFHHCIFbBTY5aiKt99toHwEKClat"
    "Sg8S65O4Pvx/n+B8+KQ0xou186hMwcQGeu8q31rGDgQP5j3bnbUsB8HruEgYGxLaPHqbCx"
    "yygwGHdMgO1CbjKha1A0Z4hgbsWebQsjMXggwlZs8jB69KDOiAXZFFLuuH/gZoRN+ATd6O"
    "98pk8QtM3UhpEp7i3tOvPn0jbA7FQGiruNdYPYnoPj4LnPpgSvohFmwmpBDClgUFyeUU9s"
    "X+wuTDXKKNhpHBJsMbHGhBPg2SyR7isZGAQLfnw3wROxxF0+t/cPjg9Ovh4dnPAQuZOV5X"
    "gZpBfnHiyUBIaaspR+wEAQITHG3B49wqBeiV5yycsMI2JlECNDTDGunG3CGGPzXEirUUus"
    "+J+giQM7meWWniCyDvCUUIgsfA59yXHAdwSwAXO4hT3qJrzM9vFbRjUQWeP2QMFi1cSSpc"
    "HT40lBJhPsqtddtddXUpUnT987YPsVXae+3JKNKB+cqL4xMGYLQE09VYbCQ9okY1nFrruc"
    "tpO1AAwsCUCkITYdou0hQP08OQ0cpVJq8hAEGyGtnZCKB+frDDE753R2p4DmE8wsy6DkCW"
    "znEeXF/6TbEFtsyv/u7+2VsPutXnXP1KsdHvVJHlVe1EGxD0NXO/ClJTYgw+/LYFBQaaQa"
    "fCooyrWFdYFawlDr32pi047rPtpJdDuX6q2k6vih52I0/B6FJ1B3L0adDGGDQpG/DnLw9r"
    "iHIQfmI06vzPA1w6Vfoh/bSVvhOZgjbPthrymjP7jsX2vq5c/UI+ipWl942in8kXXnKFPs"
    "q4u0/gy0s5b427obDfuSIHGZReUd4zjtTii/AjxGdEwWOjATbTGyRmCa6bSZTj9oOv2YIS"
    "uYX3OGrNVgWzxkycGxmbFqN2O9YRhoxoAXxwAuJVOS0+uKh9Z4RV2YbmheXdOP4l4Y8059"
    "LU0j74RLT8+voA1kkoXKkvo2u33Ei+RluUlRkGqbowmRChdLglC5RhFqpwjiscnfFbpXcs"
    "379K+NU9z82/YcuO6C0JwyLAaZXNMIQSMEFYUg+7En/Oz5dhCrz6s1grBJNVQhRcY0Tw9D"
    "T6kigjimkcQaSeJfPsiEx+S1jTyxpJ59vH14+Io+zqMK+7j0Zd6L+NGoADEMryfAjcwUha"
    "/rP65Hw6qv6zeYJ3hvIoPttmzksoftxFpCUWRd/vKefU/fTX8ZFhfoVBs23l9elv8Ajl2m"
    "cA=="
)
