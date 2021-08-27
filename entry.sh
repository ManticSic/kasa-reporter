#!/bin/bash

python3 ./main.py --fetch-interval $FETCH_INTERVAL --discover-interval $DISCOVER_INTERVAL --logstash-host $LOGSTASH_HOST --logstash-port $LOGSTASH_PORT
