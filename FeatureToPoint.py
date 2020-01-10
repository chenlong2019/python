import arcpy
fc="F:\\ftpoint\\parcels_center.shp"
arcpy.FeatureToPoint_management("F:\\zouhangshuju\\20190819\\081909\\PM25\\rangle\\PM252019_08_19_09.shp", fc)
for row in arcpy.da.SearchCursor(fc, ["SHAPE@XY"]):
    x,y=row[0]
    print("{}, {}".format(x, y))