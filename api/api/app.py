from flask import Flask
from .extensions import db, uuid_
from .patch import DB_CONNECTOR
from .routes import bp


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

if DB_CONNECTOR == "psycopg":
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2://postgres:password@db/postgres"
else:
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+pg8000://postgres:password@db/postgres"


db.init_app(app)
uuid_.init_app(app)
app.register_blueprint(bp)
