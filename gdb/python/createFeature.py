#coding:UTF-8
import sys
reload(sys) 
import arcpy
from arcpy import env
out_path="D:\\bysj\\file\\chen.gdb"
out_name="gongtong"
geometry_type="POLYGON"
arcpy.CreateFeatureclass_management (out_path, out_name, 
geometry_type,  "D:\\bysj\\data\\cd.shp", "DISABLED", "DISABLED", "D:\\bysj\\data\\cd.shp")