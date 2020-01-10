# coding=utf-8
# 常熟市溯源
# @time 2019-9-6 15:59:09
# @author lichunming,chenlong
# AOT文件

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

# 中间文件夹
outpath=u'F:\\常熟溯源\\'+time.strftime('%Y%m%d',time.localtime(time.time()))
# 坐标系转换
def projectRaster(raster):
    try:
        os.makedirs(outpath)
    except :
        pass
    out=os.path.join(outpath,"Pro_"+str(int(time.time()))+'.tif') 
    # "GCS_WGS_1984"
    ref= arcpy.SpatialReference(4326)
    # 坐标系转换
    arcpy.ProjectRaster_management(raster,out,ref)
    # 水体掩膜
    outExtractByMask = arcpy.sa.ExtractByMask(out, u'E:\\常熟溯源\\水掩膜在最终文件\\常熟水掩膜最终文件.shp')
    # 去零值
    outSetNull = arcpy.sa.SetNull(outExtractByMask, outExtractByMask, "VALUE = 0")
    outSetNulltif=os.path.join(outpath,"outSetNull_"+str(int(time.time()))+'.tif') 
    outSetNull.save(outSetNulltif)
    # 裁剪
    conversion(outSetNulltif,raster)

# 剪裁、栅格转点
def conversion(outRaster,raster):
    # 按掩膜提取
    outExtractByMask=None
    # 常熟市溯源范围矢量文件
    inMaskData=u"E:\\常熟溯源\\矢量\\常熟边界\\常熟市溯源范围.shp"
    # 中间文件
    inPointFeatures=outpath+"\\"+os.path.split(raster)[1][:-4]+'_'+getTime()+'.shp'
    outCliptif=outpath+"\\"+os.path.split(raster)[1][:-4]+'_'+getTime()+'.tif'
    # 剪裁
    try:
        # Execute ExtractByMask
        arcpy.Clip_management(outRaster,"#",outCliptif,inMaskData , "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
    except Exception as err:
        arcpy.AddMessage("------Clip_management") 
        arcpy.AddMessage(err)
    # 重采样
    # resampletif=outpath+"\\"+os.path.split(raster)[1][:-4]+'_resampletif_'+getTime()+'.tif'
    # arcpy.Resample_management(outExtractByMask, resampletif, "0.0005", "BILINEAR")
    arcpy.AddMessage("------栅格转点开始。。。")
    try:
        arcpy.RasterToPoint_conversion(outCliptif, inPointFeatures, 'VALUE')
    except :
        arcpy.AddMessage('-------'+inPointFeatures+" 已经存在。。。")
    arcpy.AddMessage("------栅格转点完成")
    # 克里金插值
    Krigingfile=os.path.join(outpath,'Kriging_'+os.path.split(raster)[1][:-4]+".tif")
    field = "GRID_CODE"
    cellSize =0.00055
    outVarRaster = ""
    kModel = "Spherical"
    kRadius = 20000
    # Execute Kriging
    try:
        arcpy.Kriging_3d(inPointFeatures, field, Krigingfile, kModel, cellSize, kRadius, outVarRaster)
    except :
        arcpy.AddMessage('------RasterToPoint_conversion Failed')
    # 常熟市范围掩膜
    changshumask=u'E:\\常熟溯源\\矢量\\常熟边界\\常熟边界缓冲区-去水域.shp'
    outtif=os.path.join(outpath,os.path.split(raster)[1][:-4]+".tif")
    # 按掩膜提取
    try:
        # Execute ExtractByMask
        outMask = arcpy.sa.ExtractByMask(Krigingfile, changshumask)
        outCon = arcpy.sa.Con(arcpy.sa.IsNull(outMask),0.0001, outMask)
        outCon.save(outtif)
    except Exception as err:
        arcpy.AddMessage("------ExtractByMask Failed") 
        arcpy.AddMessage(err)
    name=os.path.split(raster)[1][:-4]
    createTraceFiles(outtif,name)

def getTime():
    return str(int(time.time()))

# 创建溯源文件
def createTraceFiles(in_layer,name):
    # 选中常熟市企业分区1中的AOT点并导出
    arcpy.AddMessage("-------制作溯源文件。。。")
    # 企业分区文件位置
    zoneLocation=u'E:\\常熟溯源\\矢量\\常熟市溯源范围'
    # 创建文件夹
    # AOT文件
    aot_Content='F:\\changshutraceresult\\aot'
    try:
        os.makedirs(aot_Content)
    except :
        arcpy.AddMessage('-------'+aot_Content+'已经存在')
    path2Dir =  os.listdir(zoneLocation)
    for zonefile in path2Dir:
        if zonefile[-4:].lower() == '.shp':
            zone_Layer=os.path.join(zoneLocation,zonefile)
            arcpy.AddMessage('-------'+name+' 分区'+zonefile[-6:-4]+ ' -------------------')
            try:
                # 剪裁
                # Execute ExtractByMask
                outClipRaster=os.path.join(aot_Content,'AOT分区'+zonefile[-6:-4]+'_'+name+'.tif')
                arcpy.Clip_management(in_layer,"#",outClipRaster,zone_Layer , "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
            except :
                arcpy.AddMessage('-------'+name+' 分区'+zonefile[-6:-4]+ 'Clip_management 错误')
                traceback.print_exc()
    arcpy.AddMessage("------制作溯源文件完成")

if __name__ == '__main__':
    RasterFileLocation=u'E:\\常熟溯源\\20191010modis'
    path2Dir =  os.listdir(RasterFileLocation)
    tif_file_number=glob.glob(pathname=RasterFileLocation+'\\*.tif')
    img_file_number=glob.glob(pathname=RasterFileLocation+'\\*.img')
    arcpy.AddMessage("---总共"+bytes(len(tif_file_number+img_file_number))+" 个栅格文件")
    for file in path2Dir:
        if file[-4:].lower() == '.tif' or file[-4:].lower() == '.img':
            inRaster=os.path.join(RasterFileLocation,file)
            arcpy.AddMessage('---'+inRaster)
            try:
                start=time.time()
                projectRaster(inRaster)
                end=time.time()
                print('---'+inRaster+': Running time: %s Seconds'%(end-start))
            except:
                traceback.print_exc()
    arcpy.AddMessage('---'+'完成')
  