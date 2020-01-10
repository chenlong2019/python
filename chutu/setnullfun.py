# coding=utf-8
import arcpy
from arcpy import env
import time
import os,glob,traceback
# Check out the ArcGIS Geostatistical Analyst extension license
arcpy.CheckOutExtension("GeoStats")
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
raster="D:\\testdata\\tif\\SVM_outraster__10355e48.tif"
outSetNull = arcpy.sa.SetNull(raster, raster, "VALUE = 0")
outSetNull.save("D:\\testdata\\tif\\SVM_outsetnullraster__{}.tif".format(int(time.time())))