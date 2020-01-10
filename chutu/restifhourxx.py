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

# 2019年8月12日11点35分
# 常熟市空气质量预报系统
# 20190808
houtime='092708'
nowtime=''
filetime=''
# fp = io.open("D:\\cs\\zhengli\\python3\\csair\\log\\"+nowtime+".txt", 'a', encoding='utf8')
# 爬虫数据路径
pachongshuju =''
formatPath=''
station_LonLat = 'F:\\result\\Station.xls'
station = pd.read_excel(station_LonLat)
Lon = list(station['LON'].values)
Lat = list(station['LAT'].values)
inpath=''
outLayerPath = ''
outGDBPath = ''
outdBASEPath = ''
outShpPath = ''
outRasterPath = ''
fo=None
# Extent = "120.232 32.042 121.424 31.09"
Extent = "112.825200 34.718700 115.474722 36.212600"
#gdbName = "2019"+data+".gbd"
out_gdb = ''
dirfile = ["lyr","dbf","shp","tif","ran"]
#'PM2.5(μg/m3)','PM10(μg/m3)','二氧化硫(μg/m3)','二氧化氮(μg/m3)','一氧化碳(mg/m3)','臭氧(μg/m3)'
columnname=["PM25","PM10","SO2","NO2","CO","VOC"]
# 常熟市范围数据
inMaskData = "F:\\result\\changshu\\cs.shp"
outgdb=None
# Check out the ArcGIS Geostatistical Analyst extension license
arcpy.CheckOutExtension("GeoStats")
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")

# 创建目录
def createcontent(nowtime):
    nime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    # fp = io.open("D:\\cs\\zhengli\\python3\\csair\\log\\"+nowtime+".txt", 'a', encoding='utf8')
    # 爬虫数据路径
    global pachongshuju,formatPath,inpath,outLayerPath,outLayerPath,outGDBPath,outdBASEPath,outShpPath,outRasterPath,out_gdb,outgdb,ranPath,fo
    pachongshuju ="F:\\pm2511\\ddd\\nime\\orag\\"+nowtime
    formatPath="F:\\pm2511\\ddd\\nime\\out\\"+nowtime
    inpath="F:\\pm2511\\ddd\\nime\\soiybj\\"+nowtime
    outLayerPath = os.path.join(inpath,"lyr")
    outGDBPath = inpath
    outdBASEPath = os.path.join(inpath,"dbf")
    outShpPath = os.path.join(inpath,"shp")
    outRasterPath = os.path.join(inpath,"tif")
    ranPath=os.path.join(inpath,"ran")
    #gdbName = "2019"+data+".gbd"
    out_gdb = os.path.join(outGDBPath,nowtime+".gdb")
    for i in range(len(dirfile)):
        dirPath = os.path.join(inpath , dirfile[i])
        #isExists = os.path.exists(dirPath)
        try:
            os.makedirs(pachongshuju)
        except:
            print (pachongshuju + " is existing")
        try:
            os.makedirs(formatPath)
        except:
            print (formatPath + " is existing")
        try:
            os.makedirs(dirPath)
            print (dirfile[i] + " successfully created")
        except:
            print (dirfile[i] + " is existing")
    try:
        fo = open(inpath+"\\"+"log.txt", "a")
    except:
        arcpy.AddMessage(normaltime+":"+"日志文件创建失败")
    try:
        outgdb = arcpy.CreateFileGDB_management(outGDBPath, nowtime+".gdb")
    except:
        print ("{} is existing".format(out_gdb))
    
