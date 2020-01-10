# coding=utf-8
import arcpy
import os,glob,time
res=200
# 模板mxd文档路径，生成mxd文档路径
def createMxd(modelpath,mxdpath,filename,jpgpath):
    mxd=arcpy.mapping.MapDocument(modelpath)
    if(os.path.exists(mxdpath)):
        mxd=arcpy.mapping.MapDocument(mxdpath)
        print("location as "+mxdpath)
        arcpy.AddWarning("该文件已经存在")
    else:
        mxd.saveACopy(mxdpath)
        print(mxdpath+" saveAs succefssful")
        if(os.path.exists(mxdpath)):
            mxd=arcpy.mapping.MapDocument(mxdpath)
            print("location in "+mxdpath)
    # 查找数据框
    df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
    # 增加底图
    #symbologyLayer = "D:\\cs\\model\\lyr\\Rectangle_#1_常熟卫图_Level_16.tif.lyr"
    #"F:\\xinxiang\\fil\\20190817mydPM25.tif"
    shpLayer=arcpy.mapping.Layer(filename)
    arcpy.mapping.AddLayer(df, shpLayer, "TOP")
    df.extent=shpLayer.getExtent()
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
    mxd.save()
    arcpy.mapping.ExportToJPEG(mxd, jpgpath, resolution = res)


if __name__ == '__main__':
    modelpath=u"D:\\testdata\\mxd\\moudle_05.mxd"
    filename="D:\\testdata\\shp\\outraster__1def03c5.shp"
    layerpath='D:\\testdata\\lyr\\nonpol.lyr'
    try:
        mxdpath=u"D:\\testdata\\outmxd\\moudle_{}.mxd".format(int(time.time()))
        # mxd模板文件路径
        #modelpath=arcpy.GetParameterAsText(0)
        # 输出mxd文件路径
        #mxdpath=arcpy.GetParameterAsText(1)
        # tif文件路径 
        #filepath = "D:\\cs\\data\\pic3"
        # shp文件夹路径
        #filepath=arcpy.GetParameterAsText(3)
        # jpg输出路径 
        jpgpath="D:\\testdata\\jpg\\{}.jpg".format(int(time.time()))
        arcpy.AddMessage(str(time.ctime())+"输出开始!")
        createMxd(modelpath,mxdpath,filename,jpgpath,)
        print('successful')
        arcpy.AddMessage(str(time.ctime())+"输出完成!")
    except Exception as e:
        print(e.message)

