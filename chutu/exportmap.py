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
    arcpy.ApplySymbologyFromLayer_management (rasLayer, symbologyLayer)
    arcpy.mapping.AddLayer(df, rasLayer, "TOP")
    arcpy.AddMessage(str(time.ctime())+":"+symbologyLayer+"添加成功。。。")
    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.text == u"20191013-05时":
            elm.text = string
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
    mxd.save()
    arcpy.mapping.ExportToJPEG(mxd, jpgpath, resolution = res)


if __name__ == '__main__':
    filelist=os.listdir(u"F:\\o3\\xu")
    modelpath=u"F:\\py27\\chutu\\module.mxd"
    for filename in filelist:
        path=os.path.join(u"F:\\o3\\xu",filename)
        if os.path.isdir(path):
            list=os.listdir(path)
            for file in list:
                filepath=os.path.join(path,file)
                if os.path.isdir(filepath):
                    try:
                        name='O3_'+file[-2:]
                        lyrfile=os.path.join(filepath,'O3\\tif\\'+name+'.tif')
                        print(lyrfile)
                        mxdpath=u"F:\\yingji\\mxd\\O3_"+file[-4:]+".mxd"
                        # mxd模板文件路径
                        #modelpath=arcpy.GetParameterAsText(0)
                        # 输出mxd文件路径
                        #mxdpath=arcpy.GetParameterAsText(1)
                        # tif文件路径 
                        symbologyLayer="F:\\py27\\chutu\\O3_10tif.lyr"
                        #filepath = "D:\\cs\\data\\pic3"
                        # shp文件夹路径
                        #filepath=arcpy.GetParameterAsText(3)
                        # jpg输出路径 
                        jpgpath="F:\\yingji\\jpg3\\O3_"+file[-4:]+".jpg"
                        string='201910'+file[-4:-2]+'-'+file[-2:]+u'时'
                        # jpgpath=arcpy.GetParameterAsText(4)
                        arcpy.AddMessage(string)
                        arcpy.AddMessage(str(time.ctime())+"输出开始!")
                        createMxd(modelpath,mxdpath,symbologyLayer,jpgpath,string,lyrfile)
                        print('successful')
                        arcpy.AddMessage(str(time.ctime())+"输出完成!")
                    except Exception as e:
                        print(e.message)

