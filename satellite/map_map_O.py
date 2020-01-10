
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 13:51:59 2019

@author: swearxu
"""

import sys
sys.path.append(r"E:\代码")

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cmaps

def sample_data(shape=(73, 145)):

    nlats, nlons = shape
    lats = np.linspace(-np.pi / 2, np.pi / 2, nlats)
    lons = np.linspace(0, 2 * np.pi, nlons)
    lons, lats = np.meshgrid(lons, lats)
    wave = 0.75 * (np.sin(2 * lats) ** 8) * np.cos(4 * lons)
    mean = 0.5 * np.cos(2 * lats) * ((np.sin(2 * lats)) ** 2 + 2)

    lats = np.rad2deg(lats)
    lons = np.rad2deg(lons)
    data = wave + mean

    return lons, lats, data

def map_map_O(lons, lats, data,name):
    fig = plt.figure(figsize=(10, 10))
    m = Basemap(np.min(lons),np.min(lats),np.max(lons),np.max(lats), projection="merc")
    CHN = 'E:\\矢量图\\PIC\\'
    m.readshapefile(CHN+'diji_bou3_4m\\diquJie_polyline', 'state',drawbounds = True, zorder=None,
                      linewidth=0.5,color='k',antialiased=1,ax=None,
                      default_encoding='utf-8')
    m.readshapefile(CHN+'shengjie_bou2_4m\\bou2_4l', 'state', drawbounds=True, zorder=None,
                      linewidth=1,color='k',antialiased=1,ax=None,
                      default_encoding='utf-8')

    #m.drawcoastlines()
    box = [np.min(lons),np.max(lons),np.min(lats),np.max(lats)]
    #box = [120.50, 121.10, 31.4, 31.90]
    x, y= m(lons, lats)   ##必须有
# =============================================================================
#     c_min = np.nanmin(data)
#     c_max = np.nanmax(data)
# =============================================================================
    c_min = 0
    c_max = 80  #设置固定的标准进行统一化出图显示
    #<span style="color:#FF0000;">lim</span> = np.arange(0,81,10)
    #cs = m.pcolormesh(x, y, data, cmap='jet', vmin=dmin, vmax=dmax)  ## contouf  pcolormesh
    #cs = plt.contourf(x, y, data, cmap=cmaps.GMT_seis_r, vmin=c_min, vmax=c_max)
    cs = m.pcolormesh(x, y, data, cmap=cmaps.NCV_jet, vmin=c_min, vmax=c_max)   # GMT_panoply   GMT_seis_r  MPL_jet  NCV_jet  matlab_jet  rainbow
    #WhBIGrYeRe   NCV_bright
    m.colorbar(cs)   
    # labels = [left,right,top,bottom]
# =============================================================================
#     m.drawmeridians(np.arange(np.min(lons), np.max(lons), 0.2), labels=[1, 0, 0, 0])
#     m.drawparallels(np.arange(np.min(lats), np.max(lats), 0.2), labels=[0, 0, 0, 1])
# =============================================================================
# =============================================================================
#     m.drawmeridians(np.arange(np.min(lons), np.max(lons), 0.2), labels=[False,True,False,True],fontsize=10)
#     m.drawparallels(np.arange(np.min(lats), np.max(lats), 0.2), labels=[True,False,False,True],fontsize=10)
# =============================================================================
    m.drawmeridians(np.arange(120.30, 121.30, 0.2), labels=[False,True,False,True],fontsize=20)
    m.drawparallels(np.arange(31.22, 32.02, 0.2), labels=[True,False,False,True],fontsize=20)    
    
    plt.title(name,fontsize=24)

    #在地图上显示点
    # x是经度，y是纬度
    #point_x, point_y = m(point_data[:,0], point_data[:,1])
    #m.plot(point_x, point_y, marker = 'D', color = 'm')

    #plt.show()

    #Outpng = path + f'{name}.png'  #输出文件
    #filename = 'D:\\no2.png'
    #plt.savefig(filename, dpi=300)
    #plt.show()
    #plt.close()

if __name__ == '__main__':

    map_map(*sample_data())
