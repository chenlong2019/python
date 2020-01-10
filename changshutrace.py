# coding=utf-8
# 常熟市溯源
# @time 2019-9-6 15:59:09
# @author lichunming,chenlong

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
outpath='F:\\20190910\\'+time.strftime('%Y%m%d',time.localtime(time.time()))
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
    outExtractByMask = arcpy.sa.ExtractByMask(out, 'F:\\20190905\\mask\\csMask.shp')
    # 去零值
    outSetNull = arcpy.sa.SetNull(outExtractByMask, outExtractByMask, "VALUE = 0")
    # 裁剪
    conversion(outSetNull,raster)

# 剪裁、栅格转点
def conversion(outRaster,raster):
    # 按掩膜提取
    outExtractByMask=None
    # 常熟市溯源范围矢量文件
    inMaskData="F:\\20190905\\data\\changshurangle\\changshutrace.shp"
    # 中间文件
    inPointFeatures=outpath+"\\"+os.path.split(raster)[1][:-4]+'_'+getTime()+'.shp'
    try:
        # Execute ExtractByMask
        outExtractByMask = arcpy.sa.ExtractByMask(outRaster, inMaskData)
    except Exception as err:
        arcpy.AddMessage("------ExtractByMask Failed") 
        arcpy.AddMessage(err)
        return
    # 重采样
    # resampletif=outpath+"\\"+os.path.split(raster)[1][:-4]+'_resampletif_'+getTime()+'.tif'
    # arcpy.Resample_management(outExtractByMask, resampletif, "0.0005", "BILINEAR")
    arcpy.AddMessage("------栅格转点开始。。。")
    try:
        arcpy.RasterToPoint_conversion(outExtractByMask, inPointFeatures, 'VALUE')
    except :
        arcpy.AddMessage('-------'+inPointFeatures+" 已经存在。。。")
    arcpy.AddMessage("------栅格转点完成")
    # 克里金插值
    titfile=os.path.join(outpath,os.path.split(raster)[1][:-4]+".tif")
    field = "GRID_CODE"
    cellSize =0.0005
    outVarRaster = ""
    kModel = "Spherical"
    kRadius = 20000
    # Execute Kriging
    try:
        arcpy.Kriging_3d(inPointFeatures, field, titfile, kModel, cellSize, kRadius, outVarRaster)
    except :
        Arcpy.AddMessage('------RasterToPoint_conversion Failed')
    arcpy.AddMessage("------栅格转点开始。。。")
    outPointFeatures=outpath+"\\"+os.path.split(raster)[1][:-4]+'.shp'
    try:
        arcpy.RasterToPoint_conversion(titfile, outPointFeatures, 'VALUE')
    except :
        arcpy.AddMessage('-------'+inPointFeatures+" 已经存在。。。")
    arcpy.AddMessage("------栅格转点完成")
    selectByLocatin(outPointFeatures)

def getTime():
    return str(int(time.time()))

