import re
import arcpy
import os
import sys
from arcpy import env
env.workspace="D:\\bysj\\data\\KMLDataLoading"
#reader=open('D:\\bysj\\data\\KMLDataLoading\\yanhunanlu.txt','r')
s='D:\\bysj\\data\\KMLDataLoading\\yanhunanlu.txt'
s=s.split('\\')[-1]
imputname=s.split('.')[0]
reader=open('D:\\bysj\\data\\KMLDataLoading\\yanhunanlu.txt')
prjFile='D:\\bysj\\data\\cd.prj'
pat=re.compile('<coordinates>.*</coordinates>')
corstr=''
while True:
    line=reader.readline()
    if len(line)==0:
        break
    line=line.strip()
    m=pat.match(line)
    if m:
        line=line.strip()
        corstr=corstr+line
        #corstr=corstr.strip()
reader.close()
corstr=re.sub('<coordinates>(.*?)</coordinates>',r'\1',corstr)
coordilst=corstr.split(',')
coordilst=[float(a) for a in coordilst]
point=arcpy.Point()
point.X=coordilst[0]
point.Y=coordilst[1]
pointGeometry=arcpy.PointGeometry(point,prjFile)
outputname=imputname+'.shp'
arcpy.CopyFeatures_management(pointGeometry,outputname)
arcpy.AddField_management(outputname,'Name','TEXT',9,',','Name','NULLABLE','REQUIRED')
rows=arcpy.UpdateCursor(outputname)
for row in rows:
    row.Name=inputname
    rows.updateRow(row)
del rows,rows
arcpy.SetParameter(2,outputname)
arcpy.SetParameter(index,value)
print(outputname)