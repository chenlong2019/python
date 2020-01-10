# coding=utf-8
import pymysql
def getdb():
    return pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu" )

def create(db,sql):
    print(sql)
    print("connect to database")
    cursor = db.cursor()
    try:
        # 执行sql语句
        print("create start")
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print("create end")
    except:
        print("error")
        # 如果发生错误则回滚
        db.rollback()
        # 关闭数据库连接
        db.close()
def read(sql):
    print(sql)
    db=getdb()
    print("connect to database")
    cursor = db.cursor()
    try:
        # 执行SQL语句
        print("execute start")
        cursor.execute(sql)
        print("execute end")
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        print ("Error: unable to fetch data")
        return "Error"
    # 关闭数据库连接
    db.close()
#db=getdb()
# sql='INSERT INTO newchangshu.ams_sixindex (siteid, pubdate, aqi, pm25, pm10, so2, no2, co, o3, hcho, temperature, humidity, windspeed, winddirection, pressure) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{})'.format(1, 1564123930, 60.00, 1.20, 1.30, 0.52, 0.98, 0.45, 1.25, 1.24, 36.50, 77, 5.60, 332.00, 23.20)
# create(db,sql)
sql='SELECT MAX(six.pubdate) AS pubdate FROM newchangshu.ams_sixindex six'
results=read(sql)
print(results[0][0])