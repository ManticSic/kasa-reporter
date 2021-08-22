# Kasa Reporter

Small pyton program to send emeter data of kasa devices to logstash

## Build

```
$ docker build -t kasa-reporter .
```


## Run

```
$ docker run --network host --env DEVICE=ip-or-hostname --env LOGSTASH_HOST=ip-or-hostname --name kasa-reporter kasa-reporter
```

## Arguments and environment variables

Argument|Environment Variable|Type|Mandatory|Default|Description
:---|---:|---:|---:|---:|---:
`-d`, `--device`|`DEVICE`|String|Yes|n/a|Ip or hostname of the device.
`-t`, `--type`|n/a|string|No|`plug`|Type of the device. Only the type `plug` is currently supported.
`-i`, `--interval`|`INTERVAL`|Integer|No|`5`|Interval of requesting emeter data in seconds.
`--logstash-host`|`LOGSTASH_HOST`|String|Yes|n/a|Ip or hostname of the logstash server.
`--logstash-port`|`LOGSTASH_PORT`|Integer|No|`5000`|Port of the logstash server.

