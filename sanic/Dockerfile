FROM python:3.7

COPY run.sh requirements.txt /home/api/
RUN pip install -r /home/api/requirements.txt

COPY api/ /home/api/api/
WORKDIR /home/api/

ENTRYPOINT ["/home/api/run.sh"]
