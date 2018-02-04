# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 10:40:28 2017
Routine to particle track through ROMS's climatological fields

@author: Xiajian
Modified by JiM in Feb 2018 w/more documentation
"""
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy import  interpolate
from datetime import datetime, timedelta
URL1='current_07hind_hourly.nc'
def sh_bindata(x, y, z, xbins, ybins):
    """
    Bin irregularly spaced data on a rectangular grid.
    Xiaojian- I don't think this is used -JiM

    """
    ix=np.digitize(x,xbins)
    iy=np.digitize(y,ybins)
    xb=0.5*(xbins[:-1]+xbins[1:]) # bin x centers
    yb=0.5*(ybins[:-1]+ybins[1:]) # bin y centers
    zb_mean=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_median=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_std=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_num=np.zeros((len(xbins)-1,len(ybins)-1),dtype=int)    
    for iix in range(1,len(xbins)):
        for iiy in range(1,len(ybins)):
#            k=np.where((ix==iix) and (iy==iiy)) # wrong syntax
            k,=np.where((ix==iix) & (iy==iiy))
            zb_mean[iix-1,iiy-1]=np.mean(z[k])
            zb_median[iix-1,iiy-1]=np.median(z[k])
            zb_std[iix-1,iiy-1]=np.std(z[k])
            zb_num[iix-1,iiy-1]=len(z[k])
            
    return xb,yb,zb_mean,zb_median,zb_std,zb_num
def nearlonlat(lon,lat,lonp,latp):
    """
i=nearlonlat(lon,lat,lonp,latp)
find the closest node in the array (lon,lat) to a point (lonp,latp)
input:
lon,lat - np.arrays of the grid nodes, spherical coordinates, degrees
lonp,latp - point on a sphere
output:
i - index of the closest node
min_dist - the distance to the closest node, degrees
For coordinates on a plane use function nearxy

Vitalii Sheremet, FATE Project
"""
    cp=np.cos(latp*np.pi/180.)
# approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
# dist1=np.abs(dx)+np.abs(dy)
    
    i=np.argmin(dist2)
        
#    min_dist=np.sqrt(dist2[i])
    return i 
def rot2d(x, y, ang):
    '''rotate vectors by geometric angle'''
    xr = x*np.cos(ang) - y*np.sin(ang)
    yr = x*np.sin(ang) + y*np.cos(ang)
    return xr, yr
ds = Dataset(URL1,'r').variables   # netCDF4 version
URL='gom6-grid.nc'
ds1 = Dataset(URL,'r').variables   # netCDF4 version

st_lat=[]
st_lon=[]
latc=np.linspace(44.65,45.02,10)
lonc=np.linspace(-66.6,-65.93,10)
for aa in np.arange(len(lonc)):
    for bb in np.arange(len(latc)):
        st_lat.append(latc[bb])
        st_lon.append(lonc[aa])
        
T='1858-11-17T00:00:00Z'
time=[]
for a in np.arange(len(ds['ocean_time'])-1):
    #print ds['ocean_time'][a+1]-ds['ocean_time'][a]
    drt = datetime.strptime(T,'%Y-%m-%dT%H:%M:%SZ')+timedelta(hours=ds['ocean_time'][a]/float(3600))
    
    time.append(drt)

FN='necscoast_worldvec.dat'
CL=np.genfromtxt(FN,names=['lon','lat'])

days=15
jia=14*0

start_time=datetime(2007,7,14,0,0,0,0)
m_ps =dict(lon=[],lat=[],time=[])

end_time=start_time+timedelta(hours=days*24)
index11=np.argmin(abs(np.array(time)-start_time))
index22=np.argmin(abs(np.array(time)-end_time))

lon_u=np.hstack(ds1['lon_u'][:])
lat_u=np.hstack(ds1['lat_u'][:])
lon_v=np.hstack(ds1['lon_v'][:])
lat_v=np.hstack(ds1['lat_v'][:])
cc=[]

#########################################################
uu=[]
vv=[]
b=0
v0=np.hstack(ds['v'][index11][-1][:][:])
u0=np.hstack(ds['u'][index11][-1][:][:])
for a in np.arange(len(u0)):
    if u0[a]>100:
        u0[a]=0
for a in np.arange(len(v0)):
    if v0[a]>100:
        v0[a]=0

##########################################################33
#lat_v=la(np.hstack(ds1['lon_v'][:]),np.hstack(ds1['lat_v'][:]))

plt.figure()
plt.scatter(st_lon,st_lat,color='green')
plt.scatter(st_lon[0],st_lat[0],color='green',label='start')
roms=[]
for a in np.arange(len(st_lon)):
    print 'a',a
    for b in np.arange(index11,index11+1,1):
        v0=np.hstack(ds['v'][b][-1][:][:])
        u0=np.hstack(ds['u'][b][-1][:][:])
        index1=nearlonlat(lon_u,lat_u,st_lon[a],st_lat[a])
        index2=nearlonlat(lon_v,lat_v,st_lon[a],st_lat[a])
        print time[b]
        u, v = rot2d(u0[index1], v0[index2], ds1['angle'][0][0])
        if v>100:
            v=0
            u=0
        dx = 60*60*u; dy = 60*60*v
        nodes = dict(lon=[st_lon[a]], lat=[st_lat[a]],time=[time[b]])
        
        lon = st_lon[a] + dx/(111111*np.cos(st_lat[a]*np.pi/180))
            
        lat = st_lat[a] + dy/111111
        nodes['lon'].append(lon)
        nodes['lat'].append(lat)
        nodes['time'].append(time[b+1])
        for c in np.arange(1,index22-index11):
            print 'c',c
            v0=np.hstack(ds['v'][c+index11][-1][:][:])
            u0=np.hstack(ds['u'][c+index11][-1][:][:])
            index1=nearlonlat(lon_u,lat_u,lon,lat)
            index2=nearlonlat(lon_v,lat_v,lon,lat)
            '''
            if mask_u[index1]==1 or mask_v==1:
                break
            '''
            print time[c+index11]
            u, v = rot2d(u0[index1], v0[index2], ds1['angle'][0][0])
            if v>100:
                break
            dx = 60*60*u; dy = 60*60*v
            lon = lon + dx/(111111*np.cos(lat*np.pi/180))
            lat = lat + dy/111111
            nodes['lon'].append(lon)
            nodes['lat'].append(lat)
            nodes['time'].append(time[c+index11+1])
        roms.append(nodes)
    plt.scatter(nodes['lon'][-1],nodes['lat'][-1],color='red')
    plt.plot([st_lon[a],nodes['lon'][-1]],[st_lat[a],nodes['lat'][-1]],'y-')
    cc.append(nodes)
plt.scatter(nodes['lon'][-1],nodes['lat'][-1],color='red',label='end')
np.save('roms2007_7_14_to_7_29',roms)
plt.legend(loc='best') 
plt.plot(CL['lon'],CL['lat'],'b-',linewidth=0.5) 
plt.xlim([-69.5,-64.75])
plt.ylim([43.5,45.33])
plt.savefig('roms_2007_7_14_to_7_29',dpi=400)