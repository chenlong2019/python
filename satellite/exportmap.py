# encoding=utf-8
import arcpy
import os,glob,time
res=200
# 模板mxd文档路径，生成mxd文档路径
def createMxd(mxdpath,jpgpath,tifpath):
    # mxd模板文件路径
    modelpath="G:\\AutoMap\\Mxd\\xinxiangMap.mxd"
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
    
    rasLayer=arcpy.mapping.Layer(tifpath)
    # 图层文件路径
    symbologyLayer="G:\\AutoMap\\Lyr\\20190817mydPM25.lyr"
    arcpy.ApplySymbologyFromLayer_management (rasLayer, symbologyLayer)
    arcpy.mapping.AddLayer(df, rasLayer, "TOP")
    arcpy.AddMessage(str(time.ctime())+":"+symbologyLayer+"添加成功。。。")
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
    mxd.save()
    arcpy.mapping.ExportToJPEG(mxd, jpgpath, resolution = res)
if __name__ == '__main__':
   
    # 输出路径
    mxdpath= arcpy.GetParameterAsText(0)
    #mxdpath="F:\\xinxiang\\mxd\\cs4.mxd"
    # mxd模板文件路径
    #modelpath=arcpy.GetParameterAsText(0)
    # 输出mxd文件路径
    #mxdpath=arcpy.GetParameterAsText(1)
    # lyr文件路径 
    
    #filepath = "D:\\cs\\data\\pic3"
    # shp文件夹路径
    #filepath=arcpy.GetParameterAsText(3)
    # jpg输出路径 
    #jpgpath="F:\\xinxiang\\jpg\\yuuu5466.jpg"
    jpgpath=arcpy.GetParameterAsText(1)
    # tif原始文件路径
    tifpath=arcpy.GetParameterAsText(2)
    # jpgpath=arcpy.GetParameterAsText(4)
    arcpy.AddMessage(str(time.ctime())+"输出开始!")
    createMxd(mxdpath,jpgpath,tifpath)
    print('successful')
    arcpy.AddMessage(str(time.ctime())+"输出完成!")
