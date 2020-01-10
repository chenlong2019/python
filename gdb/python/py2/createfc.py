import sys
def createFC(path,shpFile):
    import arcpy
    import os
    from arcpy import env
    env.workspace=path
    if arcpy.Exists(rasterFile):
        return shpFile+' already exists!'
    else:
        arcpy.FeatureClassToGeodatabase_conversion(shpFile,path)
        return shpFile
if __name__ == '__main__':
	print(createFC(sys.argv[1],sys.argv[2]));
    #print(createFC('D:\\bysj\\file\\cdut.gdb\\wwwqqqqqq','D:\\bysj\\data\\cd.shp'))