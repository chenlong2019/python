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
nowtime=''
filetime=''
# fp = io.open("D:\\cs\\zhengli\\python3\\csair\\log\\"+nowtime+".txt", 'a', encoding='utf8')
# 爬虫数据路径
pachongshuju =''
formatPath=''
station_LonLat = 'F:\\result\\Station_LonLat.xls'
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
Extent = "120.5 31.4 121.1 31.9"
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

# 打开Chrome，登陆网站
def getdriver():
    nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
    pachongshuju ="F:\\resul\\orag\\"+nowtime
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,"download.default_directory": pachongshuju}
    chromeOptions.add_experimental_option("prefs", prefs)
    #chromeOptions.add_argument("headless")
    driver=webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',chrome_options=chromeOptions)
    driver.get("http://222.92.166.238:9000/EQMSPortalCS/Portal/Login.aspx")
    RadTxtUser=driver.find_element_by_id("RadTxtUser")
    RadTxtUser.clear()
    RadTxtUser.send_keys("daqi")
    RadTxtPwd=driver.find_element_by_id("RadTxtPwd")
    RadTxtPwd.clear()
    RadTxtPwd.send_keys("11111")
    ChbPwd=driver.find_element_by_id("ChbPwd")
    ChbPwd.click()
    btnOK=driver.find_element_by_id("btnOK")
    btnOK.click()
    time.sleep(5)
    return driver

driver=getdriver()

def func1():
    nowtime = time.strftime('%Y%m%d',time.localtime(time.time()))
    # fp = io.open('D:\\cs\\zhengli\\python3\\csair\\log\\'+nowtime+'.txt', 'a', encoding='utf8')
    createcontent()  
    arcpy.AddMessage('Do something.')
    arcpy.AddMessage('当前线程数为{}'.format(threading.activeCount()))
    fo.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+'当前线程数为{}'.format(threading.activeCount())+"\n")
    start=time.time()
    ntime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    # 20190808173859
    try:
        req()
        changeCsv()
    except :
        # fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据失败\r\n")
        arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据失败")
        fo.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据失败"+"\n")
        time.sleep(30)
        # 请求失败停顿30秒继续请求，若再失败，计入日志
        # fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"正在重新请求\r\n")
        arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"正在重新请求")
        fo.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"正在重新请求"+"\n")
        traceback.print_exc()
        try:
            req()
            changeCsv()
        except :
            # fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据失败\r\n")
            arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据失败")
            traceback.print_exc()
    end=time.time()
    arcpy.AddMessage('Running time: %s Seconds'%(end-start))
    # fp.write('Running time: %s Seconds'%(end-start)+"\r\n")
    global timer
    timer = threading.Timer(1200, func1)
    timer.start()

# 权宜之计
def func2():
    nowtime = time.strftime('%Y%m%d',time.localtime(time.time()))
    # fp = io.open('D:\\cs\\zhengli\\python3\\csair\\log\\'+nowtime+'.txt', 'a', encoding='utf8')
    arcpy.AddMessage('Hello World!')
    createcontent()  
    arcpy.AddMessage('当前线程数为{}'.format(threading.activeCount()))
    start=time.time()
    ntime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    # 20190808173859
    try:
        req()
        changeCsv()
    except :
        arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据未成功")
        # fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据失败\r\n")
        arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据失败")
        time.sleep(30)
        # 请求失败停顿30秒继续请求，若再失败，计入日志
        # fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"正在重新请求\r\n")
        arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"正在重新请求")
        traceback.print_exc()
        try:
            req()
            changeCsv()
        except Exception as err:
            arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"下载数据出错")
            fo.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"下载数据出错"+"\n")     
    end=time.time()
    arcpy.AddMessage('Running time: %s Seconds'%(end-start))

# 创建目录
def createcontent():
    nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    # fp = io.open("D:\\cs\\zhengli\\python3\\csair\\log\\"+nowtime+".txt", 'a', encoding='utf8')
    # 爬虫数据路径
    global pachongshuju,formatPath,inpath,outLayerPath,outLayerPath,outGDBPath,outdBASEPath,outShpPath,outRasterPath,out_gdb,outgdb,ranPath,fo
    pachongshuju ="F:\\resul\\orag\\"+nowtime
    formatPath="F:\\resul\\out\\"+nowtime
    inpath="F:\\resul\\soiybj\\"+nowtime
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

# 请求数据时先判断是否已经存在数据，如果不存在，则继续请求
def req(): 
    if(pachongshuju==''):
        return
    pathDir =  os.listdir(pachongshuju)
    path_file_number=glob.glob(pathname=pachongshuju+'\\*.xls')
    path_file_number = len(path_file_number)
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    if(path_file_number==0):
        reqStart()   
    else:  
        notexist=True 
        # 判断数据是否已经下载
        for filedata in pathDir:
            if filedata[-4:].lower() == '.xls':
                # 判断文件已存在
                starttime=filedata[-14:-8]
                if(filetime==starttime):
                    arcpy.AddMessage(normaltime+": 已经下载数据")
                    notexist=False
                    continue
        if(notexist):
            reqStart()

