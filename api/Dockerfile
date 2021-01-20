FROM pypy:3-7.3.3

COPY run.sh requirements.txt gunicorn_entrypoint.py migrate.py /home/api/
RUN pip install -r /home/api/requirements.txt
RUN apt update && apt install -y python3-pip && python3 -m pip install -r /home/api/requirements.txt

COPY api/ /home/api/api/
WORKDIR /home/api/

ENTRYPOINT ["/home/api/run.sh"]
