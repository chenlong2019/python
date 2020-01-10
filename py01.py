# coding=utf-8
from urllib import urlretrieve
import threading
import time,glob
import os
import pandas as pd
import csv
from selenium import webdriver
import traceback
import numpy as np 
import arcpy
import os

# 2019年8月12日11点35分
# 常熟市空气质量预报系统

# 20190808
nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
filetime=time.strftime('%m%d%H',time.localtime(time.time()))
# fp = io.open("D:\\cs\\zhengli\\python3\\csair\\log\\"+nowtime+".txt", 'a', encoding='utf8')
# 爬虫数据路径
pachongshuju ="F:\\result\\orag\\"+nowtime
formatPath="F:\\result\\format\\"+nowtime
station_LonLat = 'F:\\result\\Station_LonLat.xls'
station = pd.read_excel(station_LonLat)
Lon = list(station['LON'].values)
Lat = list(station['LAT'].values)

# 打开Chrome，登陆网站
def getdriver():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": pachongshuju}
    chromeOptions.add_experimental_option("prefs", prefs)
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
    pachongshuju = "F:\\result\\orag\\"+nowtime
    formatPath = "F:\\result\\format\\"+nowtime
    arcpy.AddMessage('Do something.')
    arcpy.AddMessage('当前线程数为{}'.format(threading.activeCount()))
    pathIsexists(pachongshuju)
    pathIsexists(formatPath)
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

# 请求数据时先判断是否已经存在数据，如果不存在，则继续请求
def req():
    pathDir =  os.listdir(pachongshuju)
    path_file_number=glob.glob(pathname=pachongshuju+'\\*.xls')
    path_file_number = len(path_file_number)
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    arcpy.AddMessage(normaltime)
    if(path_file_number==0):
        arcpy.AddMessage(normaltime+":"+"正在请求数据...")
        # fp.write(normaltime+":"+"正在请求数据..."+"\r\n")
        getData(driver)
        # fp.write(normaltime+":"+"请求数据完成"+"\r\n")
    else:  
        notexist=True 
        for filedata in pathDir:
            if filedata[-4:].lower() == '.xls':
                # 判断文件已存在
                starttime=filedata[-14:-8]
                if(filetime==starttime):
                    arcpy.AddMessage(normaltime+": 已经下载数据")
                    notexist=False
                    continue
        if(notexist):
            normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            arcpy.AddMessage(normaltime+":"+"正在请求数据 "+filetime+" ...")
            getData(driver)
            arcpy.AddMessage(normaltime+":"+"请求数据 "+filetime+" 完成")
            # fp.write(normaltime+":"+"请求数据 "+filetime+" 完成"+"\r\n")

