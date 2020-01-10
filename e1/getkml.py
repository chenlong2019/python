# coding=utf-8
import os,zipfile
import datetime
import time,traceback
import  pymysql
import requests
def getcontent(contents):
    db=pymysql.connect("localhost","root","123456","changshu_dbluesp",charset='utf8')
    cursor = db.cursor()
    filepath=os.path.join(u"D:\\wamp64\\www\\changshuams2\\public\\static\\kml",contents)
    filelist=os.listdir(filepath)
    for filename in filelist:
        kml_address="kml/"+contents+"/"+filename
        kml_type=filename[:4]
        kml_name=filename[:-4]
        date=filename[4:14]
        timeformat=date[:4]+"-"+date[4:6]+"-"+date[6:8]+" "+date[8:10]+":00:00"
        timeArray = time.strptime(timeformat, "%Y-%m-%d %H:%M:%S")
        kml_date=int(time.mktime(timeArray))
        # print kml_address
        try:
            # 执行sql语句
            sql='INSERT INTO changshu_dbluesp.ams_kml (kml_name, kml_type, kml_date, kml_address) VALUES ("{}","{}","{}","{}")'.format(kml_name,kml_type,kml_date,kml_address)
            print(sql)
            #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            traceback.print_exc()
            db.rollback()
    db.close()

if __name__ == '__main__':
    getcontent('20200108')

