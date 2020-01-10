# _*_ coding: utf-8 _*_

import sys
import os  
import io
import cv2
import time
import numpy as np
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 打印出中文字符
try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import gdal
    import ogr
    import osr

def readimage(filename_in):
    image = gdal.Open(filename_in)
    if image is None:
        print ("The multi image File can't be opened")
        sys.exit(1)
    nb = image.RasterCount
    cols = image.RasterXSize
    rows = image.RasterYSize
    image_array = np.zeros((rows, cols, nb))
    for i in range(nb):
        bandi = image.GetRasterBand(i + 1)
        image_array[:, :, i] = bandi.ReadAsArray(0, 0, cols, rows)
    image_matrix = image_array.reshape((rows * cols, nb))
    print ('')
    return image_array,image_matrix,rows,cols,nb,image


gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
ogr.RegisterAll()
driver = ogr.GetDriverByName('ESRI Shapefile')
Img_fileName='D:\\testdata\\tif\\SVM_outsetnullraster__1576543591.tif'#'D:\\testdata\\tif\\ELM_outraster__89026c17.tif'
imgs = cv2.imread(Img_fileName,2)
#img = cv2.imread(Img_fileName, 1)
image_array,image_matrix,rows,cols,nb,image = readimage(Img_fileName)
xsize = image.RasterXSize
ysize = image.RasterYSize
Img_file=cv2.imread('F:\\dw.jpg')
img1 = cv2.cvtColor(imgs, cv2.COLOR_BGR2GRAY)
ret, img2 = cv2.threshold(img1, 200, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(
    img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 提取二值图的所有轮廓边界
# print(contours)
# img = cv2.drawContours(img0, contours, -1, (0, 255, 0), 3)
# cv2.imshow("rotation", img)
# cv2.waitKey()
# cv2.destroyAllWindows()

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")  # 为了支持中文路径
gdal.SetConfigOption("SHAPE_ENCODING", "CP936")  # 为了使属性表字段支持中文
strVectorFile = "D:\\testdata\\shpgdal\\test1{}.shp".format(time.time())  # 定义写入路径及文件名
ogr.RegisterAll()  # 注册所有的驱动
strDriverName = "ESRI Shapefile"  # 创建数据，这里创建ESRI的shp文件
oDriver = ogr.GetDriverByName(strDriverName)
if oDriver == None:
    print("%s 驱动不可用！\n", strDriverName)

oDS = oDriver.CreateDataSource(strVectorFile)  # 创建数据源
if oDS == None:
    print("创建文件【%s】失败！", strVectorFile)

srs = osr.SpatialReference()  # 创建空间参考
srs.ImportFromEPSG(4326)  # 定义地理坐标系WGS1984
papszLCO = []
# 创建图层，创建一个多边形图层,"TestPolygon"->属性表名
oLayer = oDS.CreateLayer("TestPolygon", srs, ogr.wkbPolygon, papszLCO)
if oLayer == None:
    print("图层创建失败！\n")

'''下面添加矢量数据，属性表数据、矢量数据坐标'''
oFieldID = ogr.FieldDefn("FieldID", ogr.OFTInteger)  # 创建一个叫FieldID的整型属性
oLayer.CreateField(oFieldID, 1)

oDefn = oLayer.GetLayerDefn()  # 定义要素
gardens = ogr.Geometry(ogr.wkbMultiPolygon)  # 定义总的多边形集
i = 0
for contour in contours:
    area = cv2.contourArea(contour)
    if area >= 0:  # 面积大于n才保存
        # print(area)
        box1 = ogr.Geometry(ogr.wkbLinearRing)
        i += 1
        for point in contour:
            x_col = float(point[0, 1])
            y_row = float(point[0, 0])
            box1.AddPoint(y_row, x_col)
        oFeatureTriangle = ogr.Feature(oDefn)
        oFeatureTriangle.SetField(0, i)
        garden1 = ogr.Geometry(ogr.wkbPolygon)  # 每次重新定义单多变形
        garden1.AddGeometry(box1)  # 将轮廓坐标放在单多边形中
        gardens.AddGeometry(garden1)  # 依次将单多边形放入总的多边形集中
gardens.CloseRings()  # 封闭多边形集中的每个单多边形，后面格式需要

geomTriangle = ogr.CreateGeometryFromWkt(str(gardens))  # 将封闭后的多边形集添加到属性表
oFeatureTriangle.SetGeometry(geomTriangle)
oLayer.CreateFeature(oFeatureTriangle)
oDS.Destroy()
print("数据矢量创建完成！\n")