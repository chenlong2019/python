# coding=utf-8
import threading
import time,glob,xlrd
import os
import pandas as pd
import csv
from selenium import webdriver
import traceback
import numpy as np
import os.path
import pymysql
from tqdm import *
from selenium.webdriver.firefox.options import Options

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
monitorstation={'海虞子站':'1','菱塘子站':'2','兴福子站':'3','福山子站':'4','沿江子站':'5','东南子站':'6','琴湖子站':'7','湖东子站':'8','常福子站':'9','莫城子站':'10','梅李子站':'11','辛庄子站':'12','支塘子站':'13','沙家浜子站':'14','董浜子站':'15','尚湖子站':'16','古里子站':'17'}

# 打开Chrome，登陆网站
def getdriver():
    nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
    pachongshuju ="F:\\changshustate\\orag\\"+nowtime
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,"download.default_directory": pachongshuju}
    chromeOptions.add_experimental_option("prefs", prefs)
    #chromeOptions.add_argument("headless")
    options = Options()
    options.add_argument('-headless') # 无头参数
    firefox_path = r'C:\Program Files\Mozilla Firefox\geckodriver.exe'
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", r"F:\\fire")
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    brower = webdriver.Firefox(executable_path=firefox_path,firefox_options=options,firefox_profile=profile)
    brower.get("http://222.92.166.238:9000/EQMSPortalCS/Portal/Login.aspx")
    RadTxtUser=brower.find_element_by_id("RadTxtUser")
    RadTxtUser.clear()
    RadTxtUser.send_keys("daqi")
    RadTxtPwd=brower.find_element_by_id("RadTxtPwd")
    RadTxtPwd.clear()
    RadTxtPwd.send_keys("11111")
    ChbPwd=brower.find_element_by_id("ChbPwd")
    ChbPwd.click()
    btnOK=brower.find_element_by_id("btnOK")
    btnOK.click()
    time.sleep(5)
    return brower

brower=getdriver()

# 权宜之计
def func2():
    nowtime = time.strftime('%Y%m%d',time.localtime(time.time()))
    # fp = io.open('D:\\cs\\zhengli\\python3\\csair\\log\\'+nowtime+'.txt', 'a', encoding='utf8')
    print('Hello World!')
    createcontent()  
    print('当前线程数为{}'.format(threading.activeCount()))
    start=time.time()
    ntime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    # 20190808173859
    try:
        req()
        changeCsv()
    except :
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据未成功")
        # fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据失败\r\n")
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据失败")
        time.sleep(30)
        # 请求失败停顿30秒继续请求，若再失败，计入日志
        # fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"正在重新请求\r\n")
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"正在重新请求")
        traceback.print_exc()
        try:
            req()
            changeCsv()
        except Exception as err:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"下载数据出错")      
    end=time.time()
    print('Running time: %s Seconds'%(end-start))

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
        print(pachongshuju + " is existing")
    try:
        os.makedirs(formatPath)
    except:
        print(formatPath + " is existing")  

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
                    print(normaltime+": 已经下载数据")
                    notexist=False
                    continue
        if(notexist):
            reqStart()

# 下载数据，如不成功，线程等待30秒继续下载，如再不成功，另行处理
def reqStart():
    try:
        getData(brower)
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print("线程休眠30秒")
        time.sleep(30)
        print(normaltime+":"+"请求数据完成")
    except Exception as err:  
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(normaltime+":"+err.message)
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(normaltime+":"+"请求数据失败")
        print("30秒后重新请求")
        time.sleep(30)
        print("正在重新请求...")
        try:
            getData(brower)
            normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("线程休眠30秒")
            time.sleep(30)
            print(normaltime+":"+"请求数据完成")
        except:   
            normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print(normaltime+":"+"请求数据失败")