# 按位置选择
def selectByLocatin(in_layer):
    arcpy.AddMessage("------按位置选择。。。")
    name=os.path.split(in_layer)[1][:-4]
    try:
        mflm='InLayer'+getTime()
        flayer=arcpy.MakeFeatureLayer_management(in_layer,mflm)
        arcpy.SelectLayerByLocation_management(flayer, 'COMPLETELY_WITHIN', 'F:\\20190905\\data\\changshurangle\\cs.shp',0,'NEW_SELECTION')
        # cnt=arcpy.GetCount_management(flayer)
        # arcpy.AddMessage("已选择{}行".format(str(cnt)))
        # 切换选择内容
        out_layer_or_view2=arcpy.SelectLayerByLocation_management(flayer,'','','','SWITCH_SELECTION')
        # cnt=arcpy.GetCount_management(flayer)
        # arcpy.AddMessage("已选择{}行".format(str(cnt)))
        arcpy.CalculateField_management(flayer, "GRID_CODE", "0.0001", "PYTHON") 
        # 全选
        arcpy.SelectLayerByLocation_management(flayer, 'COMPLETELY_WITHIN', 'F:\\20190905\\data\\changshurangle\\cs.shp',0,'ADD_TO_SELECTION')
        out_layer_or_view2=arcpy.SelectLayerByLocation_management(flayer,'','','','NEW_SELECTION')
        # cnt=arcpy.GetCount_management(flayer)
        # arcpy.AddMessage("已选择{}行".format(str(cnt)))
        # 添加字段
        arcpy.AddField_management (flayer, 'enterprise', 'DOUBLE')
        arcpy.AddField_management (flayer, 'value', 'DOUBLE')
        arcpy.CalculateField_management(flayer, "enterprise", "0", "PYTHON")
        arcpy.CalculateField_management(flayer, "value", "!GRID_CODE!", "PYTHON")
        copy_feature=outpath+"\\"+str(int(time.time()))+'.shp'
        arcpy.CopyFeatures_management(flayer,copy_feature)
        arcpy.AddMessage("-------按位置选择完成")
        try:
            arcpy.Delete_management(flayer)
            arcpy.Delete_management(in_layer)
        except Exception as e:
            arcpy.AddMessage(e.message)
        createTraceFiles(copy_feature,name)
        try:
            arcpy.Delete_management(copy_feature)
        except Exception as e:
            arcpy.AddMessage(e.message)
    except Exception as e:
        print e.message

# 创建溯源文件
def createTraceFiles(in_layer,name):
    # 选中常熟市企业分区1中的AOT点并导出
    arcpy.AddMessage("-------制作溯源文件。。。")
    # 企业分区文件位置
    zoneLocation='F:\\20190905\\data\\zone\\polygon'
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
            filename=getTime()+'_'+zonefile[:-4]
            arcpy.AddMessage("------"+filename)
            zone_Layer=os.path.join(zoneLocation,zonefile)
            ilayer='InLayer'+getTime()
            try:
                copy_layer="F:\\20190905\\data\\out\\point\\"+str(int(time.time()))+'.shp'
                arcpy.CopyFeatures_management(in_layer,copy_layer)
                flayer=arcpy.MakeFeatureLayer_management(copy_layer,ilayer)
                # 选择图层
                zone_feature=arcpy.SelectLayerByLocation_management(flayer, 'COMPLETELY_WITHIN',zone_Layer,0,'NEW_SELECTION')
                layer="F:\\20190905\\data\\out\\point\\"+str(int(time.time()))+'.shp'
                arcpy.CopyFeatures_management(zone_feature,layer)
                # cnt=arcpy.GetCount_management(flayer)
                # arcpy.AddMessage("已选择{}行".format(str(cnt)))
                # 合并后的要素输出位置
                out_feature_class='F:\\20190905\\data\\zone\\out\\'+filename+'.shp'
                # 合并要素
                arcpy.Merge_management([layer, "F:\\20190905\\data\\zone\\point\\"+zonefile[:-4]+"_company.shp"], out_feature_class)
                # 将合并后的点转为栅格，分辨率设为0.0005，参数设置如下
                out_rasterdataset=os.path.join(aot_Content,zonefile[:-4]+'企业坐标'+name[3:]+'.tif')
                arcpy.PointToRaster_conversion (out_feature_class, 'enterprise', out_rasterdataset, 'MAXIMUM', 'NONE', '0.0005')
                # 同样，将分区一的AOT点转为栅格，分辨率设为0.0005，参数设置如下，即得到分区1AOT文件
                out_rasterdataset2=os.path.join(aot_Content,zonefile[:-4]+name+'.tif')
                arcpy.PointToRaster_conversion (layer, 'value', out_rasterdataset2, 'MAXIMUM', 'NONE', '0.0005')
                try:
                    arcpy.Delete_management(flayer)
                    arcpy.Delete_management(layer)
                    arcpy.Delete_management(copy_layer)
                    arcpy.Delete_management(out_feature_class)
                except Exception as e:
                    arcpy.AddMessage(e.message)
            except Exception as e:
                print e.message
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
  