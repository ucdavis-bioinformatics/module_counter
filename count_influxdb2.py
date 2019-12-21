#!/usr/bin/python3

import sys
#print(sys.path)
# hack for anaconda issues when running script
try:
    sys.path.remove('/software/anaconda2/4.5.12/lssc0-linux/lib/python2.7/site-packages')
    sys.path.remove('/software/anaconda3/4.5.12/lssc0-linux/lib/python3.7/site-packages')
    sys.path.remove('/software/anaconda3/4.5.12/lssc0-linux/lib/python3.6/site-packages')
except ValueError:
    pass


import threading
import time
import os

def send_count(sw_name,sw_version,user):
    import influxdb
    client = influxdb.InfluxDBClient('blammo.genomecenter.ucdavis.edu',8086,'','',"test")

    json_body = [
        {
                "measurement": "module_counts",
                "tags": {
                        "cluster":"LSSC0"
                },
                "fields": {
                        "sw_name":sw_name,
                        "sw_version":sw_version,
                        "user":user
                }
        }
    ]
    #       print(json_body)

    client.write_points(json_body)
    #time.sleep(10)
    #with open('/data/joshi/somefile.txt', 'w') as the_file:
    #    the_file.write('Hello\n')


if __name__ == '__main__':
    #print(sys.argv[1])
    #print(sys.argv[2])
    #print(sys.argv[3])
    #t = threading.Thread(target=send_count, args=(sys.argv[1],sys.argv[2],sys.argv[3]))
    data = sys.argv[1].split(" ")
    t = threading.Thread(target=send_count, args=(data[0],data[1],data[2]))
    t.daemon = True
    t.start()
    t.join()
    #print("here")
    os._exit(0)
