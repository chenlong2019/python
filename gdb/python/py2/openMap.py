# encoding:utf-8
import arcpy.mapping as mapping
import sys
def openMxd(path):
    mxd=mapping.MapDocument(path)
    for df in mapping.ListDataFrames(mxd):
        layers=mapping.ListLayers(mxd,'*',df)
        return layers
print(openMxd("D:\\bysj\\data\\max3.mxd"))
#openMxd(sys.argv[1])