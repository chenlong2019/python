import arcpy
import os,zipfile
from arcpy.sa import *
import xmlUtil
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
def getcontent():
    pathDir =  os.listdir("F:\\zouhangshuju")
    pm25slddir="D:\\sld\\cssite\\pm25"
    vocslddir="D:\\sld\\cssite\\voc"
    try:
        os.makedirs(pm25slddir)
    except :
        print('')
    try:
        os.makedirs(vocslddir)
    except :
        print('')
    for contents in pathDir:
        filepath=os.path.join("F:\\zouhangshuju",contents)
        dateDir =  os.listdir(filepath)
        for datecontents in dateDir:
            datecontent=os.path.join(filepath,datecontents)
            if os.path.isdir(datecontent):
                PM25='pm252019_'+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                VOC='voc2019_'+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                # pm25.tif文件路径
                pm25dir=os.path.join(datecontent+"\\PM25\\tif",PM25+'.tif')
                # voc.tif文件路径
                vocdir=os.path.join(datecontent+"\\VOC\\tif",VOC+'.tif')
                print(PM25)
                try:
                    RasterToPoint_conversion(pm25dir,pm25slddir)
                except Exception as Error: 
                    print Error
                try:
                    RasterToPoint_conversion(vocdir,vocslddir)
                except Exception as Error: 
                    print Error
                              
# 按掩模提取
def RasterToPoint_conversion(outRaster,outSLDPath):
    inMaskData="F:\\result\\changshu\\cs.shp"
    # Execute ExtractByMask
    outExtractByMask = ExtractByMask(outRaster,inMaskData)
    elevMAXIMUMResult = arcpy.GetRasterProperties_management(outExtractByMask, "MAXIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMAXIMUM = float(elevMAXIMUMResult.getOutput(0))
    elevMINIMUMResult = arcpy.GetRasterProperties_management(outExtractByMask, "MINIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMINIMUM = float(elevMINIMUMResult.getOutput(0))
    rastername=outRaster.split('\\')[-1][:-4]
    xmlUtil.createSLD(rastername,elevMAXIMUM,elevMINIMUM,outSLDPath)

if __name__ == '__main__':
    getcontent()