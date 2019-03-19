#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2019 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import json
import os
import re
import sys
import time
import urllib
import urllib.request

def getURL(url=''):
    raw = ''
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    try:
        raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
    except:
        try:
            raw = urllib.request.urlopen(req).read().strip().decode('latin-1')
        except:
            sleep = 10 # seconds
            maxsleep = 60
            while sleep <= maxsleep:
                print('Error while retrieving: %s' % (url))
                print('Retry in %s seconds...' % (sleep))
                time.sleep(sleep)
                try:
                    raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
                except:
                    pass
                sleep = sleep * 2
    return raw

def main():
    path="/data/project/wmcounter/public_html/ia"
    if os.path.exists('%s/iacounter.data.js' % path):
        f = open('%s/iacounter.data.js' % path, 'r')
        data = f.read().splitlines()
        total_old = float(data[0].split('=')[1].split(';')[0].strip())
        timestamp_old = int(data[1].split('=')[1].split(';')[0].strip())
        f.close()
    else:
        [timestamp_old, total_old] = [0, 0]
    
    print("timestamp_old =", timestamp_old, "total_old =", total_old)

    timestamp=int('%d' % time.time())*1000
    total=0.0
    raw = getURL(url='https://catalogd.archive.org/report/space.php')
    m = re.findall(r'Primaries<td>\d+<td><b>(\d+)</b>', raw)
    if m:
        total = int(m[0])*1024*1024*1024*1024
    
    print("timestamp =", timestamp, ", total =", total)
    fillrate = (total-total_old)/(timestamp-timestamp_old) # bytes per milisecond
    print("fillrate =", fillrate)
    
    if fillrate <= 0:
        sys.exit() #wait to the next update

    if total>total_old:
        output = u"""var sizeinit = %s;
var timeinit = %s;
var fillrate = %s; // bytes per milisecond""" % (total, timestamp, fillrate)
        outfile = open('%s/iacounter.data.js' % path, 'w')
        outfile.write(output)
        outfile.close()

if __name__ == '__main__':
    main()
