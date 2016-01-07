import serial
import numpy as np
import datetime
import math,time

ser = serial.Serial('/dev/ttyUSB0',9600,timeout=30)

weather_data = []
trans_interval = 2 #minutes, one hour is 60
ide = ['ID','Date','Time','Wind_Speed','Wind_Direction','SigmaT',
       'Air_Temperature','Barometer_Pressure','Relative_Humidity',
       'Num_Satellite','Lattitude','Longitude','Volt']
pi = 3.141592653589793
while True:
    #for line in ser.read():
    #ser.open()
    mes = ser.readline()
    #mes = str(mes) #.strip()
    mes = mes.split(',')
    print mes[:-1]
    #print len(mes),type(mes)
    weather_data.append(mes[:-1])
    #mesnp = np.array(weather_data)
    print len(weather_data)

    #ser.close()
    #st = datetime.datetime.strptime(weather_data[0][2],'%H:%M:%S')
    #et = datetime.datetime.strptime(weather_data[-1][2],'%H:%M:%S')
    #inter_time = et-st
    #if inter_time.seconds == trans_interval-30 : # one hour 60*60=3600
    if len(weather_data) == trans_interval*2 :
        mesnp = np.array(weather_data)
        mesnpt = mesnp.T

        AT = np.mean([float(i) for i in mesnpt[6]])
        BP = np.mean([float(i) for i in mesnpt[7]])
        RH = np.mean([float(i) for i in mesnpt[8]])
        VT = np.mean([float(i) for i in mesnpt[12]])

        WS = [float(i) for i in mesnpt[3]]
        WD = [float(i) for i in mesnpt[4]]
        WSU,WSV = [],[]
        for i in range(len(WS)):
            U = (WS[i]*0.5144444)*math.cos(WD[i]*pi/180)
            V = -(WS[i]*0.5144444)*math.sin(WD[i]*pi/180)
            WSU.append(U); WSV.append(V)
        WU = np.mean(WSU); WV = np.mean(WSV) # meter per second
        #time.sleep(20)
        print 'WU,WV,AT,BP,RH,VT',WU,WV,AT,BP,RH,VT,mesnpt[2][-1]
        #print mesnp,type(mesnp)
        del weather_data[:] #empty the list