# 下载数据，如不成功，线程等待30秒继续下载，如再不成功，另行处理
def reqStart():
    try:
        getData(driver)
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage("线程休眠30秒")
        time.sleep(30)
        arcpy.AddMessage(normaltime+":"+"请求数据完成")
        fo.write(normaltime+":"+"请求数据完成"+"\n")
    except Exception as err:  
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+err.message)
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+"请求数据失败")
        fo.write(normaltime+":"+"请求数据失败"+"\n")
        arcpy.AddMessage("30秒后重新请求")
        time.sleep(30)
        arcpy.AddMessage("正在重新请求...")
        fo.write(normaltime+":"+"重新请求数据"+"\n")
        try:
            getData(driver)
            normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            arcpy.AddMessage("线程休眠30秒")
            time.sleep(30)
            arcpy.AddMessage(normaltime+":"+"请求数据完成")
            fo.write(normaltime+":"+"请求数据完成"+"\n")
        except:   
            normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            arcpy.AddMessage(normaltime+":"+"请求数据失败")
            fo.write(normaltime+":"+"请求数据失败"+"\n")

# 提取其中数据
def changeCsv():
    pathDir =  os.listdir(pachongshuju)
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    arcpy.AddMessage(normaltime+":"+"准备提取数据...")
    for filedata in pathDir:
        if filedata[-4:].lower() == '.xls':
            starttime=filedata[-14:-8]
            if(filetime==starttime):
                try:
                    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    arcpy.AddMessage(normaltime+":"+"正在写入csv...")
                    # fp.write(normaltime+":"+"正在写入csv.."+"\r\n")
                    getresult(filedata[-18:])
                    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    # fp.write(normaltime+":"+filedata+"写入csv完成.."+"\r\n")
                except :
                    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    traceback.print_exc()
                    arcpy.AddMessage(normaltime+":"+"写入csv失败...")
                    # fp.write(normaltime+":"+"写入csv失败..."+"\r\n")
    time.sleep(10)
    
    
# 处理提取的csv，提取信息
# D:\\cs\\aircsv\\数据查询20190806120801.xls
def getresult(csvFile):
    arcpy.AddMessage("正在提取文件"+csvFile)
    # 08150700
    starttime=str(csvFile[-14:-8]+"00")
    h=starttime[:-2][-2:]
    d=starttime[:-4][-2:]
    M=starttime[:-6][-4:]
    filename="2019-"+M+"-"+d+"_"+h
    if(os.path.exists(formatPath+"\\"+filename+".csv")):
        arcpy.AddMessage("文件 "+formatPath+"\\"+filename+".csv"+" 已经存在")
        return("文件 "+formatPath+"\\"+filename+".csv"+" 已经存在")
    inpath=pachongshuju+"\\"+u'数据查询'+csvFile
    df=pd.read_excel(inpath,encoding='gbk')
    data=df[['测点名称','日期','PM2.5(μg/m3)','PM10(μg/m3)','二氧化硫(μg/m3)','二氧化氮(μg/m3)','一氧化碳(mg/m3)','臭氧(μg/m3)']]
    rows=np.array(data.fillna(0).values)
    site=[]
    for row in rows:
        st=row[1]
        st=st.replace("-", "")
        st=st.replace(" ", "")
        st=st.replace(":", "")
        st=st[4:-2]
        row[1]=int(st)
        # 08061100<row[1]<08061200
        if((row[1]>9021200) and (row[1]<=9021300)):
            site.append(row)
    arcpy.AddMessage("正在排序...")
    site=np.array(site)
    idex=np.lexsort([-1*site[:,1]])
    orted_data = site[idex,:]
    arcpy.AddMessage("排序完成")
    for i in range(2,8):
        reserveData(orted_data,i,columnname[i-2],filename)
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+"提取数据完成")
       

