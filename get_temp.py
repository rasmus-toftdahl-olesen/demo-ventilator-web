#!/usr/bin/env python

import sys
import os
from os import path
import time

sys.path.append(path.join(path.dirname(__file__), '..', 'sequanto-automation', 'client', 'python', 'lib'))

from sequanto.automation import Client, AutomationObject

def print_obj(obj, indent = 0):
    print '  ' * indent, obj.name, obj.type
    for child in obj.children:
        print_obj(child, indent + 1)
#print_obj(client.root)

client = None

while True:
    try:
        if not client:
            client = Client('/dev/ttyACM0', _log = False)
            print 'Connected, wiating 5 seconds for Arduino to boot'
            time.sleep(5)
            objs = [child for child in client.find('temperature').children]
            
        print '\t'.join([str(obj.value) for obj in objs])
        time.sleep(1)

    except:
        print 'Lost connection, trying again in 5 seconds.'
        time.sleep(5)
        client = None
