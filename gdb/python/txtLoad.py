import re
import arcpy
import os
import sys
from arcpy import env
env.workspace="D:\\bysj\\data\\KMLDataLoading"
#reader=open('D:\\bysj\\data\\KMLDataLoading\\yanhunanlu.txt','r')
s=arcpy.GetParameterAsText(0)
s=s.split('\\')[-1]
imputname=s.split('.')[0]
reader=open(arcpy.GetParameterAsText(0))
prjFile=arcpy.GetParameterAsText(1)
pat=re.compile('<coordinates>.*</coordinates>')
while true:
    line=reader.readline()
    if len(line)==0:
        break
    line=line.strip()
    m=pat.match(line)
    if m:
        corstr=line
        corstr=corstr.strip()
reader.close()
corstr=re.sub('<coordinates>(.*?)</coordinates>',r'\1',corstr)
coordilst=sorstr.split(',')
coordilst=[float(a) for a in coordilst]
point=arcpy.Point()
point.X=coordilst[0]
point.Y=coordilst[1]
pointGeometry=inputname+'.shp'
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