# 提取其中数据
def changeCsv():
    pathDir =  os.listdir(pachongshuju)
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    print(normaltime+":"+"准备提取数据...")
    for filedata in pathDir:
        if filedata[-4:].lower() == '.xls':
            starttime=filedata[-14:-8]
            if(filetime==starttime):
                try:
                    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    print(normaltime+":"+"正在写入csv...")
                    # fp.write(normaltime+":"+"正在写入csv.."+"\r\n")
                    getresult(filedata[-18:])
                    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    # fp.write(normaltime+":"+filedata+"写入csv完成.."+"\r\n")
                except :
                    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    traceback.print_exc()
                    print(normaltime+":"+"写入csv失败...")
                    # fp.write(normaltime+":"+"写入csv失败..."+"\r\n")
    time.sleep(10)
    
# 处理提取的csv，提取信息
# D:\\cs\\aircsv\\数据查询20190806120801.xls
def getresult(csvFile):
    print("正在提取文件"+csvFile)
    # 08150700
    inpath=pachongshuju+"\\"+u'数据查询'+csvFile
    df=pd.read_excel(inpath,encoding='gbk')				
    data=df[['测点名称','日期','PM2.5(μg/m3)','PM10(μg/m3)','二氧化硫(μg/m3)','二氧化氮(μg/m3)','一氧化碳(mg/m3)','臭氧(μg/m3)','温度(℃)','湿度(%)','风速(m/s)','风向(度)','气压(hPa)']]
    rows=np.array(data.fillna(0).values)
    db=pymysql.connect("112.114.191.161","newcahngshu","slkj1234,","newchangshu")
    cursor = db.cursor()
    timemax=0
    try:
        # 执行SQL语句
        maxsql='SELECT MAX(six.pubdate) AS pubdate FROM ams_sixindex six'
        print("execute start")
        cursor.execute(maxsql)
        print("execute end")
        # 获取所有记录列表
        results = cursor.fetchall()
        timemax=results[0][0]
    except:
        print ("Error: unable to fetch data")
        return "Error"
    if(timemax==0):
        return
    with tqdm(rows, ncols=90) as t:
        for row in t:
            timeArray = time.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            timestamp=time.mktime(timeArray)
            if(timestamp >timemax):
                try:
                # 执行sql语句
                    sql='INSERT INTO ams_sixindex (siteid, pubdate, aqi, pm25, pm10, so2, no2, co, o3, hcho, temperature, humidity, windspeed, winddirection, pressure) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{})'.format( monitorstation[row[0]], timestamp, '0', row[2], row[3], row[4], row[5], row[6], row[7], '0', row[8], row[9], row[10], row[11],row[12])
                    #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except:
                    # 如果发生错误则回滚
                    db.rollback()
                    # 关闭数据库连接
    try:
        db.close()
    except:
        print('error')

#   获取请求数据
def getData(brower):
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(normaltime+":"+"正在请求数据...")
    #wait = new WebDriverWait(driver,10)
    brower.get("http://222.92.166.238:9000///EQMSPortalCS/Pages/EnvAir/RealTimeData/RealTimeData.aspx?Token=20D5D2B920F1AE58BEAC8DA83C0D948051258DC98E0CD986BC8B24EA729C6808ABA72E92B48CD4E16AC7FB9CD9FE0EEB")
    time.sleep(2)
    pra=brower.find_element_by_id("pointCbxRsm_RadCBoxPoint_Arrow")
    pra.click()
    time.sleep(1)
    prhsi=brower.find_element_by_id("pointCbxRsm_RadCBoxPoint_Header_selectAll_input")
    prhsi.click()
    pra.click()
    time.sleep(1)
    fra=brower.find_element_by_id("factorCbxRsm_RadCBoxFactor_Arrow")
    fra.click()
    time.sleep(1)
    frshi=brower.find_element_by_id("factorCbxRsm_RadCBoxFactor_Header_selectAll_input")
    frshi.click()
    time.sleep(3)
    fra.click()
    rdt0=brower.find_element_by_id("radlDataType_0")
    rdt0.click()
    time.sleep(1)
    btnSearch=brower.find_element_by_id("btnSearch")
    btnSearch.click()
    time.sleep(3)
    rtbWrap=brower.find_element_by_class_name("rtbWrap")
    rtbWrap.click()

if __name__ == '__main__':
    while(True):
        try:
            func2()
        except:
            traceback.print_exc()
        time.sleep(3600)