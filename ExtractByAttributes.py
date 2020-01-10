# 栅格数据提取分析
# Name: ExtractByAttributes_Ex_02.py
# Description: Extracts the cells of a raster based on a logical query. 
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set environment settings
env.workspace = "F:\\result\\pm25\\20190815\\tif"

# Set local variables
inRaster = "F:\\O3T2019_8_16_13.tif"
inSQLClause = ""
inMaskData = "D:\\cs\\res\\inshp\\cs.shp"

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")

# Execute ExtractByMask
outExtractByMask = ExtractByMask(inRaster, inMaskData)
#Get the geoprocessing result object
elevMAXIMUMResult = arcpy.GetRasterProperties_management(outExtractByMask, "MAXIMUM")
#Get the elevation standard deviation value from geoprocessing result object
elevMAXIMUM = float(elevMAXIMUMResult.getOutput(0))
elevMINIMUMResult = arcpy.GetRasterProperties_management(outExtractByMask, "MINIMUM")
#Get the elevation standard deviation value from geoprocessing result object
elevMINIMUM = float(elevMINIMUMResult.getOutput(0))
inSQLClause="VALUE > "+str(elevMAXIMUM-(elevMAXIMUM-elevMINIMUM)/10)
# Execute ExtractByAttributes
attExtract = ExtractByAttributes(outExtractByMask, inSQLClause) 


# Save the output 
#attExtract.save("F:\\ree\\PM25T08.tif")
outLine="F:\\ree\\O3.shp"
field = "VALUE"
outGeom = "LINE"
arcpy.RasterDomain_3d(attExtract, outLine, outGeom)