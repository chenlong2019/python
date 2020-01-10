# coding=utf-8
import arcpy
import os,zipfile,traceback,time
from arcpy.sa import *
import MySQLdb as pymysql
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")

db=pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu",charset='utf8')
cursor = db.cursor()
def listfile(file):
    pathDir =  os.listdir(file)
    for contents in pathDir:
        # contents=100206
        try:  
            hourtime=contents[-2:]
            datetime=contents[-4:-2]
            filename="PM25_"+hourtime+'.tif'
            filepath=os.path.join(file,contents)
            if os.path.isdir(filepath):
                tifpath=filepath+'\\PM25\\tif\\'+filename
                print(tifpath)
                pm25shpdir="F:\\changshu\\siteetis\\pm251002\\pm25_1002"+hourtime
                try:
                    os.makedirs(pm25shpdir)
                except :
                    print('')
                timeformat='2019'+"-10-02"+" "+hourtime+":"+"00"+":"+"00"
                timeArray = time.strptime(timeformat, "%Y-%m-%d %H:%M:%S")
                timestamp=time.mktime(timeArray)
                '''try:
                    # 执行sql语句
                    sql='INSERT INTO newchangshu.ams_wms (wmsname, url, data_time, datatype, city,create_time,create_by,workspace) VALUES ({},{},{},{},{},{},{},{})'.format('"pm25_1008'+hourtime+'"','"http://119.3.37.164:8090/geoserver"',timestamp,u'"pm25"',u'"常熟"'.decode('ISO-8859-1').encode('utf-8'),int(time.time()),'"admin"','"0"')
                    #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                    pass
                except:
                    # 如果发生错误则回滚
                    traceback.print_exc()
                    db.rollback()
                continue'''
                inPointFeatures=os.path.join(pm25shpdir,"pm25_1002"+hourtime+hourtime+'.shp')
                # 栅格转点
                arcpy.RasterToPoint_conversion(tifpath, inPointFeatures, "VALUE")
                pm25zippath='F:\\zip\\changshu\\PM2502'
                try:
                    os.makedirs(pm25zippath)
                except :
                    print('')
                make_zip(pm25shpdir,pm25zippath+"\\"+"PM25_1002"+hourtime+hourtime+".zip")
                pass
        except :
            pass
                              
# 按掩模提取
def RasterToPoint_conversion(outRaster,inPointFeatures):
    inMaskData="F:\\changshu\\Changshu City_AL6.shp"
    # Execute ExtractByMask
    outExtractByMask = ExtractByMask(outRaster,inMaskData)
    # 栅格转点
    arcpy.RasterToPoint_conversion(outExtractByMask, inPointFeatures, "VALUE")

#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            zipf.write(pathfile, filename)
    zipf.close()

if __name__ == '__main__':
    try:
        file='20191002'
        filepath=os.path.join('F:\\xu',file)
        listfile(filepath)
    except:
        traceback.print_exc()
   