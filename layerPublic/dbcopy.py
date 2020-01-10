import  pymysql
import time,os,traceback
db=pymysql.connect("127.0.0.0","root","123456","changshu_dbluesp",charset='utf8')
cursor = db.cursor()
hour = '00'
date='1109'
data = "NO2"+date + hour
coverageName = "NO2_20191109"
timeformat='2019-11-09 00:00:00'
timeArray = time.strptime(timeformat, "%Y-%m-%d %H:%M:%S")
timestamp=time.mktime(timeArray)
try:
    # 执行sql语句
    sql='INSERT INTO ams_wms (wmsname, url, data_time, datatype, city,create_time,workspace) VALUES ({},{},{},{},{},{},{})'.format('"'+coverageName+'"',u'"http://119.3.37.164:8090/geoserver"',timestamp,u'"no2"',u'"常熟"',int(time.time()),'"1"')
    #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    traceback.print_exc()
    db.rollback()