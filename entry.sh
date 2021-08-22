#!/bin/bash

python3 ./main.py -d$DEVICE -i$INTERVAL --logstash-host $LOGSTASH_HOST --logstash-port $LOGSTASH_PORT
