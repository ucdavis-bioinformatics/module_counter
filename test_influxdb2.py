#!/usr/bin/env python3
import influxdb
import os
import datetime

client= influxdb.InfluxDBClient('blammo.genomecenter.ucdavis.edu',8086,'','',"test")

rs=client.query("SELECT * from module_counts;")
points = list(rs.get_points(measurement='module_counts'))
print(points)
#print(format(rs))