def reserveData(orted_data,index,column,filename):
    #dateTime1 = result['日期'].values
    #state = list(result['测点名称'].values)
    #PM25 = list(result['PM2.5(μg/m3)'].values)
    dateTime1 = []
    state = []
    dataArray = []
    for row in orted_data:
        data=str(row[1])
        h=data[-4:][:-2]
        m=data[-4:][-2:]
        M=data[:-4][:-2]
        d=data[:-4][-2:]
        if(int(M)<10):
            M="0"+M
        date="2019-"+M+"-"+d 
        dateTime1.append(date)
        state.append(row[0])
        dataArray.append(row[index])
    #PM10 = list(data[u'PM10(μg/m3)'].values)
    #print(type(dateTime))
    #dateTime = np.array(dateTime)
    #site = list(station['海虞子站','菱塘子站','兴福子站','福山子站','沿江子站','东南子站','琴湖子站','湖东子站','常福子站','莫城子站',
        #       '梅李子站','辛庄子站','支塘子站','沙家浜子站','董浜子站','尚湖子站','古里子站']
    site = list(station[u'站点'].values)
    data_list = []
    #PM10_list = []
    for j in range(len(site)):
        #station_PM10 = []
        station_data = []
        k = 0
        p = 0
        data_TEMP = 0
        #PM10_TEMP = 0
        for i in range(len(dateTime1)):
            if state[i] == site[j] and dataArray[i] > 0:
                k=k+1
                data_TEMP = data_TEMP+dataArray[i]
                #print(k)
                #print(data_TEMP)
            # if state[i] ==site[j] and PM10[i] != "NaN":
            #     p=p+1
            #     PM10_TEMP = PM10_TEMP + PM10[i]
        if k != 0:
            data_DATA = float(data_TEMP) / k
            #print(data_DATA)
            station_data = [site[j] , data_DATA , Lon[j] , Lat[j]]
            data_list.append(station_data)
        # if p != 0:
        #     PM10_DATA = float(PM10_TEMP) / p
        #     print(PM10_DATA)
        #     station_PM10 = [site[j] , PM10_DATA , Lon[j] , Lat[j]]
        #     PM10_list.append(station_PM10)
        else:
        #    data_list.append("")
            arcpy.AddMessage(column+'为空值')
    out_data = np.array(data_list)
    out_columns = [u'站点 ',column ,u'Long',u'Lat']
    #out_data = np.append(out_data,ExtIndex)
    #out_data = pd.DataFrame(data = outdata_dict)
    out_data = pd.DataFrame(out_data,columns=out_columns)
    # columns that can be converted to number(int,float) types will be converted,
    # while columns that cannot (for example, they contain non-digital strings or dates) will be retained separately.
    out_data = out_data.apply(pd.to_numeric, errors= "ignore")
    # export excel
    outname = column+filename.split('.')[0]+'.xls'
    nt=time.strftime('%Y%m%d',time.localtime(time.time()))
    dt=time.strftime('%m%d%H',time.localtime(time.time()))
    zouhangshuju="F:\\zouhangsh\\"+nt+"\\"+dt+"\\"+column+"\\"+"xls"
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
        EBK_ga(out_file,column)
    
def EBK_ga(out_file,zField):
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
    outFilePath="F:\\zouhangsh\\"+nt+"\\"+dt+"\\"+zField+"\\"+"tif"
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
    radius = 0.14896191744041393
    smooth = 0.2
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
    arcpy.env.extent = tempEnvironment0
    if(os.path.exists(outRaster)):
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+outRaster+"开始划分污染区域范围")
        ExtractRange(outRaster,zField)   

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
    outFilePath="F:\\zouhangsh\\"+nt+"\\"+dt+"\\"+name+"\\"+"rangle"
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

#   获取请求数据
def getData(driver):
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    arcpy.AddMessage(normaltime+":"+"正在请求数据...")
    #wait = new WebDriverWait(driver,10)
    fo.write(normaltime+":"+"正在请求数据..."+"\n")
    driver.get("http://222.92.166.238:9000///EQMSPortalCS/Pages/EnvAir/RealTimeData/RealTimeData.aspx?Token=20D5D2B920F1AE58BEAC8DA83C0D948051258DC98E0CD986BC8B24EA729C6808ABA72E92B48CD4E16AC7FB9CD9FE0EEB")
    time.sleep(2)
    pra=driver.find_element_by_id("pointCbxRsm_RadCBoxPoint_Arrow")
    pra.click()
    time.sleep(1)
    prhsi=driver.find_element_by_id("pointCbxRsm_RadCBoxPoint_Header_selectAll_input")
    prhsi.click()
    pra.click()
    time.sleep(1)
    fra=driver.find_element_by_id("factorCbxRsm_RadCBoxFactor_Arrow")

    fra.click()
    time.sleep(1)
    frshi=driver.find_element_by_id("factorCbxRsm_RadCBoxFactor_Header_selectAll_input")
    frshi.click()
    time.sleep(3)
    fra.click()
    try:
        st=time.time()
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, "radlDataType_0")))
        et=time.time()
        arcpy.AddMessage('Running time: %s Seconds'%(et-st))
    except:
        traceback.print_exc()
    rdt0=driver.find_element_by_id("radlDataType_0")
    rdt0.click()
    time.sleep(1)
    btnSearch=driver.find_element_by_id("btnSearch")
    btnSearch.click()
    time.sleep(3)
    rtbWrap=driver.find_element_by_class_name("rtbWrap")
    rtbWrap.click()

if __name__ == '__main__':
    while(True):
        try:
            func2()
        except:
            traceback.print_exc()
        time.sleep(1200)