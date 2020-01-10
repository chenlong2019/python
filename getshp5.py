# coding=utf-8
import arcpy
import os,zipfile
from arcpy.sa import *
import xmlUtil
import datetime
import time,traceback
import MySQLdb as pymysql
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
def getcontent():
    pathDir =  os.listdir(u"F:\\走航路线\\sdddd")
    db=pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu",charset='utf8')
    cursor = db.cursor()
    for contents in pathDir:
        filepath=os.path.join("F:\\走航路线\\sdddd",contents)
        listFiles(filepath,db)
    db.close()
def listFiles(filepath,db):
    filelist=os.listdir(filepath)
        for filename in filelist:
            kml_address="kml/"+contents+"/"+filename
            kml_type=filename[:4]
            kml_name=filename[:-4]
            date=filename[4:14]
            timeformat=date[:4]+"-"+date[4:6]+"-"+date[6:8]+" "+date[8:10]+":00:00"
            timeArray = time.strptime(timeformat, "%Y-%m-%d %H:%M:%S")
            kml_date=int(time.mktime(timeArray))
            print kml_date
            try:
                # 执行sql语句
                sql='INSERT INTO newchangshu.ams_kml (kml_name, kml_type, kml_date, kml_address) VALUES ("{}","{}","{}","{}")'.format(kml_name,kml_type,kml_date,kml_address)
                #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # 如果发生错误则回滚
                traceback.print_exc()
                db.rollback()
if __name__ == '__main__':
    #getcontent()
    db=pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu",charset='utf8')
    cursor = db.cursor()
    listFiles(filepath,db)
     db.close()
    
