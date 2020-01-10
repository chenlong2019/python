# coding=utf-8
import arcpy
import os,zipfile
from arcpy.sa import *
import sldUtil
import datetime
import time,traceback
import MySQLdb as pymysql
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
# sld文件生成
def getcontent():
    pathDir =  os.listdir("F:\\zouhangshuju")
    pm25slddir="D:\\sld\\cssite\\pm25"
    vocslddir="D:\\sld\\cssite\\voc"
    db=pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu",charset='utf8')
    cursor = db.cursor()
    try:
        os.makedirs(pm25slddir)
    except :
        print('')
    try:
        os.makedirs(vocslddir)
    except :
        print('')
    for contents in pathDir:
        if(int(contents)<20190923):
            print contents
            continue
        filepath=os.path.join("F:\\zouhangshuju",contents)
        dateDir =  os.listdir(filepath)
        for datecontents in dateDir:
            datecontent=os.path.join(filepath,datecontents)
            if os.path.isdir(datecontent):
                PM25='pm252019_'+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                VOC='voc2019_'+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                # pm25.tif文件路径
                pm25dir=os.path.join(datecontent+"\\PM25\\tif",PM25+'.tif')
                # voc.tif文件路径
                vocdir=os.path.join(datecontent+"\\VOC\\tif",VOC+'.tif')
                timeformat='2019'+"-"+datecontents[0:2]+"-"+datecontents[2:4]+" "+datecontents[4:6]+":"+"00"+":"+"00"
                timeArray = time.strptime(timeformat, "%Y-%m-%d %H:%M:%S")
                timestamp=time.mktime(timeArray)
                print(PM25)
                '''
                if os.path.exists(pm25dir):
                    rastername=pm25dir.split('\\')[-1][:-4]
                    sldUtil.createSLD(rastername,'D:\\sld\\cssite\\pm25')
                    #RasterToPoint_conversion(pm25dir,'D:\\sld\\cssite\\pm25')
                    '''
                if os.path.exists(vocdir):
                    rastername=vocdir.split('\\')[-1][:-4]
                    sldUtil.createSLD(rastername,'D:\\sld\\cssite\\voc')
                              
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
   

if __name__ == '__main__':
    getcontent()
    
