#!/usr/bin/env python3
import influxdb
import os
import subprocess as sp
import datetime

output=sp.getoutput("/software/slurm/17.11.2/lssc0-linux/bin/squeue -r -h -o %T | sort | uniq -c")
time=datetime.datetime.utcnow().isoformat("T")+"Z"

client= influxdb.InfluxDBClient('blammo.genomecenter.ucdavis.edu',8086,'','',"test")

for line in output.split('\n'):
        arr=line.split()
#       print(arr[0],arr[1])

        measurement="test_queue_"+arr[1]
        value=arr[0]

        json_body = [
        {
                "measurement": measurement,
                "tags": {
                        "cluster":"wopr"
                },
                "time": time,
                "fields": {
                        "Int_value": value,
                }
        }
]
#       print(json_body)

ret=client.write_points(json_body)
print(ret)

rs=client.query("SELECT * from test_queue_PENDING;")
points = list(rs.get_points(measurement='test_queue_PENDING'))
print(points)
#print(format(rs))

dbs = client.get_list_measurements()
print(dbs)
