# Gunicorn Worker Benchmarks

Read the blog post here: https://suade.org/dev/12-requests-per-second-with-python/

A simple API container for use benchmarking [gunicorn](https://gunicorn.org/) workers with a standard [Flask](http://flask.pocoo.org/) + [SQLAlchemy](https://www.sqlalchemy.org/) app. We are deliberately careful not to write a lightning-fast, unrealistic, bare-bones app. Thus we choose an example which is mostly identical to the SQLAlcehmy object-relational [tutorial](https://docs.sqlalchemy.org/en/latest/orm/tutorial.html) only we replaced users and posts with authors and books. We marshal arguments and return values using [Marshmallow](https://marshmallow.readthedocs.io/en/3.0/).

### Running the system

You'll need docker and docker-compose (>=3.5) installed. To get a running system, issue
```bash
$ docker-compose build
$ docker-compose up
```

If it's the first time you've run the system it will take a log time to seed dummy data.
Actually you can improve performance by outputing this to a CSV and then manually uploading with Postgres's COPY FROM command. As it stands, it's easier for me to leave this running in the background while I get on with other things, than to build it in to the app.

All configuration is done via environment variables - in particular, the following:
```bash
GUNICORN_WORKER_TYPE  # eventlet gevent sync
INTERPRETER  # pypy3 python3
DB_CONNECTOR  # pg8000 psycopg
```

### Benchmarking

Use [wrk](https://github.com/wg/wrk) - for example:
```
/wrk -t4 -c16 -d30s http://127.0.0.1:5000/author?limit=20&offset=500000"
```
