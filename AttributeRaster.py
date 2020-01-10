# coding=utf-8
import arcpy
from arcpy.sa import *
import xml.etree.ElementTree as ET 
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial") 
def RasterToPoint_conversion(outRaster):
    rastername=outRaster.split('\\')[-1][:-4]
    tree = ET.parse(u"D:\\sld\\pm252019083009.sld")
    for NamedLayer in tree.iter(tag='NamedLayer'):
        Namelist=NamedLayer._children
        for Name in Namelist:
            if(Name.tag==u'Name'):
                Name.text=rastername
    for FeatureTypeStyle in tree.iter(tag='FeatureTypeStyle'):
        FeatureTypeNamelist=FeatureTypeStyle._children
        for FeatureTypeName in FeatureTypeNamelist:
            if(FeatureTypeName.tag==u'FeatureTypeName'):
                FeatureTypeName.text=rastername
    inMaskData="F:\\result\\changshu\\cs.shp"
    # Execute ExtractByMask
    outExtractByMask = ExtractByMask(outRaster,inMaskData)
     #Get the geoprocessing result object
    elevMAXIMUMResult = arcpy.GetRasterProperties_management(outRaster, "MAXIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMAXIMUM = float(elevMAXIMUMResult.getOutput(0))
    elevMINIMUMResult = arcpy.GetRasterProperties_management(outRaster, "MINIMUM")
    #Get the elevation standard deviation value from geoprocessing result object
    elevMINIMUM = float(elevMINIMUMResult.getOutput(0))
    leng=(elevMAXIMUM-elevMINIMUM)/10
    for i in range(0,10):
        min=str(elevMINIMUM+leng*i+0.000000001)
        max=str(elevMINIMUM+leng*(i+1))
        Rule=FeatureTypeStyle._children[i+1]
        rclist=Rule._children
        for rc in rclist:
            if(rc.tag==u'Name'):
                rc.text=min+"-"+max
            if(rc.tag==u'Title'):
                rc.text=min+"-"+max
            if(rc.tag==u'{http://www.opengis.net/ogc}Filter'):
                # ns0:LowerBoundary
                rc._children[0]._children[1]._children[0].text=min
                # ns0:LowerBoundary
                rc._children[0]._children[2]._children[0].text=max
                print min+"-"+max
    tree.write(u"D:\\sld\\test\\"+rastername+".sld", encoding='utf-8', xml_declaration=True) 

if __name__ == '__main__':
    RasterToPoint_conversion('F:\\zouhangshuju\\20190903\\090310\\PM25\\tif\\PM252019_09_03_10.tif')
