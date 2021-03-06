FROM python:3.7

ENV FETCH_INTERVAL 5
ENV DISCOVER_INTERVAL 30
ENV LOGSTASH_HOST unknown
ENV LOGSTASH_PORT 5000

WORKDIR /usr/src/app

COPY requierments.txt .
COPY main.py .
COPY setup setup
COPY services services
COPY models models

COPY entry.sh .
RUN chmod +x entry.sh

RUN pip install --no-cache-dir -r requierments.txt

ENTRYPOINT "./entry.sh"
