from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "questions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "questions";"""


MODELS_STATE = (
    "eJztlV9r2zAUxb9K8NMK3Wi9dC17y8L+0iWsy0ahFKPYiiMiS650vSWUfPfdK9uV47img8"
    "EW2Ft8zpF07w/d6D7IdMKlffGl4BaEVsHrwX2gWMbxx553PAhYnnuHBGBz6cJ3VcqpbG7B"
    "sBjQWDBpOUoJt7EReXWIKqQkUccYFCr1UqEEbhWBTjksuUHj5hZloRK+5rb+zFfRQnCZ7N"
    "QrEjrb6RFscqd9VPDOBem0eRRrWWTKh/MNLLV6SAsFpKZcccOA0/ZgCiqfqqtarTsqK/WR"
    "ssTGmoQvWCGh0e4TGcSIEflhNdY1mNIpz8PT4fnw4uWr4QVGXCUPyvm2bM/3Xi50BCazYO"
    "t8BqxMOIyeG/A17JObodqNrs634GHJbXg1qj56teDx+SvzZ/j1wJm9vZ5R0Zm1d5KEyffR"
    "1fjD6OrZ59H1kXM2lXM5nbyv4xovd3ntJ+PL6RvkS5dysWrgJWHO4tVPZpJoz9Ghfiy7b2"
    "Vh1laYYqljRR1Tf9WsjrgR8bJriiund4aZz/wf4AMa4B/c2OoPehfeeMlMN73GkkMZY7z1"
    "60hylQJd8PDsrIdZPcWYOmoNbGWFpUdgPUgajd+AWMUPE+DpyckTAGLqUYDO2wWIJwJXHa"
    "/Jp6/TSTfExpIWyG8KG7xJRAzHAyks3P6bWHsoUtf9z0v7JSEK2kJq3C5ug7/+vGx/AZhp"
    "O+I="
)
