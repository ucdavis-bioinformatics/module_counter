#!/usr/bin/env python3
import influxdb
from collections import Counter

client=influxdb.InfluxDBClient('blammo.genomecenter.ucdavis.edu',8086,'','',"test")

rs=client.query("SELECT * from module_counts;")
points = list(rs.get_points(measurement='module_counts'))
#print(points)
#print(format(rs))

counts = Counter((tok['sw_name'],tok['sw_version']) for tok in points)
counts_sorted = sorted(counts.items(),key=lambda x: x[0][0].lower())

for sw in counts_sorted:
    print(sw[0][0]+"\t"+sw[0][1]+"\t"+str(sw[1]))
