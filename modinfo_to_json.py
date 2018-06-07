#!/usr/bin/python

import os
import re
import json
from glob import glob

#modpath = '/software/modules/3.2.10/x86_64-linux-ubuntu14.04/Modules/3.2.10/modulefiles'
modpath = '/software/modules/lssc0/lssc0-linux/modulefiles'
modpath_static = '/software/modules/modulefiles_static'
outpath = '.'

def search_path(path):
    swlist = []
    moddirs = [x for x in glob(path+"/*") if os.path.isdir(x)]
    moddirs.sort()

    #print moddirs

    for p in moddirs:
        
        modfiles = [x for x in glob(p+"/*") if os.path.isfile(x)]
        modfiles.sort()
        sw = os.path.basename(p)

        #print modfiles

        json_dict = {'note':'', 'tags':[], 'url':'', 'name':sw, 'versions':[os.path.basename(x) for x in modfiles]}

        # get information from last file, i.e. latest version
        if modfiles:
            f = open(modfiles[-1],"r");
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

            swlist.append(json_dict)

    return swlist


if __name__ == '__main__':
    all_swlist = search_path(modpath) + search_path(modpath_static)

    f2 = open(outpath+"/all_software.json","w")
    f2.write(json.dumps(all_swlist))
    f2.close()