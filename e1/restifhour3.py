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
Extent = "120.232 32.042 121.424 31.09"
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
    #nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    # fp = io.open("D:\\cs\\zhengli\\python3\\csair\\log\\"+nowtime+".txt", 'a', encoding='utf8')
    # 爬虫数据路径
    global pachongshuju,formatPath,inpath,outLayerPath,outLayerPath,outGDBPath,outdBASEPath,outShpPath,outRasterPath,out_gdb,outgdb,ranPath,fo
    pachongshuju ="F:\\201909281751\\orag\\"+nowtime
    formatPath="F:\\201909281751\\out\\"+nowtime
    inpath="F:\\201909281751\\soiybj\\"+nowtime
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

    
def EBK_ga(out_file,zField,h):
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
    outFilePath="F:\\xiaoshju\\"+nt+"\\"+getHourPath(h)+"\\"+zField+"\\"+"tif"
    try:
        os.makedirs(outFilePath)
    except:
        print ("")
    outRaster = os.path.join(outFilePath , outRasNa)
    cellSize = 0.001
    transformation = "NONE"
    maxLocalPoints = 50
    overlapFactor = 0.5
    numberSemivariograms = 100
    # Set variables for search neighborhood
    radius = 0.3
    smooth = 0.3
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
    start=time.time()
    # Execute EmpiricalBayesianKriging
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
    end=time.time()
    arcpy.AddMessage('--------------------------------Running time: %s Seconds'%(end-start))
    arcpy.env.extent = tempEnvironment0 


# 爬取市外站点数据
def addOtherData(csvpath):
    start=time.time()
    nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
    # 20190808173859
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    url="http://beijingair.sinaapp.com/data/china/sites/"+nowtime+"/csv"
    print(url)
    urlretrieve(url, csvpath)
    arcpy.AddMessage(csvpath+"下载完成")
    time.sleep(30)
    if(os.path.exists(csvpath)):
        pass
    else:
        # 若下载不成功，重新请求，若再不成功，写入日志
        urlretrieve(url, csvpath)

