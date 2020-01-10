# coding=utf-8
from urllib import urlretrieve
import threading
import time,glob,xlrd
import os
import pandas as pd
import csv
from selenium import webdriver
import traceback
import numpy as np 
import arcpy
import os.path
from arcpy import env
from arcpy.sa import *
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# 2019年9月5日11点00分

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")

def ExtractRange(outRaster, inMaskData):
    outExtractByMask=None
    attExtract=None
    '''
    try:
        # Execute ExtractByMask
     #   outExtractByMask = ExtractByMask(outRaster, inMaskData)
     except Exception as err:
        arcpy.AddMessage("ExtractByMask Failed") 
        arcpy.AddMessage(err)
        return
    '''
    #Get the geoprocessing result object
    elevMAXIMUMResult = arcpy.GetRasterProperties_management(outRaster, "MAXIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMAXIMUM = float(elevMAXIMUMResult.getOutput(0))
    elevMINIMUMResult = arcpy.GetRasterProperties_management(outRaster, "MINIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMINIMUM = float(elevMINIMUMResult.getOutput(0))
    inSQLClause="VALUE > "+str(elevMAXIMUM-(elevMAXIMUM-elevMINIMUM)/20)
    try:
        # Execute ExtractByAttributes
        attExtract = ExtractByAttributes(outRaster, inSQLClause) 
    except Exception as err:
        arcpy.AddMessage("ExtractByAttributes Failed") 
        arcpy.AddMessage(err)
        return 
    # Save the output 
    #attExtract.save("F:\\ree\\PM25T08.tif")
    rasfile=os.path.split(outRaster)[1]
    nt=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    outFileName=nt+".shp"
    dt=time.strftime('%m%d%H',time.localtime(time.time()))
    outFilePath="F:\\changshu\\result"
    try:
        os.makedirs(outFilePath)
    except:
        print ("")
    outLine = os.path.join(outFilePath , outFileName)
    field = "VALUE"
    outGeom = "LINE"
    try:
        # Execute ExtractByAttributes
        arcpy.RasterDomain_3d(attExtract, outLine, outGeom) 
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+outRaster+"污染划分完成")
    except Exception as err:
        arcpy.AddMessage(outRaster+"RasterDomain_3d Failed") 
        arcpy.AddMessage(err)
        return

def ExtractRange2(outRaster, inMaskData):
    outExtractByMask=None
    attExtract=None
    
    try:
        # Execute ExtractByMask
        outExtractByMask = ExtractByMask(outRaster, inMaskData)
    except Exception as err:
        arcpy.AddMessage("ExtractByMask Failed") 
        arcpy.AddMessage(err)
        return
    
    #Get the geoprocessing result object
    elevMAXIMUMResult = arcpy.GetRasterProperties_management(outExtractByMask, "MAXIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMAXIMUM = float(elevMAXIMUMResult.getOutput(0))
    elevMINIMUMResult = arcpy.GetRasterProperties_management(outExtractByMask, "MINIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMINIMUM = float(elevMINIMUMResult.getOutput(0))
    inSQLClause="VALUE > "+str(elevMAXIMUM-(elevMAXIMUM-elevMINIMUM)/20)
    try:
        # Execute ExtractByAttributes
        attExtract = ExtractByAttributes(outExtractByMask, inSQLClause) 
    except Exception as err:
        arcpy.AddMessage("ExtractByAttributes Failed") 
        arcpy.AddMessage(err)
        return 
    # Save the output 
    #attExtract.save("F:\\ree\\PM25T08.tif")
    rasfile=os.path.split(outRaster)[1]
    nt=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    outFileName=nt+".shp"
    dt=time.strftime('%m%d%H',time.localtime(time.time()))
    outFilePath="F:\\changshu\\result"
    try:
        os.makedirs(outFilePath)
    except:
        print ("")
    outLine = os.path.join(outFilePath , outFileName)
    field = "VALUE"
    outGeom = "LINE"
    try:
        # Execute ExtractByAttributes
        arcpy.RasterDomain_3d(attExtract, outLine, outGeom) 
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+outRaster+"污染划分完成")
    except Exception as err:
        arcpy.AddMessage(outRaster+"RasterDomain_3d Failed") 
        arcpy.AddMessage(err)
        return

if __name__ == '__main__':
    outRaster=u'F:\\changshu\\tif\\20190830mydPM25.tif'
    inMaskData='F:\\result\\changshu\\cs.shp'
    ExtractRange2(outRaster, inMaskData)