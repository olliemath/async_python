from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from .models import BookGenres, BookStatuses, CountryCodes


class SchemaWithLoadDefaults(Schema):
    def make_object(self, in_data):
        for name, field in self.fields.items():
            if name not in in_data and field.metadata.get("missing"):
                in_data[name] = field.metadata["missing"]
        return in_data


class LimitOffsetSchema(Schema):
    limit = fields.Integer(
        validate=lambda val: val >= 1 and val <= 1000, missing=100
    )
    offset = fields.Integer(validate=lambda val: val >= 0, missing=0)


class Author(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    country_code = EnumField(CountryCodes, required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    contact_address = fields.Str(required=True)
    contract_started = fields.DateTime(format="iso")
    contract_finished = fields.DateTime(format="iso")
    contract_value = fields.Integer()


class Book(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Str(required=True)
    author = fields.Nested(Author, dump_only=True)
    published = fields.DateTime(format="iso")
    status = EnumField(BookStatuses, required=True)
    retail_price = fields.Integer(validate=lambda val: val >= 0)
    cost_price = fields.Integer(validate=lambda val: val >= 0)
    run = fields.Integer(validate=lambda val: val >= 0)
    volume = fields.Integer(validate=lambda val: val >= 0)
    genres = fields.List(EnumField(BookGenres))


class AuthorDetail(Author):
    books = fields.List(
        fields.Nested(Book, only=("id", "title", "published", "status")),
        dump_only=True,
    )
    genres = fields.List(fields.Str, dump_only=True)


author = Author()
authors = Author(many=True)
book = Book()
books = Book(many=True)
author_detail = AuthorDetail()
