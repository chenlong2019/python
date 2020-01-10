# coding=utf-8
import arcpy
in_raster=u"D:\\testdata\\oragdata\\t1\\2016-spectral_00.img"
property_type=["MINIMUM","MAXIMUM","MEAN","STD","TOP","LEFT","RIGHT","BOTTOM","CELLSIZEX","CELLSIZEY","COLUMNCOUNT","ROWCOUNT","BANDCOUNT","ANYNODATA","ALLNODATA","SENSORNAME","PRODUCTNAME","ACQUISITIONDATE","SOURCETYPE","CLOUDCOVER","SUNAZIMUTH","SUNELEVATION","SENSORAZIMUTH","SENSORELEVATION","OFFNADIR","WAVELENGTH"]
for property in property_type:
    try:
        elevResult =arcpy.GetRasterProperties_management(in_raster, property)
        elev = elevResult.getOutput(0)
        print(property+":"+elev)
    except :
        pass
    