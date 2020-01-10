# coding=UTF-8
#建立文件地理数据库并导入数据
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
import arcpy
import os
from arcpy import env 
env.overwriteOutput=True

def create(name,path):
	wspath=path
	env.workspace=path
	fgdbname=name
	fgdblst=arcpy.ListWorkspaces("*","FileGDB")
	if fgdblst:
		for fgdb in fgdblst:
			fname=os.path.basename(fgdb)
			if fname[:-4]==fgdbname:
				return fgdbname+'.gdb'+'已经存在！'
				fgb=wspath+'\\'+fgdbname+'.gdb'
			else:
				fgb=arcpy.CreateFileGDB_management(wspath,fgdbname)
	else:
		fgb=arcpy.CreateFileGDB_management(wspath,fgdbname)
	return 'succes'
if __name__ == '__main__':
	print(create(sys.argv[1],sys.argv[2]) );
