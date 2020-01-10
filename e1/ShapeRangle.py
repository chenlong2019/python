import arcpy
import os
import time
# Check out the ArcGIS Geostatistical Analyst extension license
arcpy.CheckOutExtension("GeoStats")
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
def ExtractRange(outRaster):
    inSQLClause="VALUE > 0"
    try:
        # Execute ExtractByAttributes
        attExtract = arcpy.sa.ExtractByAttributes(outRaster, inSQLClause) 
        # Save the output 
        #attExtract.save("F:\\ree\\PM25T08.tif")
        rasfile=os.path.split(outRaster)[1]
        outFileName=os.path.splitext(rasfile)[0]+".shp"
        outFilePath="D:\\shapedata\\1617\\"
        try:
            os.makedirs(outFilePath)
        except:
            print ("")
        outLine = os.path.join(outFilePath , outFileName)
        field = "VALUE"
        outGeom = "LINE"
        try:
            # Execute ExtractByAttributes
            arcpy.RasterDomain_3d(attExtract, outLine, outGeom) 
            normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            arcpy.AddMessage(normaltime+":"+outRaster+"污染划分完成")
        except Exception as err:
            arcpy.AddMessage(outRaster+"RasterDomain_3d Failed") 
            arcpy.AddMessage(err)
    except Exception as err:
        arcpy.AddMessage("ExtractByAttributes Failed") 
        arcpy.AddMessage(err)
        return 
    

if __name__ == '__main__':
    outRaster=u'D:\\shapedata\\1617\\outRaster.tif'
    ExtractRange(outRaster)

