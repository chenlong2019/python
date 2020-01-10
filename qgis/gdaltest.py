from osgeo import gdal
from osgeo import osr,ogr
import time
#############获取矢量点位的经纬度
#设置driver
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
ogr.RegisterAll()
driver = ogr.GetDriverByName('ESRI Shapefile')
#打开矢量
file='D:\\testdata\\feature\\site_{}.shp'.format(time.time())
Img_fileName='D:\\testdata\\tif\\SVM_outsetnullraster__1576543591.tif'
image = gdal.Open(Img_fileName)
#ds = driver.Open('D:\\testdata\\feature\\sites.shp', 0)
#if ds is None:
   # print('Could not open ' +'sites.shp')
   # sys.exit(1)
#获取图层
ds = driver.CreateDataSource(file)
bandi = image.GetRasterBand(1)
poSpatialRef =osr.SpatialReference(image.GetProjectionRef())
poLayer=ds.CreateLayer("Result", poSpatialRef, ogr.wkbPolygon)
nb = image.RasterCount
gdal.Polygonize(bandi, None,poLayer,3, [], callback=None )

