#!/usr/bin/python

import os
import re
import json
from glob import glob

modpath = '/software/modules/3.2.10/x86_64-linux-ubuntu14.04/Modules/3.2.10/modulefiles'
#modpath = '/software/modules/lssc0/lssc0-linux/modulefiles'
modpath_static = '/software/modules/modulefiles_static'
outpath = '.'
countfiles_path = '/data/src/joshi/module_counter'

def search_path(path,swcounts):
    swlist = []
    moddirs = [x for x in glob(path+"/*") if os.path.isdir(x)]
    moddirs.sort()

    for p in moddirs:
        modfiles = [x for x in glob(p+"/*") if os.path.isfile(x)]

        if modfiles:
            modfiles.sort()
            sw = os.path.basename(p)
            json_dict = {'description':'', 'tags':[], 'url':'', 'name':sw, 'versions':[os.path.basename(x) for x in modfiles], 'counts':[]}

            # get information from last file, i.e. latest version
            f = open(modfiles[-1],"r");
            file_string = f.read()
            #print file_string

            m2 = re.search('set note "(.+?)"',file_string)
            if m2:
                json_dict['description'] = m2.group(1)

            m2 = re.search('set tags "(.+?)"',file_string)
            if m2:
                json_dict['tags'] = [x.lstrip() for x in m2.group(1).split(",")]

            m2 = re.search('set url "(.+?)"',file_string)
            if m2:
                json_dict['url'] = m2.group(1)

            f.close()

            if sw in swcounts:
                json_dict['counts'] = swcounts[sw]

            swlist.append(json_dict)

    return swlist


if __name__ == '__main__':

    # take only last 31 days
    countfile_list = glob(countfiles_path+"/counts.*.out")
    countfile_list.sort()
    countfile_list = countfile_list[-31:]

    swcounts = {}
    for c in countfile_list:
        f = open(c,"r")
        thisday = {}
        for line in f:
            line = line.rstrip('\n')
            data = line.split('\t')
            sw = data[0]
            cnt = data[2]
            if sw in thisday:
                thisday[sw] += cnt
                print cnt
            else:
                thisday[sw] = cnt

        for sw,cnt in thisday.iteritems():
            if sw in swcounts:
                swcounts[sw].append(cnt)
            else:
                swcounts[sw]=[]

    all_swlist = search_path(modpath,swcounts) + search_path(modpath_static,swcounts)

    f2 = open(outpath+"/all_software.json","w")
    f2.write(json.dumps(all_swlist, indent=1))
    f2.close()