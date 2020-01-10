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
    pathDir =  os.listdir("F:\\zouhangshuju")
    pm25slddir="D:\\sld\\cssite\\pm25"
    vocslddir="D:\\sld\\cssite\\voc"
    db=pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu",charset='utf8')
    cursor = db.cursor()
    try:
        os.makedirs(pm25slddir)
    except :
        print('')
    try:
        os.makedirs(vocslddir)
    except :
        print('')
    for contents in pathDir:
        if(int(contents)<20190924):
            print contents
            continue
        filepath=os.path.join("F:\\zouhangshuju",contents)
        dateDir =  os.listdir(filepath)
        for datecontents in dateDir:
            datecontent=os.path.join(filepath,datecontents)
            if os.path.isdir(datecontent):
                PM25='pm252019_'+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                VOC='voc2019_'+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                # pm25.tif文件路径
                pm25dir=os.path.join(datecontent+"\\PM25\\tif",PM25+'.tif')
                # voc.tif文件路径
                vocdir=os.path.join(datecontent+"\\VOC\\tif",VOC+'.tif')
                timeformat='2019'+"-"+datecontents[0:2]+"-"+datecontents[2:4]+" "+datecontents[4:6]+":"+"00"+":"+"00"
                timeArray = time.strptime(timeformat, "%Y-%m-%d %H:%M:%S")
                timestamp=time.mktime(timeArray)
                print(PM25)
                if os.path.exists(pm25dir):
                    try:
                        # 执行sql语句
                        sql='INSERT INTO newchangshu.ams_wms (wmsname,  data_time, datatype, city,create_time,create_by,workspace) VALUES ({},{},{},{},{},{},{})'.format('"'+PM25+'"',timestamp,u'"pm25"',u'"常熟"'.decode('ISO-8859-1').encode('utf-8'),int(time.time()),'"admin"','"changshusite"')
                        #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
                        cursor.execute(sql)
                        # 提交到数据库执行
                        db.commit()
                    except:
                        # 如果发生错误则回滚
                        traceback.print_exc()
                        db.rollback()
                if os.path.exists(vocdir):
                    try:
                        # 执行sql语句
                        sql='INSERT INTO newchangshu.ams_wms (wmsname, data_time, datatype, city,create_time,create_by,workspace) VALUES ({},{},{},{},{},{},{})'.format('"'+VOC+'"',timestamp,u'"voc"',u'"常熟"'.decode('ISO-8859-1').encode('utf-8'),int(time.time()),'"admin"','"changshusite"')
                        #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
                        cursor.execute(sql)
                        # 提交到数据库执行
                        db.commit()
                    except:
                        # 如果发生错误则回滚
                        traceback.print_exc()
                        db.rollback()
                              
# 按掩模提取
def RasterToPoint_conversion(outRaster,outSLDPath):
    inMaskData="F:\\changshu\\Changshu City_AL6.shp"
    # Execute ExtractByMask
    outExtractByMask = ExtractByMask(outRaster,inMaskData)
    elevMAXIMUMResult = arcpy.GetRasterProperties_management(outExtractByMask, "MAXIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMAXIMUM = float(elevMAXIMUMResult.getOutput(0))
    elevMINIMUMResult = arcpy.GetRasterProperties_management(outExtractByMask, "MINIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMINIMUM = float(elevMINIMUMResult.getOutput(0))
    rastername=outRaster.split('\\')[-1][:-4]
    xmlUtil.createSLD(rastername,elevMAXIMUM,elevMINIMUM,outSLDPath)

if __name__ == '__main__':
    getcontent()
    
