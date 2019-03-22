from enum import Enum
import json
import uuid

from iso3166 import countries_by_alpha2
from sqlalchemy.types import STRINGTYPE, TypeDecorator
from sqlalchemy_utils import ChoiceType, UUIDType
from .extensions import db


CountryCodes = Enum("CountryCodes", {cc: cc for cc in countries_by_alpha2})


class CountryCode(db.Model):
    id = db.Column(
        ChoiceType(CountryCodes, impl=db.String()),
        nullable=False,
        primary_key=True,
    )


class BookStatuses(Enum):
    published = "published"
    draft = "draft"
    discontinued = "discontinued"


class BookStatus(db.Model):
    id = db.Column(
        ChoiceType(BookStatuses, impl=db.String()),
        nullable=False,
        primary_key=True,
    )


class BookGenres(Enum):
    existential_fiction = "Existential Fiction"
    beatnik_poetry = "Beatnik Poetry"
    rap = "Rap"
    non_fictional_lulz = "Non Fictional Lulz"


class JSONEncodedDict(TypeDecorator):
    impl = STRINGTYPE

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)


class Author(db.Model):
    id = db.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    country_code = db.Column(
        "country_code_id",
        ChoiceType(CountryCodes, impl=db.String()),
        db.ForeignKey("country_code.id"),
        nullable=False,
    )

    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    contact_address = db.Column(db.String, nullable=False)

    contract_started = db.Column(db.DateTime)
    contract_finished = db.Column(db.DateTime)
    contract_value = db.Column(db.Integer)

    @property
    def genres(self):
        result = set()
        for book in self.books:
            result.update(book.genres)

        return sorted(result)


class Book(db.Model):
    def __init__(self, **kwargs):
        genres = kwargs.get("genres", [])
        for genre in genres:
            if not isinstance(genre, BookGenres):
                raise TypeError(
                    "{} is not a BookGenres instance".format(genre)
                )

        if genres:
            kwargs["genres"] = [genre.value for genre in genres]

        super(Book, self).__init__(**kwargs)

    id = db.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String, nullable=False)
    author_id = db.Column(
        UUIDType, db.ForeignKey("author.id"), nullable=False, index=True
    )
    author = db.relationship("Author", backref="books")
    published = db.Column(db.DateTime)
    status = db.Column(
        "status_id",
        ChoiceType(BookStatuses, impl=db.String()),
        db.ForeignKey("book_status.id"),
        nullable=False,
    )

    retail_price = db.Column(db.Integer)
    cost_price = db.Column(db.Integer)
    run = db.Column(db.Integer)
    volume = db.Column(db.Integer)

    # Let's assume we're lazy and don't bother with many-many relationships
    genres = db.Column(
        JSONEncodedDict,
        nullable=False,
        default=[BookGenres.existential_fiction.value],
    )
