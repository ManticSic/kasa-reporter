FROM python:3.7

ENV DEVICE unknown
ENV INTERVAL 5

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requierments.txt

ENTRYPOINT ["./entry.sh"]