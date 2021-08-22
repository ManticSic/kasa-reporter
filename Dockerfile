FROM python:3.7

ENV DEVICE unknown
ENV INTERVAL 5
ENV LOGSTASH_HOST unknown
ENV LOGSTASH_PORT 5000

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requierments.txt

ENTRYPOINT ["./entry.sh"]