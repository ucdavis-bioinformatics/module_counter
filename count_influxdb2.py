#!/usr/bin/env python3
import threading
import sys
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
    with open('/data/joshi/somefile.txt', 'w') as the_file:
        the_file.write('Hello\n')


if __name__ == '__main__':
    t = threading.Thread(target=send_count, args=(sys.argv[1],sys.argv[2],sys.argv[3]))
    t.daemon = True
    t.start()
    t.join()
    print("here")
    os._exit(0)
