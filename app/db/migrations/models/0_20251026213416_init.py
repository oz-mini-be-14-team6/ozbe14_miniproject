from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "diaryentry" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
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
    "eJztll1vmzAUhv8K4iqTuqpl6Yd2x5JszdQkU8u2qlWFHOwQK2BTY9agKv99PgbCRxLUSN"
    "PWSLuD97y2z3kwPn4xQ45JEB/3KRLpgEmRmh+NF5OhkKiHLdEjw0RRVMZAkGgaaDsGH1n7"
    "prEUyJMqMkNBTJSESewJGknKmVJZEgQgck8ZKfNLKWH0KSGu5D6RcyJU4OFRyZRhsiRx8R"
    "ot3BklAa6lTDGsrXVXppHWhkx+1kZYbep6PEhCVpqjVM45W7spk6D6hBGBJIHppUggfcgu"
    "r7WoKMu0tGQpVsZgMkNJICvlvpKBxxnwU9nEukAfVnlvnXYvupcfzruXyqIzWSsXq6y8sv"
    "ZsoCYwdsyVjiOJMofGWHKTVKrpNtD15khsZ7ce0MCnkm7iK2C18SuEEmC5af4QwRAt3YAw"
    "X87V6+nJSQuvH/ZN78q+6SjXO6iGq42c7fFxHrKyGEAtIaoVJcm2Tx2jQ5Y7tmBlyKGAbO"
    "HmDO4cSDqM46egiqszsu80yTDNI9eT8ZfCXsHbu558alIVBOp30RawfRWRNCQ74NZGNvji"
    "fOhx8fA2aZuqBjxhQZqfKW30h6PBrWOPvtU+Qd92BhCxavgLtXPe2ODrSYyfQ+fKgFfjfj"
    "IeaII8lr7QK5Y+596EnFAiucv4s4tw5fgr1ALMCg7u2aJyBIEwRd7iGQnsbkS4xXd5N0Oh"
    "FTYVxJCvPwvAhTTzlmYTQb35tmaXR1obHSo9/5vcATW5X0TEkNIeba4y5FDO53qjs87OXt"
    "HolGtno9Ox+pEMv8YeEHP7YQL8uzeFr7eT8b43he9MFfiAqSePjIDG8vFtYm2hCFW33xua"
    "V4RGN4IJ4N7wT9vL6jcsID5V"
)
