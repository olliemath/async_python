from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import InvalidUsage, NotFound

from models import Author, Book
import marshallers


bp = Blueprint("app")


class InvalidParameter(InvalidUsage):
    description = "An invalid parameter was provided"


def validate_get(request, marshaller):
    parsed = marshaller.load(request.args)
    if parsed.errors:
        raise InvalidParameter(parsed.errors)

    return parsed.data


def validate_post(request, marshaller):
    parsed = marshaller.load(request.json)
    if parsed.errors:
        raise InvalidParameter(parsed.errors)

    return parsed.data


@bp.route("/author", methods=["GET", "POST"])
async def author(request):
    """View all authors, or create a new one."""

    if request.method == "GET":
        args = validate_get(request, marshallers.LimitOffsetSchema())
        limit = args["limit"]
        offset = args["offset"]

        authors = await Author.all().prefetch_related(
            "country_code"
        ).limit(limit).offset(offset)
        return json(marshallers.authors.dump(authors))

    if request.method == "POST":
        author = Author(**validate_post(marshallers.author))
        await author.save()

        return json({"id": author.id})


@bp.route("/author/<author_id:uuid>", methods=["GET"])
async def author_detail(request, author_id):

    author = await Author.filter(id=author_id).prefetch_related(
        "country_code", "books"
    ).first()

    if author is None:
        raise NotFound(author_id)

    return json(marshallers.author_detail.dump(author))


def get_genres(books):
    genres = set()
    for book in books:
        genres.update(book.get("genres"))
    return sorted(genres)


@bp.route("/book", methods=["GET", "POST"])
async def book(request):

    if request.method == "GET":
        args = validate_get(marshallers.LimitOffsetSchema())
        limit = args["limit"]
        offset = args["offset"]

        books = await Book.all().limit(limit).offset(
            offset
        ).prefetch_related("author")
        return json(marshallers.books.dump(books))

    if request.method == "POST":
        book_data = validate_post(marshallers.book)

        # Check author exists
        author = await Author.filter(id=book_data["author_id"]).first()
        if author is None:
            raise NotFound(book_data["author_id"])

        book = Book(**book_data)
        await book.save()

        return json({"id": book.id})
