FROM pypy:3-7.0.0
# Or, to build the CPython version:
# FROM python:3.6

RUN useradd -m --uid 1000 api
COPY run.sh requirements.txt gunicorn_entrypoint.py /home/api/
COPY api/ /home/api/api/
RUN chown -R api:api /home/api

WORKDIR /home/api/
USER api

ENV PATH=/home/api/.local/bin:$PATH \
    PYTHONPATH=/home/api/.local/lib/python2.7/site-packages/:$PYTHONPATH

RUN pip install --user -r /home/api/requirements.txt

ENTRYPOINT ["/home/api/run.sh"]
