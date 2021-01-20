from enum import Enum
import json
import uuid

from iso3166 import countries_by_alpha2
from tortoise.models import Model
from tortoise import fields


CountryCodes = Enum("CountryCodes", {cc: cc for cc in countries_by_alpha2})


class CountryCode(Model):
    id = fields.CharEnumField(CountryCodes, pk=True)

    class Meta:
        table = "country_code"


class BookStatuses(Enum):
    published = "published"
    draft = "draft"
    discontinued = "discontinued"


class BookStatus(Model):
    id = fields.CharEnumField(BookStatuses, pk=True)

    class Meta:
        table = "book_status"


class BookGenres(Enum):
    existential_fiction = "Existential Fiction"
    beatnik_poetry = "Beatnik Poetry"
    rap = "Rap"
    non_fictional_lulz = "Non Fictional Lulz"


class JSONEncodedField(fields.TextField):

    def to_db_value(self, value, instance):
        if value is not None:
            return json.dumps(value)

    def to_python_value(self, value):
        if value is None:
            return value

        return json.loads(value)


class Author(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.TextField()
    country_code = fields.ForeignKeyField("models.CountryCode")
    email = fields.TextField()
    phone = fields.TextField()
    contact_address = fields.TextField()

    contract_started = fields.DatetimeField(null=True)
    contract_finished = fields.DatetimeField(null=True)
    contract_value = fields.IntField(null=True)

    @property
    def genres(self):
        result = set()
        for book in self.books:
            result.update(book.genres)

        return sorted(result)


class Book(Model):
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

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    title = fields.TextField()
    author = fields.ForeignKeyField(
        "models.Author", related_name="books", null=True
    )
    published = fields.DatetimeField(null=True)
    status = fields.ForeignKeyField("models.BookStatus", null=True)
    retail_price = fields.IntField(null=True)
    cost_price = fields.IntField(null=True)
    run = fields.IntField(null=True)
    volume = fields.IntField(null=True)

    # Let's assume we're lazy and don't bother with many-many relationships
    genres = JSONEncodedField(
        null=False, default=[BookGenres.existential_fiction.value]
    )
