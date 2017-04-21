#!/usr/bin/env python

from flask import Flask, render_template, jsonify, request
import sys
import os
from os import path
import serial
import io
import time
import datetime
import threading

sys.path.append(path.join(path.dirname(__file__), '..', 'sequanto-automation', 'client', 'python', 'lib'))

from sequanto.automation import Client, AutomationObject

class SerialWrapper ( io.TextIOBase ):
    def __init__ ( self, _serial ):
        io.TextIOBase.__init__ ( self )
        self.m_serial = _serial

    def readline ( self ):
        ret = ''
        while True:
            c = self.m_serial.read(1)
            if c == '\n':
                return ret
            elif c == '\r':
                continue
            else:
                ret += c

    def write ( self, _data ):
        self.m_serial.write ( _data )

#def print_obj(obj, indent = 0):
#	print '  ' * indent, obj.name, obj.type
#	for child in obj.children:
#		print_obj(child, indent + 1)
#print_obj(io_client.root)

class UpdateThread(threading.Thread):
    def __init__ ( self ):
        super(UpdateThread, self).__init__(name='Ventilator Update')

        self.set_points = [30.0,]*24
        self.on = False
        self.set_point = 30
        self.raw = -1
        self.volt = -1
        self.celcius = -1
        self.percentage = -1
    
    def run( self ):
        ser = serial.Serial('/dev/ttyACM0', 57600, timeout = 1)

        # Wait for IO board to boot
        time.sleep(5)

        io_client = Client ( SerialWrapper(ser) )

        ventilator_on = io_client.find('ventilator', 'on')
        ventilator_set_point = io_client.find('ventilator', 'set_point')
        temp_raw = io_client.find('temperature', 'raw')
        temp_volt = io_client.find('temperature', 'volt')
        temp_celcius = io_client.find('temperature', 'celcius')
        temp_percentage = io_client.find('temperature', 'percentage')

        while True:
            chour = datetime.datetime.now().time().hour
            ventilator_set_point.value = self.set_points[chour]
            
            self.on = ventilator_on.value
            self.set_point = ventilator_set_point.value
            self.raw = temp_raw.value
            self.volt = temp_volt.value
            self.celcius = temp_celcius.value
            self.percentage = temp_percentage.value
            
            time.sleep(5)

update_thread = UpdateThread()
update_thread.start()

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/raw')
def raw():
	return render_template('raw.html')

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    if request.form:
        for i in range(23):
            name = 'hour-%i' % i
            if name in request.form:
                update_thread.set_points[i] = float(request.form[name])
    return render_template('configure.html', set_points = update_thread.set_points)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/json/temp')
def json_temp():
	return jsonify(raw = update_thread.raw,
		       volt = update_thread.volt,
		       celcius = update_thread.celcius,
		       percentage = update_thread.percentage)

@app.route('/json/state')
def json_state():
    ctime = datetime.datetime.now().time()
    return jsonify(on = update_thread.on,
                   time = '%.2i:%.2i:%.2i' % (ctime.hour, ctime.minute, ctime.second),
                   set_point = update_thread.set_point,
                   celcius = update_thread.celcius)

app.run(host='0.0.0.0',port=80, threaded=True)

