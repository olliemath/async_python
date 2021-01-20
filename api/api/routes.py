from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload

from .extensions import db
from .models import Author, Book
from . import marshallers


from werkzeug.exceptions import BadRequest


bp = Blueprint("app", __name__)


class InvalidParameter(BadRequest):
    code = 400
    description = "An invalid parameter was provided"


def validate_get(marshaller):
    parsed = marshaller.load(request.args)
    if parsed.errors:
        raise InvalidParameter(parsed.errors)

    return parsed.data


def validate_post(marshaller):
    parsed = marshaller.load(request.get_json(force=True))
    if parsed.errors:
        raise InvalidParameter(parsed.errors)

    return parsed.data


@bp.route("/author", methods=["GET", "POST"])
def author():
    """View all authors, or create a new one."""

    if request.method == "GET":
        args = validate_get(marshallers.LimitOffsetSchema())
        limit = args["limit"]
        offset = args["offset"]

        authors = Author.query.limit(limit).offset(offset).all()
        return jsonify(marshallers.authors.dump(authors))

    if request.method == "POST":
        author = Author(**validate_post(marshallers.author))

        db.session.add(author)
        db.session.commit()

        return jsonify({"id": author.id})


@bp.route("/author/<uuid:author_id>", methods=["GET"])
def author_detail(author_id):
    author = Author.query.filter_by(id=author_id).first_or_404()
    return jsonify(marshallers.author_detail.dump(author))


@bp.route("/book", methods=["GET", "POST"])
def book():

    if request.method == "GET":
        args = validate_get(marshallers.LimitOffsetSchema())
        limit = args["limit"]
        offset = args["offset"]

        books = Book.query.limit(limit).offset(offset).options(
            joinedload("author")
        ).all()
        return jsonify(marshallers.books.dump(books))

    if request.method == "POST":
        book_data = validate_post(marshallers.book)

        # Check author exists
        Author.query.filter_by(id=book_data["author_id"]).first_or_404()
        book = Book(**book_data)

        db.session.add(book)
        db.session.commit()

        return jsonify({"id": book.id})
