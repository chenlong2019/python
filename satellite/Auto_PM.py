# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 11:29:02 2019

@author: swearxu
"""


from map_map import *
from map_map_O import *
from spatial_kriging import *
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal,osr
from glob import glob
import pandas as pd
from scipy.interpolate import griddata
from netCDF4 import Dataset
import os
import datetime
import seaborn as sns
from scipy import stats
import cv2 as cv

starttime = datetime.datetime.now()

def file_search_glob(inpath, condition="*.nc"):
    return glob(inpath + "/**/" + condition, recursive=True)

def get_filePath_fileName_fileExt(fileUrl):
#获取文件路径， 文件名， 后缀名
    filepath, tmpfilename = os.path.split(fileUrl)
    shotname, extension = os.path.splitext(tmpfilename)
    return filepath, shotname, extension

path = r'F:\\Data_Changshu\\Auto_download\\PM2.5\\20190829\\'               #存放数据的文件路径   PM2.5
files = file_search_glob(path, u"*.nc")                                  #NC文件List   latitude  longitude  PM2.5
num = len(files)
for i in range(num):
    filepath,name, extension = get_filePath_fileName_fileExt(files[i])
    data = Dataset(files[i])
    Lat = data.variables['latitude'][:]   # 读取经纬度参数
    Lon = data.variables['longitude'][:]
    #不同污染物参数不同nc文件或者同一个文件根据情况更改
    value = data.variables['PM2.5'][:]                   #PM10        PM2.5            
    value = np.asarray(value)
    
    LonMin,LatMax,LonMax,LatMin = [Lon.min(),Lat.max(),Lon.max(),Lat.min()]
    Resolution = 0.01       #单位为度  *100约为KM级
    lon_row = np.arange(LonMin,122,Resolution)     #此处为LonMax的时候 行数少一行 为599，因此手动设置为122
    lat_row = np.arange(LatMin,LatMax,Resolution)
    [Lon_grid,Lat_grid] = np.meshgrid(lon_row,lat_row)
    np.putmask(value, value == 0, np.nan)
    map_map(Lon_grid,Lat_grid,value,name)  #显示检验
    Outpng = path +f'Ori_'+ f'{name}.png'  #输出png    
    plt.savefig(Outpng, dpi=300)

    #裁剪出目标区域
    #value[np.where(np.isnan(value))] = 0   #空值先赋值为0
    np.putmask(value, value == 0, np.nan)
    #卫星的经纬度组成点对
    pointss = [[Lon_grid[i][j],Lat_grid[i][j]] for i in range(Lat_grid.shape[0]) for j in range(Lat_grid.shape[1])]
    pointss = np.asarray(pointss)
    values = value.flatten()
    lonlatdata = np.vstack((pointss[:,0],pointss[:,1],values)).T
    nan_rows = np.where(lonlatdata[:,0] < 120.34)
    lonlatdata = np.delete(lonlatdata,nan_rows,axis=0)
    nan_rows = np.where(lonlatdata[:,0] > 121.26)
    lonlatdata = np.delete(lonlatdata,nan_rows,axis=0)
    nan_rows = np.where(lonlatdata[:,1] < 31.31)
    lonlatdata = np.delete(lonlatdata,nan_rows,axis=0)
    nan_rows = np.where(lonlatdata[:,1] > 32.01)
    lonlatdata = np.delete(lonlatdata,nan_rows,axis=0)    #lonlatdata 为目标区域的经度纬度和值三列数据
    #np.savetxt('D:\\guodegang.txt',lonlatdata)
        
    # 构建新的网格
    Resolution_target = 0.001
    LonMin1 = 120.34
    LonMax1 = 121.26
    LatMin1 = 31.31
    LatMax1 = 32.01
    lon_row1 = np.arange(LonMin1,LonMax1,Resolution_target)
    lat_row1 = np.arange(LatMin1,LatMax1,Resolution_target)
    [Lon_grid1,Lat_grid1] = np.meshgrid(lon_row1,lat_row1)
    
    nan_rows = np.where(np.isnan(lonlatdata[:,2]))
    lonlatdata_nan = np.delete(lonlatdata,nan_rows,axis=0)
    
    if len(lonlatdata_nan) < 10:      #   ==0
        continue
        
    else:      
# =============================================================================
#     grid_value_idw = spatial_kriging(lonlatdata,LonMin1,LonMax1,LatMin1,LatMax1, "LINERA_RBF", Resolution_target)
#     map_map_O(Lon_grid1,Lat_grid1,grid_value_idw,name)  #显示检验
# =============================================================================
    
        grid_value = griddata(lonlatdata_nan[:,[0,1]], lonlatdata_nan[:,2],(Lon_grid1,Lat_grid1), method='linear',
                          fill_value=np.nan, rescale=False)  #插值计算，注意边界的空值问题  linear nearest cubic
        map_map_O(Lon_grid1,Lat_grid1,grid_value,name)  #显示检验
        Outpng1 = path +f'F100jet_'+ f'{name}.png'  #输出png    
        plt.savefig(Outpng1, dpi=300)
    
# =============================================================================
#     #高斯滤波
#     grid_value = cv.GaussianBlur(grid_value, (11, 11), 0)
#     #均值滤波
#     grid_value = cv.blur(grid_value, (11,11))
#     #filter2D处理
#     kernel = np.ones((5, 5), np.float32) / 25 #此为均值滤波卷积核
#     grid_value = cv.filter2D(grid_value, -1, kernel)
# =============================================================================
    
    
       
# =============================================================================
#     #---------------站点数据处理------------------------------------------------------------------------------------------------#
#     # 读取站点数据
#     data_station = pd.read_excel(files_station[i], sheet_name=0)
#     #data_station = data_station.drop(labels=None,axis=0, index=23, columns=None, inplace=False)  # 删除第24行   
#     data_station = np.array(data_station)    
#     temp = data_station[:,[2,3,8]]     # 经度纬度 PM2.5三列值
#     data_pm25 = np.array(temp, dtype = 'float64')
#     #data_lonlat = data_station[:,[0,1]]
#     ##建立行列索引，要与卫星产品数据网格保持一致   并经纬度为边界经纬度为
#     im_xleftup=LonMin    #左上角x
#     #im_xsolution = im_geotrans[1]   #x方向分辨率
#     im_yleftup=LatMin   #左上角y
#     #im_ysolution=im_geotrans[5]   #y方向分辨率
#     num_station =len(data_pm25)
#     value_station = np.zeros(shape = (num_station,6), dtype = np.float64)
#     for j, data_row in enumerate(data_pm25):
#         data_x=data_row[0]      #每一行excel的经度
#         data_y=data_row[1]      #每一行excel的纬度
#         data_z=data_row[2]      #每一行excel的大气指标值
#         #计算站点的像元位置        
#         difference_x=abs(data_x-im_xleftup)
#         difference_y=abs(data_y-im_yleftup)
#         pixle_ynum=int(np.floor(abs(difference_x/Resolution)))
#         pixle_xnum=int(np.floor(abs(difference_y/Resolution)))
#         # 站点x  站点y  像元位置x  像元位置y  影像值  站点值
#         value_station[j,:] = [data_x,data_y,pixle_xnum,pixle_ynum ,grid_value[pixle_xnum,pixle_ynum],data_z]
#         #print(data_x,data_y,pixle_xnum,pixle_ynum ,grid_value[pixle_xnum,pixle_ynum],data_z)       
# # =============================================================================
# #     plt.plot(value_station[:,4], value_station[:,5], marker='.', linestyle='none')
# #     plt.xlabel('Satellite')
# #     plt.ylabel('Station')     
# #     print(stats.pearsonr(value_station[:,4], value_station[:,5]))   #return r and Pvalue(<0.05)显著性检验
# # =============================================================================
#     dif = value_station[:,5] - value_station[:,4]  #地面值-卫星值
#     value_dif = np.vstack((value_station[:,0], value_station[:,1], dif)).T   #return 列
#     #----差值的空间插值计算--------------------------------------------------------------------------------------------------#
#     
#     #目前暂定的为双线性插值
#     grid_value_dif = griddata(value_dif[:,[0,1]], value_dif[:,2],(Lon_grid,Lat_grid), method='linear',
#                           fill_value=np.nan, rescale=False)
#     #sns.heatmap(grid_value_dif)
#     #plt.show()
#     grid_value_dif[np.where(np.isnan(grid_value_dif))]=0   #nan赋值为0
#     fuse_value = grid_value + grid_value_dif               # 获取融合后的值
#     #sns.heatmap(fuse_value)
#     np.putmask(fuse_value, fuse_value == 0, np.nan)
#     map_map(Lon_grid,Lat_grid,fuse_value)  #显示检验
#     
# # =============================================================================
# #     #调用其他插值方法
# #     # method = "KRIGING"+"IDW"+"LINERA_RBF"   经纬度点三列数据+
# #     grid_value_dif_kriging = site_interpolation(value_dif,LonMin,LonMax,LatMin,LatMax, "KRIGING", Resolution)
# #     
# # =============================================================================
#     
#     
#     
#     #sns.heatmap(grid_value_dif_kriging)
#     #plt.show()
#     grid_value_dif[np.where(np.isnan(grid_value_dif))]=0   #nan赋值为0
#     fuse_value = grid_value + grid_value_dif               # 获取融合后的值
#     #sns.heatmap(fuse_value)
#     np.putmask(fuse_value, fuse_value == 0, np.nan)
#     map_map(Lon_grid,Lat_grid,grid_value_dif_kriging)  #显示检验
#  
#     
#     ##Return grid_value为插值后结果，Lon_grid，Lat_grid为插值后的经纬度
#     filepath,name, extension = get_filePath_fileName_fileExt(files[i])
#     Outpng = path +f'Ori_'+ f'{name}.png'  #输出png
# # =============================================================================
# #     np.putmask(grid_value, grid_value == 0, np.nan)  
# #     np.putmask(grid_value, grid_value < 0.01, np.nan)
# #     #map_map(Lon_grid,Lat_grid,grid_value,data_pm25)  #显示检验
# #     map_map(Lon_grid,Lat_grid,grid_value)  #显示检验
# # =============================================================================
#     plt.savefig(Outpng, dpi=300)
# =============================================================================
    
    
    ##输出TIF
        OutTif = path + f'{name}.tif'  #输出文件 
        # 影像分辨率
       # LonMin,LatMax,LonMax,LatMin = [Lon_grid.min(),Lat_grid.max(),Lon_grid.max(),Lat_grid.min()]
        N_Lat = len(Lat_grid1) 
        N_Lon = Lon_grid1.shape[1]
        Lon_Res = (LonMax1 - LonMin1) /(float(N_Lon)-1)
        Lat_Res = (LatMax1 - LatMin1) / (float(N_Lat)-1)
        
    # =============================================================================
    #     filepath,name, extension = get_filePath_fileName_fileExt(files[i])
    #     OutTif = path + f'{name}.tif'  #输出文件 
    #     Outpng = path + f'{name}.png'  #输出png
    # =============================================================================
        
         # 构建.tiff文件框架
        data_tif = gdal.GetDriverByName('Gtiff').Create(OutTif,N_Lon,N_Lat,1,gdal.GDT_Float32) 
    
         # 设置影像的显示范围
        geotransform = (LonMin1,Lon_Res, 0, LatMin1, 0, Lat_Res)
        data_tif.SetGeoTransform(geotransform)
    
         # 地理坐标系统信息
        srs = osr.SpatialReference() #获取地理坐标系统信息，用于选取需要的地理坐标系统
         # =============================================================================
         # print(type(srs))
         # print(srs)
         # =============================================================================
        srs.ImportFromEPSG(4326) # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]
        data_tif.SetProjection(srs.ExportToWkt()) # 给新建图层赋予投影信息
    
         # 数据写入
        data_tif.GetRasterBand(1).WriteArray(grid_value) # 将数据写入内存，此时没有写入硬盘  #Value  为值
        data_tif.FlushCache() # 将数据写入硬盘
        data_tif = None # 关闭spei_ds指针，注意必须关闭
 
     
print('Finished')     
endtime = datetime.datetime.now()
print ('Time：',endtime - starttime)    
 