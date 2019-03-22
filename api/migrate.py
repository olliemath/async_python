"""
A simple migration script in liue of the need for anything fancy like Alembic
"""
from __future__ import absolute_import
from psycopg2cffi import compat

compat.register()

import sqlalchemy as sa  # noqa: F401
from sqlalchemy.engine.url import make_url  # noqa: F401
from sqlalchemy.orm import sessionmaker  # noqa: F401

from api.app import app, db  # noqa: F401
from api.seed import create_authors_and_books, seed_enums  # noqa: F401


uri = app.config["SQLALCHEMY_DATABASE_URI"]
url = make_url(uri)
engine = sa.create_engine(url)
db.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

seed_enums(session)
create_authors_and_books(session, 1000 * 1000)
