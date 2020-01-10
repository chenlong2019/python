import arcpy
fc="D:\\成都市矢量数据\\宾馆酒店.shp"
for row in arcpy.da.SearchCursor(fc, ["SHAPE@XY"]):
    x,y=row[0]
    print("{}, {}".format(x, y))