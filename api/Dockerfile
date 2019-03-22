FROM python:2
# FROM pypy:2-6.0.0

COPY gunicorn.conf.py /
COPY run.sh /

RUN useradd -m --uid 1000 api
COPY requirements.txt /home/api/
COPY gunicorn.conf.py /home/api/
WORKDIR /home/api/src
USER api

ENV GUNICORN_TIMEOUT=1200 \
    TERM=xterm \
    PATH=/home/api/.local/bin:$PATH \
    PYTHONPATH=/home/api/.local/lib/python2.7/site-packages/:$PYTHONPATH

RUN pip install -q --user --upgrade pip setuptools
RUN pip install -q --user -r /home/api/requirements.txt

ENTRYPOINT ["/run.sh"]
