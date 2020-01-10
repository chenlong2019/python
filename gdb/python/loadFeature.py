#coding:UTF-8
import sys
reload(sys)  
sys.setdefaultencoding('UTF-8') 
import arcpy
from arcpy import env
wspath="D:\\bysj\\fea"
env.workspace = wspath
#将shapefile导入文件数据库中
env.workspace=wspath
for fc in arcpy.ListFiles('*.shp'):
    env.workspace="D:\\bysj\\file\\chen.gdb"
    fcfgb=arcpy.ListFeatureClasses()
    fc=fc.split('.')[0]
    if fc in fcfgb:
        print(fc+" 已经存在!")
    else:
        env.workspace=wspath
        arcpy.FeatureClassToGeodatabase_conversion(fc,"D:\\bysj\\file\\chen.gdb")

#栅格数据
env.workspace=wspath
for fc in arcpy.ListRasters():
    s=fc
    env.workspace="D:\\bysj\\file\\chen.gdb"
    fcfgb=arcpy.ListRasters()
    fc=fc.split('.')[0]
    if fc in fcfgb:
        print(fc+" 已经存在!")
    else:
        env.workspace=wspath
        arcpy.RasterToGeodatabase_conversion(wspath+os.sep+s,fgb)