# Kasa Reporter

Small python program to send emeter data of kasa devices to logstash

## Build

```
$ docker build -t kasa-reporter .
```


## Run

```
$ docker run --network host --env LOGSTASH_HOST=ip-or-hostname --name kasa-reporter kasa-reporter
```

## Arguments and environment variables

Argument|Environment Variable|Type|Mandatory|Default|Description
:---|---:|---:|---:|---:|---:
`--fetch-interval`|`FETCH_INTERVAL`|Integer|No|`5`|Interval of requesting emeter data in seconds.
`--discover-interval`|`DISCOVER_INTERVAL`|Integer|No|`30`|Interval of discovering devices in network 255.255.255.255.
`--logstash-host`|`LOGSTASH_HOST`|String|Yes|n/a|Ip or hostname of the logstash server.
`--logstash-port`|`LOGSTASH_PORT`|Integer|No|`5000`|Port of the logstash server.

