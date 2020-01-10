# coding=utf-8
import arcpy
import os,glob,time
res=200
# 模板mxd文档路径，生成mxd文档路径
def createMxd(modelpath,mxdpath,symbologyLayer,jpgpath,string,lyrfile):
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
            rasLayer=arcpy.mapping.Layer(lyrfile)
            symbologyLayr=arcpy.mapping.Layer(symbologyLayer)
            # rasLayer.symbology.
            arcpy.ApplySymbologyFromLayer_management (rasLayer,symbologyLayr)
            arcpy.mapping.AddLayer(df, rasLayer, "AUTO_ARRANGE")
            arcpy.AddMessage(str(time.ctime())+":"+symbologyLayer+"添加成功。。。")
            for legend in arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend"):
                print(legend.items)
            arcpy.RefreshActiveView()
            for legend in arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend"):
                print(legend.items)
            mxd.save()
    arcpy.mapping.ExportToJPEG(mxd, jpgpath, resolution = res)

if __name__ == '__main__':
    rootpath=u'F:\\xx\\中心城区'
    pathDir =  os.listdir(rootpath)
    try:
        os.makedirs(u'F:\\xx\\AutoMap\\result\\mxd\\o3')
    except:
        pass
    try:
        os.makedirs(u'F:\\xx\\AutoMap\\result\\JpgOutput')
    except:
        pass
    for filename in pathDir:
        if filename[-4:].lower() == '.tif':
            # o3
            if filename[-5:-4].lower() == '3':
                try:
                    filepath=os.path.join(rootpath,filename)
                    print(filename)
                    mxdpath=u"F:\\xx\\AutoMap\\result\\mxd\\xinxiang{}.mxd".format(filename[:-4])
                    modelpath=u"F:\\xx\\AutoMap\\Mxd\\xinxiang_O3.mxd"
                    # mxd模板文件路径
                    #modelpath=arcpy.GetParameterAsText(0)
                    # 输出mxd文件路径
                    #mxdpath=arcpy.GetParameterAsText(1)
                    # tif文件路径 
                    symbologyLayer=u'F:\\xx\\Lyr\\C_20191111modo356.lyr'
                    #filepath = "D:\\cs\\data\\pic3"
                    # shp文件夹路径
                    #filepath=arcpy.GetParameterAsText(3)
                    # jpg输出路径 
                    jpgpath=u"F:\\xx\\AutoMap\\result\\JpgOutput\\{}.jpg".format(filename[:-4])
                    # jpgpath=arcpy.GetParameterAsText(4)
                    arcpy.AddMessage('')
                    arcpy.AddMessage(str(time.ctime())+"输出开始!")
                    createMxd(modelpath,mxdpath,symbologyLayer,jpgpath,'',filepath)
                    print('successful')
                    arcpy.AddMessage(str(time.ctime())+"输出完成!")
                except Exception as e:
                    print(e.message)