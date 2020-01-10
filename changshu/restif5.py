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

# 2019年8月12日11点35分
# 常熟市空气质量预报系统
# url=http://beijingair.sinaapp.com/data/china/sites/20190926/csv
monitorstation={'1160A':'18','1161A':'19','1162A':'20','1163A':'21','1164A':'22','1165A':'23','1166A':'24','1167A':'25','1168A':'26','1171A':'27','1192A':'28','1193A':'29','1988A':'30','1989A':'31','1993A':'32','1994A':'33','1995A':'34','1996A':'35','2008A':'36','2009A':'37'}  
# 爬取市外站点数据
def addOtherData(index,h):
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
    time.sleep(30)
    hourtime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    wpath="D:\\cs\\csv\\"+nowtime
    try:
        os.makedirs(wpath)
    except :
        pass
    if(os.path.exists(csvpath+"\\"+ntime+".csv")):
        arra=readCsv(csvpath+"\\"+ntime+".csv",wpath+"\\"+hourtime+".csv",index,h)
        time.sleep(10)
        end=time.time()
        print('Running time: %s Seconds'%(end-start))
        return arra
    else:
        # 若下载不成功，重新请求，若再不成功，写入日志
        urlretrieve(url, csvpath)
        time.sleep(30)
        if(os.path.exists(csvpath+"\\"+ntime+".csv")):
            arra=readCsv(csvpath+"\\"+ntime+".csv",wpath+"\\"+hourtime+".csv",index,h)
            time.sleep(10)
            end=time.time()
            print('Running time: %s Seconds'%(end-start))
            return arra

# 写入csv文件
def readCsv(file,outfile,index,h):
        data = pd.read_csv(file,encoding='gbk')
        header=[u'date',u'hour',u'type',u'1160A',u'1161A',u'1162A',u'1163A',u'1164A',u'1165A',u'1166A',u'1167A',u'1168A',u'1171A',u'1192A',u'1193A',u'1988A',u'1989A',u'1993A',u'1994A',u'1995A',u'1996A',u'2008A',u'2009A']
        rows=data[[u'date',u'hour',u'type',u'1160A',u'1161A',u'1162A',u'1163A',u'1164A',u'1165A',u'1166A',u'1167A',u'1168A',u'1171A',u'1192A',u'1193A',u'1988A',u'1989A',u'1993A',u'1994A',u'1995A',u'1996A',u'2008A',u'2009A']]
        rows=np.array(rows.fillna(0).values)
        list=[]
        list.append(header)
        for row in rows:
            if int(row[1])==int(h) and (row[2]==u'AQI' or row[2]==u'PM2.5' or row[2]==u'PM10' or row[2]==u'SO2' or row[2]==u'NO2'  or row[2]==u'CO'):
                list.append(row)
        for row in rows:
            if int(row[1])==int(h) and row[2]==u'O3' :
                list.append(row)
        list=np.array(list).transpose()
        out_columns=['站点编号','AQI','PM2.5','PM10','SO2','NO2','CO','O3']
        out=pd.DataFrame(list,columns=out_columns)
        out_file='F:\\beijingair\\2045.xls'
        #out.to_excel(out_file,sheet_name='Sheet1')
        saveToMys(list)
def saveToMys(list):
    for i in range(3,23):
        row=list[i]
        print(row)


def saveToMysql(list):
    db=pymysql.connect("47.97.220.210","root","hbHSK123,","newchangshudb")
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

if __name__ == '__main__':
    addOtherData(2,8)