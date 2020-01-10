#
#
#
import arcpy,os,glob
from arcpy import env


arcpy.CheckOutExtension("Spatial")
filepath=r"D:\\Project\\Changshu\\MODIS\\TIF\\PM2.5\\Spring"#输入文件文件夹
env.workspace = filepath
os.chdir(filepath)
Rasters = glob.glob("*.tif")
outfile=r'D:\\Project\\Changshu\\MODIS\\TIF\\PM2.5'#输出文件文件夹
inMaskData = r"E:\\矢量图\\exportedBoundaries_shp_levels_land_20190821_171302\\ChangshuCity_AL8.tif"#过滤文件文
for Raster in Rasters:
    inRaster = Raster
    arcpy.gp.ExtractByMask_sa(Raster, inMaskData, outfile+"\\"+Raster.split(".")[0]+'.img')







import arcpy
arcpy.CheckOutExtension("spatial")
arcpy.gp.overwriteOutput=1
arcpy.env.workspace = "D:\\Project\\Changshu\\MODIS\\TIF\\PM2.5\\Spring"
rasters = arcpy.ListRasters("*", "tif")
mask= "E:\\矢量图\\exportedBoundaries_shp_levels_land_20190821_171302\\Changshu City_AL6.shp"
for raster in rasters:
    print(raster)
    out= "D:\\Project\\Changshu\\MODIS\\TIF\\PM2.5\\"+"YM_"+raster[0:11]
    print(out)
    arcpy.gp.ExtractByMask_sa(raster, mask, out)
    print("ma_"+raster[0:11]+"  has done")
print("All done")
