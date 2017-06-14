# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 09:13:45 2017

@author: bling
"""
import sys
import datetime as dt
from matplotlib.path import Path
import netCDF4
from dateutil.parser import parse
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
from datetime import datetime, timedelta
from math import radians, cos, sin, atan, sqrt  
import numpy as np
import sys
import datetime as dt
from matplotlib.path import Path
import netCDF4
from dateutil.parser import parse
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
from datetime import datetime, timedelta
from math import radians, cos, sin, atan, sqrt  
from matplotlib.dates import date2num,num2date
def haversine(lon1, lat1, lon2, lat2): 
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """   
    #print 'lon1, lat1, lon2, lat21',lon1, lat1, lon2, lat2
    #print 'lon1, lat1, lon2, lat22',lon1, lat1, lon2, lat2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
    #print 34
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * atan(sqrt(a)/sqrt(1-a))   
    r = 6371 
    d=c * r
    #print 'd',d
    return d
def calculate_SD(dmlon,dmlat):
    '''compare the model_points and drifter point(time same as model point)
    (only can pompare one day)!!!'''
    #print modelpoints,dmlon,dmlat,drtime
    #print len(dmlon)
    
    dd=0
    
    for a in range(len(dmlon)-1):
        #print 12
        #dla=(dmlat[a+1]-dmlat[a])*111
        #dlo=(dmlon[a+1]-dmlon[a])*(111*np.cos(dmlat[a]*np.pi/180))
        #d=sqrt(dla**2+dlo**2)#Calculate the distance between two points 
        #print model_points['lon'][a][j],model_points['lat'][a][j],dmlon[a][j],dmlat[a][j],d           
        #print 'd',d
        d=haversine(dmlon[a+1],dmlat[a+1],dmlon[a],dmlat[a])
        dd=dd+d
    #print 'dd',dd
    return dd
m26=np.load('roms2004_8_03_to_8_18.npy')#'m_ps2011-2010_630.npy'
p=m26.tolist()
print len(p)
FN='necscoast_worldvec.dat'
CL=np.genfromtxt(FN,names=['lon','lat'])
plon2007=[]
plat2007=[]
for a in np.arange(len(p)):

    plon2007.append(p[a]['lon'][-1])
    plat2007.append(p[a]['lat'][-1])
    
length=60*0.009009009
latc=np.linspace(44.65,45.02,10)
lonc=np.linspace(-66.6,-65.93,10)

p1 = Path.circle(((lonc[5]+lonc[4])/2,(latc[5]+latc[4])/2),radius=length)
fig,axes=plt.subplots(1,1,figsize=(10,10))#figure()
cl=plt.Circle(((lonc[5]+lonc[4])/2,(latc[5]+latc[4])/2),length,alpha=0.2,color='red')
axes.add_patch(cl)
plt.plot(CL['lon'],CL['lat'])
plt.axis([-70,-65,42,47])
points = np.vstack((np.array(plon2007).flatten(),np.array(plat2007).flatten())).T  
        
insidep = []
        #collect the points included in Path.
for i in xrange(len(points)):
    if p1.contains_point(points[i]):
        insidep.append(points[i]) 
print '2007-5',len(insidep)