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
inRaster = "F:\\zouhangshuju\\20190816\\081617\\VOC\\tif\\VOC2019_08_16_17.tif"
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
#TOP —返回范围的顶部值或 Y 最大值 (YMax)。
#LEFT —返回范围的左侧值或 X 最小值 (XMin)。
#RIGHT —返回范围的右侧值或 X 最大值 (XMax)。
#BOTTOM —返回范围的底部值或 Y 最小值 (YMin)
attExtract.save("F:\\ae\\iiiid.tif")
YMin = arcpy.GetRasterProperties_management(attExtract, "TOP")
XMin = arcpy.GetRasterProperties_management(attExtract, "LEFT")
YMax = arcpy.GetRasterProperties_management(attExtract, "RIGHT")
XMax = arcpy.GetRasterProperties_management(attExtract, "BOTTOM")
arcpy.AddMessage("YMin: "+YMin.getOutput(0))
arcpy.AddMessage("XMin: "+XMin.getOutput(0))
arcpy.AddMessage("YMax: "+YMax.getOutput(0))
arcpy.AddMessage("XMax: "+XMax.getOutput(0))