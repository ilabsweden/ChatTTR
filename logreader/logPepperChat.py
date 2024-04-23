###########################################################
# Parser of PepperChat log files intended for use with ChatTTR
#
# Syntax:
#    python logprint.py <path to log file>
#
# Author: Erik Billing, University of Skovde
# Created: April 2024. 
# License: MIT
###########################################################

import json
import sys
from datetime import datetime

def readLog(s):
    if isinstance(s,str):
        if not s.startswith('['):
            s = '[' + s[:-2] + ']'
        s = json.loads(s)

    # lastt = None
    for i in s:
        t = datetime.strptime(i['receiving']['time'] if 'receiving' in i else i['sending']['time'],'%Y-%m-%dT%H:%M:%S.%f')
        # if lastt:
        #     d = t-lastt
        #     print('\tReplied in %.1f seconds.'%d.total_seconds())
        # else:
        #     print('Conversation started ' + str(t))
        #     pass
        # lastt = t


        if 'receiving' in i and 'choices' in i['receiving']:
            yield 'robot',i['receiving']['choices'][0]['message']['content'].strip()
        if 'sending' in i and 'input' in i['sending']:
            yield 'human',i['sending']['input'].strip()

def printLog(s):
    for agent,uterance in readLog(s):
        print('%s: %s'%('R' if agent=='robot' else 'H',uterance))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please specify log file to be printed.')
    else:
        with open(sys.argv[1]) as f:
            printLog(f.read())

