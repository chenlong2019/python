# coding=utf-8
import arcpy
import os
import time,sys,traceback
# Check out the ArcGIS Geostatistical Analyst extension license
arcpy.CheckOutExtension("GeoStats")
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
def ExtractRange(outRaster,outFilePath):
    inSQLClause="VALUE > 0"
    try:
        # Execute ExtractByAttributes
        attExtract = arcpy.sa.ExtractByAttributes(outRaster, inSQLClause) 
        print('67')
        sys.stdout.flush()
        # Save the output 
        #attExtract.save("F:\\ree\\PM25T08.tif")
        rasfile=os.path.split(outRaster)[1]
        outFileName=os.path.splitext(rasfile)[0]+".shp"
        outLine = os.path.join(outFilePath , outFileName)
        field = "VALUE"
        outGeom = "LINE"
        try:
            # Execute ExtractByAttributes
            arcpy.RasterDomain_3d(attExtract, outLine, outGeom) 
            normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            arcpy.AddMessage(normaltime+":"+outRaster+"污染划分完成")
            print('90')
            sys.stdout.flush()
        except Exception as err:
            arcpy.AddMessage(outRaster+"RasterDomain_3d Failed") 
            arcpy.AddMessage(err)
    except Exception as err:
        arcpy.AddMessage("ExtractByAttributes Failed") 
        arcpy.AddMessage(err)
        traceback.print_exc()
        return 
    

if __name__ == '__main__':
    print('0')
    sys.stdout.flush()
    outRaster= u"D:\\shapedata\\1617\\Raster.tif"# sys.argv[1]
    outFilePath=u"D:\\shapedata\\1617"# sys.argv[2]
    ExtractRange(outRaster,outFilePath)
    print('100')
    sys.stdout.flush()

