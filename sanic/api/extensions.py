from tortoise.contrib.sanic import register_tortoise


DB_URL = "postgres://postgres:password@test-db/postgres"


def setup_database(app):
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": ["models"]},
        generate_schemas=False,
    )
