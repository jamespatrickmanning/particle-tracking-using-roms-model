# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 10:50:18 2016

@author: bling
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:32:13 2015
@author: bling
"""

import os, glob, time
import serial,numpy
 
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
cs1 = []; cs2 = [] #celcius degree lists
send_interval = 5 # unit: minute
 
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
    
time.sleep(3)	
while True:
    #cs,fs = read_temp()
    cs = read_temp()
    print "temp1: %d, temp2: %d" % (cs[0],cs[1])
    cs1.append(cs[0]); cs2.append(cs[1])
    
    temp_inter = 60 #collect data interval, every minute
    
    if len(cs1) == send_interval:
        mes10 = numpy.mean(cs1); mes20 = numpy.mean(cs2)
        mes11 = numpy.min(cs1); mes21 = numpy.min(cs2)
        mes12 = numpy.max(cs1); mes22 = numpy.max(cs2)

        mes10 = str(int(mes10)); mes20 = str(int(mes20))
        mes11 = str(int(mes11)); mes21 = str(int(mes21))
        mes12 = str(int(mes12)); mes22 = str(int(mes22))
        
        mes = mes10+mes11+mes12 + mes20+mes21+mes22      
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
                ser.writelines('ylb00'+mes+'\n')
                #time.sleep(3)
                #print 'Sending data: '+meandepth+rangedepth+time_len+meantemp+sdeviatemp
                #print datetime.now()
                time.sleep(2) # 1100s 18 minutes        
                ser.close() # close port
                #time.sleep(288)
                temp_inter = temp_inter-12
            except:
                print 'Can not send data.'  #'''
    time.sleep(temp_inter)
