import random

from faker import Faker
from faker.providers import internet

from .models import (
    Author,
    Book,
    BookStatus,
    BookStatuses,
    BookGenres,
    CountryCode,
    CountryCodes,
)

random.seed(1234)
fake = Faker()
fake.add_provider(internet)


def create_author():
    return Author(
        name=fake.name(),
        country_code=random.choice(list(CountryCodes)),
        email=fake.email(),
        phone=fake.phone_number(),
        contact_address=fake.address(),
        contract_started=fake.date_time(),
        contract_finished=fake.date_time(),
        contract_value=fake.random_digit(),
    )


def create_book(author):
    return Book(
        title=fake.sentence(
            nb_words=6, variable_nb_words=True, ext_word_list=None
        ),
        author_id=author.id,
        published=fake.date_time(),
        status=random.choice(list(BookStatuses)),
        retail_price=random.randint(0, 100 * 100),
        cost_price=random.randint(0, 100 * 100),
        run=random.randint(0, 10),
        volume=random.randint(10 * 1000, 100 * 1000),
        genres=random.sample(list(BookGenres), random.randint(1, 3)),
    )


def _create_authors_and_books(session, n_authors=1000):
    print("Seeding {} authors".format(n_authors))
    authors = [create_author() for _ in range(n_authors)]
    session.add_all(authors)
    session.commit()

    books = []
    for author in authors:
        books += [create_book(author) for _ in range(random.randint(0, 20))]
    session.add_all(books)
    session.commit()


def create_authors_and_books(session, n_authors=1000):

    CHUNKSIZE = 100000
    n_chunks = n_authors // CHUNKSIZE
    for _ in range(n_chunks):
        _create_authors_and_books(session, CHUNKSIZE)

    remainder = n_authors % CHUNKSIZE
    if remainder:
        _create_authors_and_books(session, remainder)


def seed_enums(session):
    if not session.query(BookStatus).count():
        statuses = [BookStatus(id=status) for status in BookStatuses]
        codes = [CountryCode(id=code) for code in CountryCodes]

        session.add_all(statuses + codes)
        session.commit()