# 判断文件夹是否存在，如不存在则创建
def pathIsexists(path):
    path=path.strip()
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        arcpy.AddMessage(path+' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        arcpy.AddMessage(path+' 目录已存在')

# 提取其中数据
def changeCsv():
    pathDir =  os.listdir(pachongshuju)
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    filetime=time.strftime('%m%d%H',time.localtime(time.time()))
    arcpy.AddMessage(normaltime)
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
    # 08061100
    starttime=str(int(csvFile[-14:-8]+"00")-100)
    h=starttime[:-2][-2:]
    d=starttime[:-4][-2:]
    M=starttime[:-6][-4:]
    filename="2019-"+M+"-"+d+"_"+h
    if(os.path.exists(formatPath+"\\"+filename+".csv")):
        arcpy.AddMessage("文件 "+formatPath+"\\"+filename+".csv"+" 已经存在")
        return("文件 "+formatPath+"\\"+filename+".csv"+" 已经存在")
    inpath=pachongshuju+"\\"+u'数据查询'+csvFile
    print(inpath)
    df=pd.read_excel(inpath,encoding='gbk')
    data=df[['测点名称','日期','PM2.5(μg/m3)','PM10(μg/m3)','二氧化硫(μg/m3)','二氧化氮(μg/m3)','一氧化碳(mg/m3)','臭氧(μg/m3)']]
    rows=np.array(data.fillna(0).values)
    site=[]
    print(rows)
    for row in rows:
        st=row[1]
        st=st.replace("-", "")
        st=st.replace(" ", "")
        st=st.replace(":", "")
        st=st[4:-2]
        row[1]=int(st)
        # 08061100<row[1]<08061200
        if((row[1]>int(starttime)) and (row[1]<=(int(starttime)+100))):
            site.append(row)
    arcpy.AddMessage("正在排序...")
    site=np.array(site)
    idex=np.lexsort([-1*site[:,1]])
    orted_data = site[idex,:]
    arcpy.AddMessage("排序完成")
    result=[]
    #dateTime1 = result['日期'].values
    #state = list(result['测点名称'].values)
    #PM25 = list(result['PM2.5(μg/m3)'].values)
    dateTime1 = []
    state = []
    PM25 = []
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
        PM25.append(row[2])
    #PM10 = list(data[u'PM10(μg/m3)'].values)
    #print(type(dateTime))
    #dateTime = np.array(dateTime)
    #site = list(station['海虞子站','菱塘子站','兴福子站','福山子站','沿江子站','东南子站','琴湖子站','湖东子站','常福子站','莫城子站',
        #       '梅李子站','辛庄子站','支塘子站','沙家浜子站','董浜子站','尚湖子站','古里子站']
    site = list(station[u'站点'].values)
    PM25_list = []
    #PM10_list = []
    for j in range(len(site)):
        #station_PM10 = []
        station_PM25 = []
        k = 0
        p = 0
        PM25_TEMP = 0
        #PM10_TEMP = 0
        for i in range(len(dateTime1)):
            if state[i] == site[j] and PM25[i] != u"NaN":
                k=k+1
                PM25_TEMP = PM25_TEMP+PM25[i]
                #print(k)
                #print(PM25_TEMP)
            # if state[i] ==site[j] and PM10[i] != "NaN":
            #     p=p+1
            #     PM10_TEMP = PM10_TEMP + PM10[i]
        if k != 0:
            PM25_DATA = float(PM25_TEMP) / k
            #print(PM25_DATA)
            station_PM25 = [site[j] , PM25_DATA , Lon[j] , Lat[j]]
            PM25_list.append(station_PM25)
        # if p != 0:
        #     PM10_DATA = float(PM10_TEMP) / p
        #     print(PM10_DATA)
        #     station_PM10 = [site[j] , PM10_DATA , Lon[j] , Lat[j]]
        #     PM10_list.append(station_PM10)
        else:
        #    PM25_list.append("")
            arcpy.AddMessage('PM25为空值')
    out_data = np.array(PM25_list)
    out_columns = [u'站点 ',u'PM25' ,u'Long',u'Lat']
    #out_data = np.append(out_data,ExtIndex)
    #out_data = pd.DataFrame(data = outdata_dict)
    out_data = pd.DataFrame(out_data,columns=out_columns)
    arcpy.AddMessage(out_data)
    # columns that can be converted to number(int,float) types will be converted,
    # while columns that cannot (for example, they contain non-digital strings or dates) will be retained separately.
    out_data = out_data.apply(pd.to_numeric, errors= "ignore")
    # export excel
    outname = filename.split('.')[0]+'.xls'
    arcpy.AddMessage(outname)
    out_file = os.path.join(formatPath,outname)
    arcpy.AddMessage(out_file)
    out_data.to_excel(out_file,sheet_name='Sheet1')   
    normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    arcpy.AddMessage(normaltime+":"+outname+".csv  创建成功")

#   获取请求数据
def getData(driver):
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
    time.sleep(1)
    fra.click()
    time.sleep(1)
    rdt0=driver.find_element_by_id("radlDataType_0")
    rdt0.click()
    time.sleep(1)
    btnSearch=driver.find_element_by_id("btnSearch")
    btnSearch.click()
    time.sleep(3)
    rtbWrap=driver.find_element_by_class_name("rtbWrap")
    rtbWrap.click()
    arcpy.AddMessage("线程休眠30秒")
    time.sleep(30)

if __name__ == '__main__':
    try:
        func1()
    except:
        traceback.print_exc()

