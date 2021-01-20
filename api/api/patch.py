"""
Apply any required patches for e.g. pypy/gevent
"""

import logging
import os

INTERPRETER = os.getenv("INTERPRETER")
WORKER_TYPE = os.getenv("GUNICORN_WORKER_TYPE")
DB_CONNECTOR = os.getenv("DB_CONNECTOR")


def patch_db_conn():
    """
    We use psycopg2cffi if under pypy, and we need to "greenify"
    it when under either an eventlet or a gevent worker
    """
    if INTERPRETER == "pypy3":
        from psycopg2cffi import compat
        logging.info("Patching PsycoPG2")
        compat.register()

    if WORKER_TYPE == "eventlet":
        import eventlet
        logging.info("Patching for Eventlet")
        eventlet.monkey_patch()

    elif WORKER_TYPE == "gevent" and DB_CONNECTOR == "psycopg":
        import psycogreen.gevent
        logging.info("Patching for Gevent")
        psycogreen.gevent.patch_psycopg()
