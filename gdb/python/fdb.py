#2019年5月10日14点44分
#创建文件地理数据库
import arcpy
path="D:\\bysj\\fdb"
fgdblst=arcpy.ListWorkspaces("*","FileGDB")
if fgdblst:
    for fgdb in fgdblst:
        fname=os.path.basename(fgdb)
    if fname[:-4]==fgdbname:
        print(fgdbname+'.gdb'+'已经存在！')
        fgb=path+'\\'+fgdbname+'.gdb'
    else:
        fgb=arcpy.CreateFileGDB_management(path,fgdbname)
else:
    fgb=arcpy.CreateFileGDB_management(path,fgdbname)
