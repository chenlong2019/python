#coding:UTF-8
import sys
reload(sys) 
import arcpy
from arcpy import env
out_dataset_path="D:\\bysj\\file\\chen.gdb"
out_name="qqq"
geometry_type="POLYGON"
arcpy.CreateRasterDataset_management(out_dataset_path, out_name)