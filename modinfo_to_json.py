#!/usr/bin/python

import os
import re
import json

#modpath = '/software/modules/3.2.10/x86_64-linux-ubuntu14.04/Modules/3.2.10/modulefiles'
modpath = '/software/modules/lssc0/lssc0-linux/modulefiles'
modpath_static = '/software/modules/lssc0/lssc0-linux/modulefiles'
outpath = '.'

def pywalker(path):
    retlist=[]
    for root, dirs, files in os.walk(path):
        for file_ in files:
            retlist.append(os.path.join(root, file_))

    return retlist
 
if __name__ == '__main__':
    for p in pywalker(modpath):
        m = re.search('^'+modpath+'/(.+?)/(.+?)$',p)
        if m:
            sw = m.group(1)
            ver = m.group(2)

            json_dict = {'note':'', 'tags':[], 'url':''}
            f = open(p,"r");
            file_string = f.read()
            #print file_string

            m2 = re.search('set note "(.+?)"',file_string)
            if m2:
                json_dict['note'] = m2.group(1)

            m2 = re.search('set tags "(.+?)"',file_string)
            if m2:
                json_dict['tags'] = [x.lstrip() for x in m2.group(1).split(",")]

            m2 = re.search('set url "(.+?)"',file_string)
            if m2:
                json_dict['url'] = m2.group(1)

            f.close()

            f2 = open(outpath+"/"+sw+"__"+ver+".json","w")
            f2.write(json.dumps(json_dict))
            f2.close()
