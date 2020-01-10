# coding=utf-8
import os,zipfile
import xmlUtil
import datetime
import time,traceback
import  pymysql
def getcontent():
    for i in range(0,15):
        wmsname='QLSG_PS_50_{}'.format(i)
        timeformat='2019-11-18 16:00:00'
        timeArray = time.strptime(timeformat, "%Y-%m-%d %H:%M:%S")
        timestamp=time.mktime(timeArray)
        db=pymysql.connect("localhost","root","123456","changesmonitorsys",charset='utf8')
        cursor = db.cursor()
        try:
            # 执行sql语句
            sql='INSERT INTO ams_wms (wmsname,  data_time, datatype, city,create_time,create_by,workspace) VALUES ({},{},{},{},{},{},{})'.format('"'+wmsname+'"',timestamp,u'""',u'""',int(time.time()),0,'"cms"')
            #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
            print(sql)
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            traceback.print_exc()
            db.rollback()

if __name__ == '__main__':
    getcontent()
    
