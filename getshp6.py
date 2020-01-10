# coding=utf-8
import arcpy
import os,zipfile
from arcpy.sa import *
import xmlUtil
import datetime
import time,traceback
import shutil
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
def getcontent():
    pathDir =  os.listdir("F:\\zouhangshuju")
    for contents in pathDir:
        filepath=os.path.join("F:\\zouhangshuju",contents)
        dateDir =  os.listdir(filepath)
        for datecontents in dateDir:
            datecontent=os.path.join(filepath,datecontents)
            if os.path.isdir(datecontent):
                datastr='2019-'+datecontents[0:2]+'-'+datecontents[2:4]+'_'+datecontents[4:6]
                print datastr
                # pm25.tif文件路径
                pm25dir=os.path.join(datecontent+"\\PM25\\xls",'PM25'+datastr+'.xls')
                # voc.tif文件路径
                vocdir=os.path.join(datecontent+"\\VOC\\xls",'VOC'+datastr+'.xls')
                no2dir=os.path.join(datecontent+"\\NO2\\xls",'NO2'+datastr+'.xls')
                pm10dir=os.path.join(datecontent+"\\PM10\\xls",'PM10'+datastr+'.xls')
                codir=os.path.join(datecontent+"\\CO\\xls",'CO'+datastr+'.xls')
                so2dir=os.path.join(datecontent+"\\SO2\\xls",'SO2'+datastr+'.xls')
                try:
                    shutil.copy(pm25dir, 'F:\\xls')
                except Exception as Error:
                    print Error
                try:
                    shutil.copy(vocdir, 'F:\\xls')
                except Exception as Error:
                    print Error
                try:
                    shutil.copy(no2dir, 'F:\\xls')
                except Exception as Error:
                    print Error
                try:
                    shutil.copy(pm10dir, 'F:\\xls')
                except Exception as Error:
                    print Error
                try:
                    shutil.copy(codir, 'F:\\xls')
                except Exception as Error:
                    print Error
                try:
                    shutil.copy(so2dir, 'F:\\xls')
                except Exception as Error:
                    print Error

if __name__ == '__main__':
    try:
        getcontent()
    except Exception as Error:
        print Error
    
    
