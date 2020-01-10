import sys
def createRC(path,rasterFile):
    import arcpy
    import os
    from arcpy import env
    env.workspace=path
    rasterFile=arcpy.RasterToGeodatabase_conversion(rasterFile,path)
    return rasterFile
if __name__ == '__main__':
	print(createRC(sys.argv[1],sys.argv[2]));
    #print(createRC('D:\\bysj\\file\\cdut.gdb','D:\\bysj\\data\\sssaa1.tif'));