# 写入csv文件
def readCsv(file,h):
    filename=os.path.split(file)[1][:-4]
    data = pd.read_csv(file,encoding='gbk')
    rows=data
    rows=np.array(rows.fillna(0).values)
    lists=[]
    for row in rows:
        # row[2]==u'AQI' or 
        if int(row[1])==int(h) and (row[2]==u'PM2.5' or row[2]==u'PM10' or row[2]==u'SO2' or row[2]==u'NO2'  or row[2]==u'CO'):
            lists.append(row)
    for row in rows:
        if int(row[1])==int(h) and row[2]==u'O3' :
            lists.append(row)
    pm25list=[]
    pm10list=[]
    so2list=[]
    no2list=[]
    colist=[]
    o3list=[]
    lists=np.array(lists).transpose()[3:42]
    site = list(station[u'站点'].values)
    for i in range(0,39):      
        if lists[i][0]>0:
            pm25_station_data = [site[i] , lists[i][0] , Lon[i] , Lat[i]]
            pm25list.append(pm25_station_data)
        else:
            arcpy.AddMessage('---------------------------'+site[i]+str(h)+'时'+'无PM2.5数据----------------------------')
        '''pm10_station_data = [site[i] , lists[i][1] , Lon[i] , Lat[i]]
        pm10list.append(pm10_station_data)
        so2_station_data = [site[i] , lists[i][2] , Lon[i] , Lat[i]]
        so2list.append(so2_station_data)
        no2_station_data = [site[i] , lists[i][3] , Lon[i] , Lat[i]]
        no2list.append(no2_station_data)
        co_station_data = [site[i] , lists[i][4] , Lon[i] , Lat[i]]
        colist.append(co_station_data)'''
        if lists[i][1]>0:
            o3_station_data = [site[i] , lists[i][1] , Lon[i] , Lat[i]]
            o3list.append(o3_station_data)
        else:
            arcpy.AddMessage('---------------------------'+site[i]+str(h)+'时'+'无O3数据----------------------------')

    vallist=[pm25list,pm10list,so2list,no2list,colist,o3list]
    collist=['PM25','PM10','SO2','NO2','CO','O3']
    out_data = np.array(vallist[0])
    column=collist[0]
    out_columns = [u'站点 ',column ,u'Long',u'Lat']
    #out_data = np.append(out_data,ExtIndex)
    #out_data = pd.DataFrame(data = outdata_dict)
    out_data = pd.DataFrame(out_data,columns=out_columns)
    # columns that can be converted to number(int,float) types will be converted,
    # while columns that cannot (for example, they contain non-digital strings or dates) will be retained separately.
    out_data = out_data.apply(pd.to_numeric, errors= "ignore")
    # export excel
    outname = column+'_'+filename+'.xls'
    nt=time.strftime('%Y%m%d',time.localtime(time.time()))
    dt=time.strftime('%m%d%H',time.localtime(time.time()))
    zouhangshuju="F:\\xiaoshju\\"+nt+"\\"+getHourPath(h)+"\\"+column+"\\"+"xls"
    try:
        os.makedirs(zouhangshuju)
    except:
        print ("")
    out_file = os.path.join(zouhangshuju,outname)
    try:
        out_data.to_excel(out_file,sheet_name='Sheet1')
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+outname+".csv  创建成功")
    except Exception as err:
        arcpy.AddMessage(out_file+" 创建失败")
        arcpy.AddMessage(out_file+" "+err.message)
        traceback.print_exc()
    if(os.path.exists(out_file)):
        EBK_ga(out_file,column,h) 
    out_data = np.array(vallist[5])
    column=collist[5]
    out_columns = [u'站点 ',column ,u'Long',u'Lat']
    #out_data = np.append(out_data,ExtIndex)
    #out_data = pd.DataFrame(data = outdata_dict)
    out_data = pd.DataFrame(out_data,columns=out_columns)
    # columns that can be converted to number(int,float) types will be converted,
    # while columns that cannot (for example, they contain non-digital strings or dates) will be retained separately.
    out_data = out_data.apply(pd.to_numeric, errors= "ignore")
    # export excel
    outname = column+'_'+filename+'.xls'
    nt=time.strftime('%Y%m%d',time.localtime(time.time()))
    dt=time.strftime('%m%d%H',time.localtime(time.time()))
    zouhangshuju="F:\\xiaoshju\\"+nt+"\\"+getHourPath(h)+"\\"+column+"\\"+"xls"
    try:
        os.makedirs(zouhangshuju)
    except:
        print ("")
    out_file = os.path.join(zouhangshuju,outname)
    try:
        out_data.to_excel(out_file,sheet_name='Sheet1')
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+outname+".csv  创建成功")
    except Exception as err:
        arcpy.AddMessage(out_file+" 创建失败")
        arcpy.AddMessage(out_file+" "+err.message)
        traceback.print_exc()
    if(os.path.exists(out_file)):
        EBK_ga(out_file,column,h)   

def getHourPath(hour):
    dt=time.strftime('%m%d',time.localtime(time.time()))
    ho=str(hour) if (hour>9) else '0'+str(hour)
    print(dt+ho)
    return dt+ho

def ExtractRange(outRaster,name):
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
    inSQLClause="VALUE > "+str(elevMAXIMUM-(elevMAXIMUM-elevMINIMUM)/5)
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
    outFileName=os.path.splitext(rasfile)[0]+".shp"
    nt=time.strftime('%Y%m%d',time.localtime(time.time()))
    dt=time.strftime('%m%d%H',time.localtime(time.time()))
    outFilePath="F:\\xiaoshju\\"+nt+"\\"+houtime+"\\"+name+"\\"+"rangle"
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
    for i in range(14,16):
        try:
            createcontent(getHourPath(i))
            filepath='F:\\xls\\china_sites_201909282242.csv'
            readCsv(filepath,i)
        except :
            pass
        
def ffff():    
    while(True):
        start=time.time()
        print '**************** Hello World *************'
        ntime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
        csvpath="D:\\cs\\csv\\all\\"+nowtime
        formattime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        filepath=csvpath+"\\"+ntime+".csv"
        print '-------------------- '+formattime+' --------------------'
        try:
            os.makedirs(csvpath)
        except :
            pass
        try:
            addOtherData(filepath)
        except :
            traceback.print_exc()
        try:
            h=int(time.strftime('%H',time.localtime(time.time())))-2
            if h<0:
                continue
            createcontent(getHourPath(h))
            readCsv(filepath,h)
            if h==21:
                createcontent(getHourPath(h+1))
                readCsv(filepath,h+1)
                createcontent(getHourPath(h+2))
                readCsv(filepath,h+2)
            
        except:
            traceback.print_exc()
        end=time.time()
        arcpy.AddMessage('Running time: %s Seconds'%(end-start))
        print ''
        time.sleep(1200)