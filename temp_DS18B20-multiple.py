#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:32:13 2015
@author: bling
"""

import os, glob, time
import serial
 
os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
device_folder = glob.glob(base_dir + '28*')
device_files = []
for i in device_folder:
    device_file = i + '/w1_slave'
    device_files.append(device_file)
    

transmit = 'OFF' # ON,OFF
 
def read_temp_raw():
    lines = []
    for i in device_files:
        f = open(i, 'r')
        lines.append(f.readlines())
        f.close()
    return lines
 
def read_temp():
    temp_c = []
    #temp_f = []
    lines = read_temp_raw()
    for i in lines:
        '''while i[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw() #'''
        if i[0].strip()[-3:] != 'YES':
            continue
        equals_pos = i[1].find('t=')
        if equals_pos != -1:
            temp_string = i[1][equals_pos+2:]
            temp_c.append((float(temp_string)/1000.0+30)*100)
            #temp_f.append(float(temp_string)/1000.0 * 9.0 / 5.0 + 32.0)
    return temp_c#, temp_f
	
while True:
    #cs,fs = read_temp()
    cs = read_temp()
    '''for i in range(len(cs)):
        #print i
        print "ID:%d temp C=%f\ttemp F=%f" % (i,cs[i],fs[i])#'''
    print "temp1: %d, temp2: %d" % (cs[0],cs[1])
    print '\n'
    time.sleep(3)
'''while True:
    #print("temp C=%f\ttemp F=%f" % read_temp())
    # Send data every 10 minutes.
    time.sleep(300)
    
    mes = "%.6d0%.6d" % read_temp()
    print mes
    if transmit == 'ON':
        try:
            #ser=serial.Serial('COM16', 9600) # in Windows
            ser=serial.Serial('/dev/ttyUSB0',9600) # linux
            #print 'Open serial port.'
            # send the data
            time.sleep(1)
            ser.writelines('\n')       
            time.sleep(1)
            ser.writelines('\n')
            time.sleep(1)
            ser.writelines('yab'+'\n') # Force the given message to idle.
            time.sleep(5)
            ser.writelines('\n')
            time.sleep(1)
            ser.writelines('\n')
            time.sleep(1)
            #ser.writelines('ylb9'+meandepth+rangedepth+time_len+meantemp+sdeviatemp+'\n')
            ser.writelines('ylb90'+mes+'\n')
            #time.sleep(3)
            #print 'Sending data: '+meandepth+rangedepth+time_len+meantemp+sdeviatemp
            #print datetime.now()
            time.sleep(2) # 1100s 18 minutes        
            ser.close() # close port
            time.sleep(288)
        except:
            print 'Can not send data.'  #'''
