# coding=utf-8
import arcpy
import os,zipfile
from arcpy.sa import *
import xmlUtil
import datetime
import time,traceback
import MySQLdb as pymysql
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
# sld文件生成
def getcontent():
    pathDir =  os.listdir("F:\st")
    satellitezippath='F:\\zip\\changshu\\satellite'
    try:
        os.makedirs(satellitezippath)
    except :
        print('')
    db=pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu",charset='utf8')
    cursor = db.cursor()
    for contents in pathDir:
        if(contents!='201909230030_PM25.tif'):
            continue
        if contents[-4:].lower() == '.tif':
            filepath=os.path.join("F:\\st",contents)
            index=filepath.index('2019')
            mon=filepath[index+4:index+6]
            day=filepath[index+6:index+8]
            date='2019-'+mon+'-'+day
            timeArray = time.strptime(date, "%Y-%m-%d")
            timestamp=int(time.mktime(timeArray))
            print(filepath)
            if os.path.exists(filepath):
                try:
                    RasterToPoint_conversion(filepath,'D:\\sld\\satellite') 
                except:
                    # 如果发生错误则回滚
                    traceback.print_exc()
                              
# 按掩模提取
def RasterToPoint_conversion(outRaster,outSLDPath):
    inMaskData="F:\\changshu\\Changshu City_AL6.shp"
    # Execute ExtractByMask
    outExtractByMask = ExtractByMask(outRaster,inMaskData)
    elevMAXIMUMResult = arcpy.GetRasterProperties_management(outExtractByMask, "MAXIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMAXIMUM = float(elevMAXIMUMResult.getOutput(0))
    elevMINIMUMResult = arcpy.GetRasterProperties_management(outExtractByMask, "MINIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMINIMUM = float(elevMINIMUMResult.getOutput(0))
    rastername=outRaster.split('\\')[-1][:-4]
    xmlUtil.createSLD(rastername,elevMAXIMUM,elevMINIMUM,outSLDPath)

if __name__ == '__main__':
    try:
        getcontent()
    except :
        pass
    
