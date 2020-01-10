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
import  pymysql
from tqdm import *
from selenium.webdriver.firefox.options import Options

# 2019年8月12日11点35分
# 常熟市空气质量预报系统

# 20190808
nowtime=''
filetime=''
# 爬虫数据路径
monitorstation={'海虞子站':'1','菱塘子站':'2','兴福子站':'3','福山子站':'4','沿江子站':'5','东南子站':'6','琴湖子站':'7','湖东子站':'8','常福子站':'9','莫城子站':'10','梅李子站':'11','辛庄子站':'12','支塘子站':'13','沙家浜子站':'14','董浜子站':'15','尚湖子站':'16','古里子站':'17'}

# 打开Chrome，登陆网站
def getdriver(pachongshuju):
    nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
    options = Options()
    options.add_argument('-headless') # 无头参数
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", pachongshuju)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    brower = webdriver.Firefox(firefox_options=options,firefox_profile=profile)
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



# 权宜之计
def func2(brower,pachongshuju,stoppath):
    nowtime = time.strftime('%Y%m%d',time.localtime(time.time()))
    print('Hello World!')
    createcontent(pachongshuju)  
    print('当前线程数为{}'.format(threading.activeCount()))
    start=time.time()
    ntime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    # 20190808173859
    try:
        reqStart(brower)
        changeCsv(pachongshuju,stoppath)
    except :
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据未成功")
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"请求数据失败")
        time.sleep(30)
        # 请求失败停顿30秒继续请求，若再失败，计入日志
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"正在重新请求")
        traceback.print_exc()
        try:
            reqStart(brower)
            changeCsv(pachongshuju,stoppath)
        except Exception as err:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+"下载数据出错")
            traceback.print_exc()
    end=time.time()
    print('Running time: %s Seconds'%(end-start))

# 创建目录
def createcontent(pachongshuju):
    try:
        os.makedirs(pachongshuju)
    except:
        pass

# 下载数据，如不成功，线程等待30秒继续下载，如再不成功，另行处理
def reqStart(brower):
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
def changeCsv(pachongshuju,stoppath):
    pathDir =  os.listdir(pachongshuju)
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(normaltime+":"+"准备提取数据...")
    ind=int(stoppath)
    for filedata in pathDir:
        if filedata[-4:].lower() == '.xls':
            starttime=filedata[-18:-6]
            print(starttime)
        if(ind<=int(starttime)):
            try:
                normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                getresult(filedata)
                normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # fp.write(normaltime+":"+filedata+"写入csv完成.."+"\r\n")
            except :
                normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                traceback.print_exc()
                print(normaltime+":"+"写入csv失败...")
                time.sleep(10)

# 处理提取的csv，提取信息
# D:\\cs\\aircsv\\数据查询20190806120801.xls
def getresult(csvFile):
    print("正在提取文件"+csvFile)
    # 08150700
    inpath=pachongshuju+"/"+csvFile
    df=pd.read_excel(inpath,encoding='gbk')				
    data=df[['测点名称','日期','PM2.5(μg/m3)','PM10(μg/m3)','二氧化硫(μg/m3)','二氧化氮(μg/m3)','一氧化碳(mg/m3)','臭氧(μg/m3)','温度(℃)','湿度(%)','风速(m/s)','风向(度)','气压(hPa)']]
    rows=np.array(data.fillna(0).values)
    db=pymysql.connect("127.0.0.1","changshu_dbluesp","Gy6M7CYysmRr2ShY","changshu_dbluesp")
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
    if(timemax==None):
        timemax=100
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
            dowpath=time.strftime('%Y%m%d%H',time.localtime(time.time()))
            stoppath=time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
            print(stoppath)
            pachongshuju=r"/www/stationdata2/"+dowpath
            brower=getdriver(pachongshuju)
            func2(brower,pachongshuju,stoppath)
            brower.close()
        except:
            traceback.print_exc()
        time.sleep(600)