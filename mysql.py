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
import MySQLdb as pymysql

# 2019年8月12日11点35分
# 常熟市空气质量预报系统

# 20190808
nowtime=''
filetime=''
# fp = io.open("D:\\cs\\zhengli\\python3\\csair\\log\\"+nowtime+".txt", 'a', encoding='utf8')
# 爬虫数据路径
pachongshuju =''
formatPath=''
outgdb=None

# 打开Chrome，登陆网站
def getdriver():
    nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
    pachongshuju ="F:\\changshustate\\orag\\"+nowtime
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
        time.sleep(30)
        # 请求失败停顿30秒继续请求，若再失败，计入日志
        # fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"正在重新请求\r\n")
        arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"正在重新请求")
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
           
    end=time.time()
    arcpy.AddMessage('Running time: %s Seconds'%(end-start))

# 创建目录
def createcontent():
    nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    # fp = io.open("D:\\cs\\zhengli\\python3\\csair\\log\\"+nowtime+".txt", 'a', encoding='utf8')
    # 爬虫数据路径
    global pachongshuju,formatPath
    pachongshuju ="F:\\changshustate\\orag\\"+nowtime
    formatPath="F:\\changshustate\\out\\"+nowtime
   
    #gdbName = "2019"+data+".gbd"
   
    #isExists = os.path.exists(dirPath)
    try:
        os.makedirs(pachongshuju)
    except:
        print (pachongshuju + " is existing")
    try:
        os.makedirs(formatPath)
    except:
        print (formatPath + " is existing")
   

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
    except Exception as err:  
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+err.message)
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+"请求数据失败")
        arcpy.AddMessage("30秒后重新请求")
        time.sleep(30)
        arcpy.AddMessage("正在重新请求...")
        try:
            getData(driver)
            normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            arcpy.AddMessage("线程休眠30秒")
            time.sleep(30)
            arcpy.AddMessage(normaltime+":"+"请求数据完成")
        except:   
            normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            arcpy.AddMessage(normaltime+":"+"请求数据失败")

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
    data=df[['测点名称','日期','PM2.5(μg/m3)','PM10(μg/m3)','二氧化硫(μg/m3)','二氧化氮(μg/m3)','一氧化碳(mg/m3)','臭氧(μg/m3)','温度(℃)','湿度(%)','风速(m/s)','风向(度)','气压(hPa)']]
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
        if((row[1]>(int(starttime)-100)) and (row[1]<=(int(starttime)))):
            site.append(row)
    arcpy.AddMessage("正在排序...")
    site=np.array(site)
    idex=np.lexsort([-1*site[:,1]])
    orted_data = site[idex,:]
    arcpy.AddMessage(orted_data)
    db=pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu")
    cursor = db.cursor()
    for row in orted_data:
        try:
            # 执行sql语句
            sql='INSERT INTO newchangshu.ams_sixindex (siteid, pubdate, aqi, pm25, pm10, so2, no2, co, o3, hcho, temperature, humidity, windspeed, winddirection, pressure) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})'.format(1, 1, 1564123930, 60.00, 1.20, 1.30, 0.52, 0.98, 0.45, 1.25, 1.24, 36.50, 77, 5.60, 332.00, 23.20)
            #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
            db.close()


#   获取请求数据
def getData(driver):
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    arcpy.AddMessage(normaltime+":"+"正在请求数据...")
    #wait = new WebDriverWait(driver,10)
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