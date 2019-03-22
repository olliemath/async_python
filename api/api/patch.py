import logging
import os

try:
    # May be under PyPy - in which case we need to patch psycopg2
    from psycopg2cffi import compat

    logging.info("Patching PsycoPG2")
    compat.register()
except ImportError:
    pass


WORKER_TYPE = os.getenv("GUNICORN_WORKER_TYPE")
DB_CONNECTOR = os.getenv("DB_CONNECTOR")


def patch_db_conn():
    if WORKER_TYPE == "eventlet":
        import eventlet

        logging.info("Patching for Eventlet")
        eventlet.monkey_patch()

    elif WORKER_TYPE == "gevent" and DB_CONNECTOR == "psycopg":
        import psycogreen.gevent

        logging.info("Patching for Gevent")
        psycogreen.gevent.patch_psycopg()
