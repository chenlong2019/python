# coding=utf-8
from urllib.request import urlretrieve
import threading
import time
import os
import pandas as pd
import csv
import numpy as np

# 20190808
nowtime=time.strftime('%Y%m%d',time.localtime(time.time()))
fp = open('D:\\cs\\csv\\log\\'+nowtime+'.txt', 'w', encoding='utf8')
def func1():
    print('Do something.')
    print('当前线程数为{}'.format(threading.activeCount()))
    start=time.time()
    ntime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    # 20190808173859
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    csvpath="D:\\cs\\csv\\all\\"+nowtime
    url="http://beijingair.sinaapp.com/data/china/sites/"+nowtime+"/csv"
    print(url)
    pathIsexists(csvpath)
    urlretrieve(url, csvpath+"\\"+ntime+".csv")
    print(ntime+".csv"+"下载完成")
    time.sleep(30)
    hourtime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    wpath="D:\\cs\\csv\\"+nowtime
    pathIsexists(wpath)
    if(os.path.exists(csvpath+"\\"+ntime+".csv")):
        fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+ntime+".csv"+"下载成功"+"\r\n")
        writeToCsv(csvpath+"\\"+ntime+".csv",wpath+"\\"+hourtime+".csv")
    else:
        # 若下载不成功，重新请求，若再不成功，写入日志
        urlretrieve(url, csvpath)
        time.sleep(30)
        if(os.path.exists(csvpath+"\\"+ntime+".csv")):
            fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+ntime+".csv"+"下载成功"+"\r\n")
            writeToCsv(csvpath+"\\"+ntime+".csv",wpath+"\\"+hourtime+".csv")
        else:
            fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+":"+ntime+".csv"+"下载成功" +"\r\n")
    end=time.time()
    print('Running time: %s Seconds'%(end-start))
    global timer
    timer = threading.Timer(3600, func1)
    timer.start()

# 写入csv文件
def writeToCsv(file,outfile):
        data = pd.read_csv(file)
       
        header=['date','hour','type','1160A','1161A','1162A','1163A','1164A','1165A','1166A','1167A','1168A','1171A','1192A','1193A','1988A','1989A','1993A','1994A','1995A','1996A','2008A','2009A']
        rows=data[['date','hour','type','1160A','1161A','1162A','1163A','1164A','1165A','1166A','1167A','1168A','1171A','1192A','1193A','1988A','1989A','1993A','1994A','1995A','1996A','2008A','2009A']]
        rows=np.array(rows.fillna(0).values)
        list=[]
        list.append(header)
        for row in rows:
            if row[1]==8 and (row[2]=='AQI' or row[2]=='PM2.5' or row[2]=='PM10' or row[2]=='SO2' or row[2]=='NO2'  or row[2]=='CO'):
                list.append(row)
        for row in rows:
            if row[1]==8 and row[2]=='O3' :
                list.append(row)
        list=np.array(list).transpose()
        arra=[]
        for index in range(3,23):
            arra.append(list[index][2])
        print(arra)
        with open(outfile,"w",newline='') as csvfile: 
            writer = csv.writer(csvfile)
            #先写入columns_name
            # writer.writerow(header)
            print("正在写入。。。")
            #写入多行用writerows
            writer.writerows(list)
            print("写入完成")

# 判断文件夹是否存在，如不存在则创建
def pathIsexists(path):
    path=path.strip()
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print(path+' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')

if __name__ == '__main__':
    func1()
