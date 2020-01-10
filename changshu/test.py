import time,os,sys
import arcpy
in_features=u'D:\\shapedata\\testf0503312\\calculate_output.shp'
arcpy.CalculateAreas_stats.CalculateGeometryAttributes_management(in_features, ["AREA"], "SQUARE_METERS")
