#coding:UTF-8
import sys
reload(sys) 
import arcpy
from arcpy import env
out_dataset_path="D:\\bysj\\file\\chen.gdb"
out_name="tg"
def create(out_dataset_path,out_name):
		arcpy.CreateFeatureDataset_management(out_dataset_path, out_name)
if __name__ == '__main__':
	print(create(sys.argv[1],sys.argv[2]) );