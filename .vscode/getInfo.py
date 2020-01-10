#coding=utf-8
import arcpy
import os
arcpy.env.workspace = 'E:\\PycharmProjects\\test\\test.gdb'
print 'Processing................. '
fcs = []
dscount=0
fscount=0
index=0
list=arcpy.ListDatasets('', '') + ['']
for fds in arcpy.ListRasters('','') + ['']:
    if not fds=='':
        arcpy.AddMessage(fds)
for fds in arcpy.ListDatasets('','') + ['']:
    if not fds=='':
        desc = arcpy.Describe(fds)
        if hasattr(desc, "dataType"):
            if desc.dataType=='FeatureDataset':
                arcpy.AddMessage('-----------------'+fds+' FeatureDataset')
                index=index+1
                print('{}'.format(index))
                for fc in arcpy.ListFeatureClasses('','',fds):
                    #yield os.path.join(fds, fc)
                    fcs.append(os.path.join(fds, fc))
        arcpy.AddMessage(fds)
        dscount=dscount+1
        for fc in arcpy.ListFeatureClasses('','',fds):
            #yield os.path.join(fds, fc)
            fcs.append(os.path.join(fds, fc))
for fcp in fcs:
    arcpy.AddMessage(fcp)
    fscount=fscount+1
arcpy.AddMessage(u'矢量数据集：'+str(dscount)+'个')
arcpy.AddMessage(u'矢量要素类：'+str(fscount)+'个')