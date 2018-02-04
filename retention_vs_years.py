# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:57:02 2017
This routine compares retention of particles in one area over different years 
@author: Xiaojian Liu in mid-2017
Modifications by JiM in early 2018

This routine assumes at least two other programs have run:
"roms.py" does particle tracking (JiM renamed this to "track_roms.py"
"retention_of_particles.py" calculates % retention for different times (JiM renamed this to "retention_vs_years.py"
"""
import datetime as dt
import pytz
import pandas as pd
from math import sqrt,radians,sin,cos,atan
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pytz import timezone
import numpy as np
import csv
from matplotlib.path import Path
from netCDF4 import Dataset
from scipy import  interpolate
from matplotlib.dates import date2num,num2date
t0=datetime(2004,3,31,0,0,0)
tt=[]
for a in np.arange(25):
    tt.append(t0+timedelta(days=a*5))
t=['3/31','4/5','4/10','4/15','4/20','4/25','4/30','5/5','5/10','5/15','5/20','5/25','5/30','6/4','6/9','6/14','6/19','6/24','6/29','7/4','7/9','7/14','7/19','7/24','7/29']
# the following lines have the % retention as derived from what program? How did you generate these numbers?
r2004=[77,27,53,78,100,100,100,100,98,67,66,91,95,71,57,67,88,96,79,73,76,70,59,50,41]
r2005=[96,82,81,93,95,96,61,44,41,40,61,78,89,53,82,72,94,91,62,67,81,74,61,75,73]
r2006=[88,54,44,27,58,65,38,74,77,100,86,63,67,72,99,53,47,44,47,69,75,97,85,79,86]
r2007=[99,88,73,62,100,95,76,94,74,74,92,97,34,49,62,51,32,62,72,99,82,68,84,73,58]
r2008=[99,97,94,30,48,58,2,2,21,86,80,100,83,69,63,87,100,97,90,28,63,75,85,31,7]
plt.figure(figsize=(12,4))
plt.plot(tt,r2004,'*-',label='2004')
plt.plot(tt,r2005,'*-',label='2005')
plt.plot(tt,r2006,'*-',label='2006')
plt.plot(tt,r2007,'*-',label='2007')
plt.plot(tt,r2008,'*-',label='2008')
plt.title('retention of particle')
plt.legend(loc='best')
plt.ylim([0,110])
