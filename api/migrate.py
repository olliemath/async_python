"""
A simple migration script in liue of the need for anything fancy like Alembic
"""
from api.patch import patch_db_conn
patch_db_conn()

import sqlalchemy as sa  # noqa: E402
from sqlalchemy.engine.url import make_url  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from api.app import app, db  # noqa: E402
from api.seed import (  # noqa: E402
    create_authors_and_books, is_seeded, seed_enums
)


uri = app.config["SQLALCHEMY_DATABASE_URI"]
url = make_url(uri)
engine = sa.create_engine(url)
db.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

seed_enums(session)
if not is_seeded(session):
    create_authors_and_books(session, 1000 * 1000)
