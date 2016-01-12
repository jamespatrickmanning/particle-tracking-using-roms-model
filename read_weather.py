import serial
import numpy as np
import datetime
import math,time

# Automatic detect USB port
try:
    ser = serial.Serial('/dev/ttyUSB0',9600,timeout=30)
except:
    ser = None
    n = 0
    while not ser:
        n=n+1
        pn = '/dev/ttyUSB%d'%n
        print 'Try connect %s'%pn
        try:
            ser = serial.Serial(pn,9600,timeout=30)
        except:
            pass
        time.sleep(1)
        if n==4:
            print 'Check the connection...'
            raise Exception('Check the connection...') #'''

weather_data = []
trans_interval = 10 #minutes, one hour is 60
transmit = 'ON' # ON, OFF
ide = ['ID','Date','Time','Wind_Speed','Wind_Direction','SigmaT',
       'Air_Temperature','Barometer_Pressure','Relative_Humidity',
       'Num_Satellite','Lattitude','Longitude','Volt']
pi = 3.141592653589793
m = 0
while True:
    #for line in ser.read():
    #ser.open()
    m = m+1
    mes = ser.readline()
    '''if not mes:
        print 'No data transmitted.'
        raise Exception('No data transmitted.') #'''
    #mes = str(mes) #.strip()
    mes = mes.split(',')
    try:
        mes[12]
    except:
        print 'No data transmitted this moment.'
    else:
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
    #if len(weather_data) == trans_interval*2 :
    if m%(trans_interval*2) == 0:
        if weather_data:
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
                U = (WS[i]*0.5144444)*math.sin(WD[i]*pi/180)
                V = (WS[i]*0.5144444)*math.cos(WD[i]*pi/180)
                WSU.append(U); WSV.append(V)
            WU = np.mean(WSU); WV = np.mean(WSV) # meter per second
            #time.sleep(20)
            #print 'WU,WV,AT,BP,RH,VT',WU,WV,AT,BP,RH,VT,mesnpt[2][-1]
            mes1 = '%.4d%.4d%.4d'%(WU*10,WV*10,AT*10)
            print 'WU,WV,AT 10-times',mes1
            del weather_data[:] #empty the list

            # Send data to satellite
            if transmit == 'ON':
                try:
                    ser1=serial.Serial('/dev/ttyUSB1',9600) # linux
                    time.sleep(1)
                    ser1.writelines('\n')
                    time.sleep(1)
                    ser1.writelines('\n')
                    time.sleep(1)
                    ser1.writelines('yab'+'\n') # Force the given
message to idle.
                    time.sleep(5)
                    ser1.writelines('\n')
                    time.sleep(1)
                    ser1.writelines('\n')
                    time.sleep(1)

#ser.writelines('ylb9'+meandepth+rangedepth+time_len+meantemp+sdeviatemp+'\n')
                    ser1.writelines('ylb9'+mes1+'\n')
                    time.sleep(2) # 1100s 18 minutes
                    ser1.close() # close port
                except:
                    print "Can't send data to satellite."
