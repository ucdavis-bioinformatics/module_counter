#!/usr/bin/env python3
import influxdb
import os
import datetime
import sys

#time=datetime.datetime.utcnow().isoformat("T")+"Z"
client= influxdb.InfluxDBClient('blammo.genomecenter.ucdavis.edu',8086,'','',"test")

json_body = [
        {
                "measurement": "module_counts",
                "tags": {
                        "cluster":"LSSC0"
                },
                "fields": {
                        "sw_name":sys.argv[1],
                        "sw_version":sys.argv[2],
                        "user":sys.argv[3]
                }
        }
]
#       print(json_body)

client.write_points(json_body)

