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

# 2019年8月12日11点35分
# 常熟市空气质量预报系统
# 20190808

# Check out the ArcGIS Geostatistical Analyst extension license
arcpy.CheckOutExtension("GeoStats")
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")

def EBK_ga(inPointFeatures,outPath):
    try:
        arcpy.AddField_management(inPointFeatures, "PM102", "FLOAT", 9)
    except :
        traceback.print_exc()
    try:
        arcpy.CalculateField_management (inPointFeatures, 'PM102', "float(!PM10__μg_!)", "PYTHON_9.3")
    except :
        traceback.print_exc()
    
    name=os.path.split(inPointFeatures)[1][:-4]
    outRaster=os.path.join(outPath,name+'.tif')
    cellSize = 0.01
    transformation = "NONE"
    maxLocalPoints = 50
    overlapFactor = 0.5
    numberSemivariograms = 100
    # Set variables for search neighborhood
    radius = 1.0
    smooth = 0.14
    try:
        #lyr to shp
        searchNeighbourhood = arcpy.SearchNeighborhoodSmoothCircular(radius, smooth)
    except Exception as err:
        arcpy.AddMessage("SearchNeighborhoodSmoothCircular: "+" Failed")
        arcpy.AddMessage(err.message)
    outputType = "PREDICTION"
    Output_geostatistical_layer=''
    quantileValue = ""
    thresholdType = ""
    probabilityThreshold = ""
    semivariogram = "POWER"
    tempEnvironment0 = arcpy.env.extent
    arcpy.env.extent = Extent
    # Execute EmpiricalBayesianKriging
    start =time.time()
    try:
        arcpy.EmpiricalBayesianKriging_ga(inPointFeatures, 'PM102', Output_geostatistical_layer ,outRaster,
                                        cellSize, transformation, maxLocalPoints, overlapFactor,
                                        numberSemivariograms,
                                        searchNeighbourhood, outputType, quantileValue, thresholdType,
                                        probabilityThreshold)
        print ('Converting {} to {}'.format(inPointFeatures, outRasNa))
        arcpy.AddMessage(normaltime+":"+"经验贝叶斯克里金插值完成")       
    except Exception as err:
        arcpy.AddMessage("EmpiricalBayesianKriging_ga: "+" Failed")
        arcpy.AddMessage(err.message)
    end =time.time()
    print('Running time: %s Seconds'%(end-start))
    arcpy.env.extent = tempEnvironment0 

def getHourPath(date,hour):
    ho=str(hour) if (hour>9) else '0'+str(hour)
    print('11'+date+ho)
    return '11'+date+ho

if __name__ == '__main__':
    path=u'F:\\常熟溯源\\矢量数据21'
    pathDir =  os.listdir(path)
    for PointFeatures in pathDir:
        if PointFeatures[-4:].lower() == '.shp':
            inPointFeatures=os.path.join(path,PointFeatures)
            try:
                print('-------------- '+inPointFeatures+' -----------------------')
                EBK_ga(inPointFeatures,u'F:\\插值结果\\矢量数据21')
            except:
                traceback.print_exc()
        