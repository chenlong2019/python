import pymysql
import time,os,traceback
            

def selectIndex(index,date,hour,val,db):
    data = "{}11".format(index)+date + hour
    path = u"E:\\输出结果\\tif\\{}\\201911{}\\{}_{}{}.tif".format(index,date,index,date,hour)
    coverageName = "{}_2019{}{}".format(index,date,hour) 
    timeformat='2019'+"-11-{}".format(date)+" "+hour+":"+"00"+":"+"00"
    timeArray = time.strptime(timeformat, "%Y-%m-%d %H:%M:%S")
    timestamp=time.mktime(timeArray)
    if os.path.exists(path):
        print(path)
        try:
            # 执行sql语句
            sql='INSERT INTO ams_wms (wmsname, url, data_time, datatype, city,create_time,workspace) VALUES ({},{},{},{},{},{},{})'.format('"'+coverageName+'"',u'"http://119.3.37.164:8090/geoserver"',timestamp,val,u'"常熟"',int(time.time()),'"0"')
            #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            traceback.print_exc()
            db.rollback()

if __name__ == '__main__':
    db=pymysql.connect("localhost","root","123456","changshu_dbluesp",charset='utf8')
    cursor = db.cursor()
    for j in range(12,13):
        for i in range(4,11):
            hour = str(i) if (i>9) else '0'+str(i)
            date=str(j) if (j>9) else '0'+str(j)
            index='SO2' 
            selectIndex(index,date,hour,u'"so2"',db)
            index='PM25' 
            selectIndex(index,date,hour,u'"pm25"',db)
            index='PM10' 
            selectIndex(index,date,hour,u'"pm10"',db)
            index='NO2' 
            selectIndex(index,date,hour,u'"no2"',db)
            index='CO' 
            selectIndex(index,date,hour,u'"co"',db)
            index='O3' 
            selectIndex(index,date,hour,u'"o3"',db)
