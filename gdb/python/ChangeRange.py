# coding=utf-8
import arcpy
import os
import time,sys,traceback 
import sys
import shutil
import uuid
# Check out the ArcGIS Geostatistical Analyst extension license
arcpy.CheckOutExtension("GeoStats")
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
def ExtractRange(outRaster,outFilePath,file):
    inSQLClause="VALUE > 0"
    try:
        # Execute ExtractByAttributes
        attExtract = arcpy.sa.ExtractByAttributes(outRaster, inSQLClause) 
        print('87')
        sys.stdout.flush()
        # Save the output 
        #attExtract.save("F:\\ree\\PM25T08.tif")
        rasfile=os.path.split(outRaster)[1]
        in_point_features=os.path.join(file,u"RasterToPoint_conversion.shp")
        out_feature_class=os.path.join(file,u"AggregatePoints_cartography.shp")
        out_SmoothPolygon_class=os.path.join(file,u"out_SmoothPolygon_class.shp")
        calculate_output=os.path.join(file,u"calculate_output.shp")
        try:
            arcpy.RasterToPoint_conversion(attExtract, in_point_features , "VALUE")
        except:
            pass
        try:
            arcpy.AggregatePoints_cartography(in_point_features, out_feature_class, 30)
        except :
            pass
        try:
            arcpy.SmoothPolygon_cartography (out_feature_class, out_SmoothPolygon_class, 'PAEK', 30)
        except :
            pass
        try:
            # Process: Calculate Areas...
            arcpy.CalculateAreas_stats(out_SmoothPolygon_class, calculate_output)
        except:
            # If an error occurred when running the tool, print out the error message.
            traceback.print_exc()
        try:
            arcpy.Delete_management(in_point_features)
        except :
            traceback.print_exc()
        try:
            arcpy.DeleteFeatures_management(out_SmoothPolygon_class)
        except :
            traceback.print_exc()
        try:
            arcpy.DeleteFeatures_management(out_feature_class)
        except :
            traceback.print_exc()
        try:
            arcpy.Delete_management(out_feature_class)
        except :
            traceback.print_exc()
        try:
            arcpy.Delete_management(out_SmoothPolygon_class)
        except :
            traceback.print_exc()
        
    except Exception as err:
        arcpy.AddMessage("ExtractByAttributes Failed") 
        arcpy.AddMessage(err)
        traceback.print_exc()
        return 

if __name__ == '__main__':
    print('75')
    sys.stdout.flush()
    file=u'D:\\shapedata\\test'+str(uuid.uuid4())[:8]
    try:
        os.makedirs(file)
    except:
        pass
    outRaster=u'D:\\shapedata\\result\\2016-spectral17ac5c428.tif'
    outFilePath=os.path.join(file,u"test2.tif")
    ExtractRange(outRaster,outFilePath,file)
    shutil.rmtree(file)
    print('100')
    sys.exit(0)