def EBK_ga(out_file,zField,h,date):
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    arcpy.AddMessage(normaltime+":"+out_file+"正在进行经验贝叶斯克里金插值...")
    outTableName = arcpy.ValidateTableName(os.path.basename(out_file.strip(".xls")),out_gdb)
    print (outTableName)
    outTable = os.path.join(out_gdb,outTableName)
    print('Converting sheet1 to {}'.format( outTable))
    # Perform the conversion
    dbfTable = os.path.join(outdBASEPath, outTableName + '.dbf')
    try:
        arcpy.ExcelToTable_conversion(out_file, outTable, "Sheet1") # Excel to Table
        arcpy.TableToDBASE_conversion(outTable, outdBASEPath)  #Table to dbf
    except Exception as err:
        print ("{} is existing".format(dbfTable))
        arcpy.AddMessage(err.message)
    # dbaseTableName = filename.strip(".xls")
    # print (dbaseTableName)
    # outTable = os.path.join(outgdb, dbaseTableName)
    # print (outTable)
    # arcpy.ExcelToTable_conversion(xlsTable, outTable, "Sheet1")
    x_coords = 'Long'   #list(date[u'Long'].head())
    y_coords = 'Lat'  #list(date[u'Lat'].values)
    outLayerName =  outTableName + '.lyr'
    outLayer = os.path.join(outLayerPath ,outLayerName)
    spRef = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"
    try:
        arcpy.MakeXYEventLayer_management(dbfTable , x_coords, y_coords, outLayerName, spRef)
    except Exception as err:
        arcpy.AddMessage("MakeXYEventLayer_management: "+outLayerName+" created Failed")
        arcpy.AddMessage(err.message)
    try:
        arcpy.SaveToLayerFile_management(outLayerName,outLayer)
    except Exception as err:
        arcpy.AddMessage("SaveToLayerFile_management: "+outLayer+" created Failed")
        arcpy.AddMessage(err.message)
    try:
        #lyr to shp
        arcpy.FeatureClassToShapefile_conversion(outLayer, outShpPath)
    except Exception as err:
        arcpy.AddMessage("FeatureClassToShapefile_conversion: "+outShpPath+" created Failed")
        arcpy.AddMessage(err.message)
    # Set local variables
    inPointFeatures = os.path.join(outShpPath , outTableName + '_lyr.shp')
    Output_geostatistical_layer = ""
    outRasNa =  outTableName + '.tif'
    nt=time.strftime('%Y%m%d',time.localtime(time.time()))
    dt=time.strftime('%m%d%H',time.localtime(time.time()))
    outFilePath="F:\\PM25\\0921\\201909"+date+"\\PM25"+getHourPath(date,h)+"\\"+zField+"\\"+"tif"
    try:
        os.makedirs(outFilePath)
    except:
        print ("")
    outRaster = os.path.join(outFilePath , outRasNa)
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
    quantileValue = ""
    thresholdType = ""
    probabilityThreshold = ""
    semivariogram = "POWER"
    tempEnvironment0 = arcpy.env.extent
    arcpy.env.extent = Extent
    # Execute EmpiricalBayesianKriging
    start =time.time()
    try:
        arcpy.EmpiricalBayesianKriging_ga(inPointFeatures, zField, Output_geostatistical_layer ,outRaster,
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
    print('09'+date+ho)
    return '09'+date+ho

if __name__ == '__main__':
    # http://222.92.166.238:9000/EQMSPortalCS/Portal/Login.aspx
    # url="http://beijingair.sinaapp.com/data/china/sites/20191010/csv"
    for i in range(16,17):
        arcpy.AddMessage('----------------- Hello World ----------------')
        h= ho=str(i) if (i>9) else '0'+str(i)
        out_file='F:\\xinxiang\\0921\\PM25\\PM25_21'+h+'.xls'#'F:\\xiaou\\zhenli\\PM25_092905.xls'
        zField='PM25'
        arcpy.AddMessage('----------------- '+h+' ----------------')
        try:
            createcontent(getHourPath(h,"21"))
            EBK_ga(out_file,zField,h,"21")
        except:
            traceback.print_exc()
    '''for i in range(11,16):
        print('------------------ Hello World ------------------------')
        date=str(i)
        arcpy.AddMessage('----------------- '+date+' ----------------')
        h='00'
        out_file='F:\\eightdata\\O3\\10'+date+'\\O3_'+h+'.xls'#'F:\\xiaou\\zhenli\\PM25_092905.xls'
        zField='O3'
        arcpy.AddMessage('----------------- '+h+' ----------------')
        try:
            createcontent(getHourPath(date,h))
            EBK_ga(out_file,zField,h,date)
        except:
            traceback.print_exc()
        arcpy.AddMessage('----------------- Hello World ----------------')
        h='05'
        out_file='F:\\eightdata\\O3\\10'+date+'\\O3_'+h+'.xls'#'F:\\xiaou\\zhenli\\PM25_092905.xls'
        zField='O3'
        arcpy.AddMessage('----------------- '+h+' ----------------')
        try:
            createcontent(getHourPath(date,h))
            EBK_ga(out_file,zField,h,date)
        except:
            traceback.print_exc()

        h='10'
        out_file='F:\\eightdata\\O3\\10'+date+'\\O3_'+h+'.xls'#'F:\\xiaou\\zhenli\\PM25_092905.xls'
        zField='O3'
        arcpy.AddMessage('----------------- '+h+' ----------------')
        try:
            createcontent(getHourPath(date,h))
            EBK_ga(out_file,zField,h,date)
        except:
            traceback.print_exc()

        h='15'
        out_file='F:\\eightdata\\O3\\10'+date+'\\O3_'+h+'.xls'#'F:\\xiaou\\zhenli\\PM25_092905.xls'
        zField='O3'
        arcpy.AddMessage('----------------- '+h+' ----------------')
        try:
            createcontent(getHourPath(date,h))
            EBK_ga(out_file,zField,h,date)
        except:
            traceback.print_exc()

        h='21'
        out_file='F:\\eightdata\\O3\\10'+date+'\\O3_'+h+'.xls'#'F:\\xiaou\\zhenli\\PM25_092905.xls'
        zField='O3'
        arcpy.AddMessage('----------------- '+h+' ----------------')
        try:
            createcontent(getHourPath(date,h))
            EBK_ga(out_file,zField,h,date)
        except:
            traceback.print_exc()'''
