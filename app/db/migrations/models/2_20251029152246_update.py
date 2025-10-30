from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "blacklisted_tokens" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(512) NOT NULL UNIQUE,
    "blacklisted_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
        CREATE TABLE IF NOT EXISTS "bookmarks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "quote_id" INT NOT NULL REFERENCES "quotes" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        DROP TABLE IF EXISTS "bookmarks";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "blacklisted_tokens";
        DROP TABLE IF EXISTS "bookmarks";"""


MODELS_STATE = (
    "eJztmltvmzAUgP9KlKdW6qY26017I2m6Zm2TraVb1apCDjjECtgpmKVRlf8+20AwBGiIki"
    "VovIXjc8Dns30ubt/rNjGg5X5uWkAfWcil0FDJCOL619p7HQMbsh+ZOge1OhiPIw0uoKBv"
    "CaN+pK1Rri6GQd+lDtAp0xgAy4VMZEBXd9CYIsK/ij3L4kKiM0WEzUjkYfTqQfYuE9IhdN"
    "jA8wsTI2zAN+iGj+ORNkDQMmIOIIN/W8g1Oh0LWQfTS6HIv9bXdGJ5No6Ux1M6JHiujTDl"
    "UhNi6ADmEpNRx+PT57MLfA498mcaqfhTlGwMOACeRSV3l2SgE8z5sdm4wkGTf+VT4+j47P"
    "j8y+nxOVMRM5lLzma+e5HvvqEg0FXrMzEOKPA1BMaIGw2XOY6uNQROOru5QQIfm3QSXwhr"
    "q/xs8KZZEJt0yB5Pjho5tH4pd60r5W6Pae1zXwjbxv5O7wZDDX+MI40QyscA0EWWFwwHRT"
    "ZM57lonQBrBOafwx+rYA4FEefobK4JtAOB0cPWNFjDHM5q57Z9ryq3P7gntuu+WgKTorb5"
    "SENIpwnp3mliSeYvqf3uqFc1/lh76nXbgiBxqemIL0Z66lOdzwl4lGiYTDRgSNstlIZgZj"
    "zQDEbSkeGCPluqCXAMbWGENEiW7uKQ3bCTEoCBKZaFw+XTDAMyISMbOKPUYB2O5QfpQKuK"
    "zaWLza8eoVArRE82+ZjhjkSOtWCMsHkudIpRkyz+J2gLMS7OcBHgJXEgMvE1nAqOHTYjgH"
    "WYwi0IUQ/Ba3aP3yzcA6E0Cg8OmMyDmLw1mHvMKUj9Akm5bykX7Xps54nTtwZsP8P3lJeb"
    "HIjSwW0noV4g4EzTsqk/kJtKDaaCYJVIS5dI+cJNNYqolXI6s1udhNl6Gp5/kBpiLc/R4e"
    "ESLQ/Tymx5xFg8xfpk2HcpxCkdjwrfMjblgmFZoOa1M+1HNdbJhOj2bpXH/Vg3c9PrfgvV"
    "JdStm14zQVhn7dRqDWXcsmomd6CZrKrTqjrdTnW6nSLLr19Tiqx5YZtdZInCsaqxSldjrV"
    "AMVGXAh2UASyVDkhLrsovWyKIsTDdUrxa4wZXu8uXb0jjyZmB6eX0HLSCczMws8tXs7gHP"
    "yi6zTeYEkWxTUkKYhLMzAk9yVUIoXULgyyZ+Fwhesk0Z/764kWZ7DFx3QpyUbZgNUrap8k"
    "CVB4rlgeRVT3DpuTqH+eVqiSBsMhkq0EH6MC0dBiO5CRFEOlVGLFFG/MPqmOCYLBvHJZNy"
    "hvHGyckSYZxpZYZxMZboitjRKAAxUC8nwI2UFJnN+vf7Xrdos/6AmYPPBtLpQY3/I9PLbm"
    "LNoci9zm/dk136QfxemL+gWazWWH96mf0F2eB5+w=="
)
