# coding=utf-8
from urllib.request import urlretrieve
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

# 2019年8月12日11点35分
# 常熟市空气质量预报系统
# url=http://beijingair.sinaapp.com/data/china/sites/20190926/csv
monitorstation={'1160A':'18','1161A':'19','1162A':'20','1163A':'21','1164A':'22','1165A':'23','1166A':'24','1167A':'25','1168A':'26','1171A':'27','1192A':'28','1193A':'29','1988A':'30','1989A':'31','1993A':'32','1994A':'33','1995A':'34','1996A':'35','2008A':'36','2009A':'37'}  
# 爬取市外站点数据
def addOtherData(h):
    start=time.time()
    ntime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
    # 20190808173859
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    csvpath="D:\\cs\\csv\\all\\"+nowtime
    url="http://beijingair.sinaapp.com/data/china/sites/"+nowtime+"/csv"
    print(url)
    try:
        os.makedirs(csvpath)
    except :
        pass
    urlretrieve(url, csvpath+"\\"+ntime+".csv")
    print(ntime+".csv"+"下载完成")
    time.sleep(10)
    hourtime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    wpath="F:\\cscsv\\"+nowtime
    try:
        os.makedirs(wpath)
    except :
        pass
    if(os.path.exists(csvpath+"\\"+ntime+".csv")):
        arra=readCsv(csvpath+"\\"+ntime+".csv",wpath+"\\"+hourtime+".csv",h)
        time.sleep(10)
        end=time.time()
        print('Running time: %s Seconds'%(end-start))
        return arra
    else:
        # 若下载不成功，重新请求，若再不成功，写入日志
        urlretrieve(url, csvpath)
        time.sleep(30)
        if(os.path.exists(csvpath+"\\"+ntime+".csv")):
            arra=readCsv(csvpath+"\\"+ntime+".csv",wpath+"\\"+hourtime+".csv",h)
            time.sleep(10)
            end=time.time()
            print('Running time: %s Seconds'%(end-start))
            return arra

# 写入csv文件
def readCsv(file,outfile,h):
        data = pd.read_csv(file,encoding='gbk')
        header=[u'type',u'date',u'hour',u'1160A',u'1161A',u'1162A',u'1163A',u'1164A',u'1165A',u'1166A',u'1167A',u'1168A',u'1171A',u'1192A',u'1193A',u'1988A',u'1989A',u'1993A',u'1994A',u'1995A',u'1996A',u'2008A',u'2009A']
        rows=data[[u'type',u'date',u'hour',u'1160A',u'1161A',u'1162A',u'1163A',u'1164A',u'1165A',u'1166A',u'1167A',u'1168A',u'1171A',u'1192A',u'1193A',u'1988A',u'1989A',u'1993A',u'1994A',u'1995A',u'1996A',u'2008A',u'2009A']]
        rows=np.array(rows.fillna(0).values)
        # 储存至excel
        list=[]
        # 储存至数据库
        list.append(header)
        hourlist=[]
        for i in range(0,23):
            hourlist.append(h)
        list.append(hourlist)
        for row in rows:
            tpyeval=row[0]
            if tpyeval==u'AQI' or tpyeval==u'PM2.5' or tpyeval==u'PM10' or tpyeval==u'SO2' or tpyeval==u'NO2'  or tpyeval==u'CO':
                if int(row[2])==int(h):
                    list.append(row)   
        for row in rows:
            tpyeval=row[0]
            if tpyeval==u'O3' :
                if int(row[2])==int(h):
                    list.append(row)
        list=np.array(list).transpose()[3:22]
        out_columns=['站点编号','时间','AQI','PM2.5','PM10','SO2','NO2','CO','O3']
        out=pd.DataFrame(list,columns=out_columns)
        date=str(rows[0][1])
        hour=str(str(h))
        out_file='F:\\beijingair\\'+date+'-'+hour+'.xls'
        if not os.path.exists(out_file):
            out.to_excel(out_file,sheet_name='Sheet1')
        '''timestr=date[0:4]+'-'+date[4:6]+'-'+date[6:8]+' '+hour
        timeArray = time.strptime(timestr, "%Y-%m-%d %H")
        timestamp=str(int(time.mktime(timeArray)))
        saveToMys(list,timestamp)'''

def saveToMys(list,timestamp):
    db=pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu")
    cursor = db.cursor()
    for row in list:
        try:
        # 执行sql语句
            sql='INSERT INTO ams_sixindex (siteid, pubdate, aqi, pm25, pm10, so2, no2, co, o3, hcho, temperature, humidity, windspeed, winddirection, pressure) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{})'.format( monitorstation[row[0]], timestamp, row[2], row[3], row[4], row[5], row[6], row[7], '0', row[8], 0, 0, 0,0,0)
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

if __name__ == '__main__':
    while(True):
        try:
            h=time.strftime('%H',time.localtime(time.time()))
            addOtherData(int(h)-2)
        except :
            pass
        time.sleep(1200)
    