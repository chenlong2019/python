import arcpy
import os,zipfile
from arcpy.sa import *
import MySQLdb as pymysql
import time
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
def getcontent():
    pathDir =  os.listdir("F:\\st")
    satellitezippath='F:\\zip\\changshu\\satellite'
    try:
        os.makedirs(satellitezippath)
    except :
        print('')
    db=pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu",charset='utf8')
    cursor = db.cursor()
    for contents in pathDir:
        if contents[-4:].lower() == '.tif':
            filepath=os.path.join("F:\\st",contents)
            index=filepath.index('2019')
            mon=filepath[index+4:index+6]
            day=filepath[index+6:index+8]
            date='2019-'+mon+'-'+day
            timeArray = time.strptime(date, "%Y-%m-%d")
            timestamp=int(time.mktime(timeArray))
            print(timestamp)
            if os.path.exists(filepath):
                    try:
                        # 执行sql语句
                        sql='INSERT INTO newchangshu.ams_wms (wmsname,  data_time, datatype, city,create_time,create_by,workspace) VALUES ({},{},{},{},{},{},{})'.format('"'+contents[:-4]+'"',timestamp,u'"pm25"',u'"常熟"'.decode('ISO-8859-1').encode('utf-8'),int(time.time()),'"admin"','"1"')
                        #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
                        cursor.execute(sql)
                        # 提交到数据库执行
                        db.commit()
                    except:
                        # 如果发生错误则回滚
                        traceback.print_exc()
                        db.rollback()
            continue
            shppath="F:\\changshu\\satellite\\"+contents[:-4]
            try:
                os.makedirs(shppath)
            except :
                print('')
            outPointFeatures=shppath+"\\"+contents[:-4]+'.shp'
            try:
                RasterToPoint_conversion(filepath,outPointFeatures)
                make_zip(shppath,satellitezippath+"\\"+contents[:-4]+".zip")
            except Exception as Error: 
                print Error
                              
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
    getcontent()