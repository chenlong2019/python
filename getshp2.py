import arcpy
import os,zipfile
from arcpy.sa import *
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("3D")
def getcontent():
    pathDir =  os.listdir("F:\\zouhangshuju")
    pm25zippath='F:\\zip\\changshu\\pm25'
    voczippath='F:\\zip\\changshu\\voc'
    try:
        os.makedirs(pm25zippath)
    except :
        print('')
    try:
        os.makedirs(voczippath)
    except :
        print('')
    for contents in pathDir:
        if(int(contents)<20190831):
            print contents
            continue
        filepath=os.path.join("F:\\zouhangshuju",contents)
       
        dateDir =  os.listdir(filepath)
        for datecontents in dateDir:
            datecontent=os.path.join(filepath,datecontents)
            if os.path.isdir(datecontent):
                PM25='PM252019_'+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                VOC='VOC2019_'+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                pm25shpdir="F:\\changshu\\siteetis\\pm25\\"+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                vocshpdir="F:\\changshu\\siteetis\\voc\\"+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                try:
                    os.makedirs(pm25shpdir)
                except :
                    print('')
                try:
                    os.makedirs(vocshpdir)
                except :
                    print('')
                pm25dir=os.path.join(datecontent+"\\PM25\\tif",PM25+'.tif')
                vocdir=os.path.join(datecontent+"\\VOC\\tif",VOC+'.tif')
                print pm25dir
                print vocdir
                pm25PointFeatures=os.path.join(pm25shpdir,PM25+'.shp')
                vocPointFeatures=os.path.join(vocshpdir,VOC+'.shp')
                try:
                    RasterToPoint_conversion(pm25dir,pm25PointFeatures)
                    make_zip(pm25shpdir,"F:\\changshu\\csstate\\pm25"+"\\"+PM25+".zip")
                except Exception as Error: 
                    print Error
                try:
                    RasterToPoint_conversion(vocdir,vocPointFeatures)
                    make_zip(vocshpdir, "F:\\changshu\\csstate\\voc"+"\\"+VOC+".zip")
                except Exception as Error: 
                    print Error
   
                              
# 按掩模提取
def RasterToPoint_conversion(outRaster,inPointFeatures):
    inMaskData="F:\\changshu\\Changshu City_AL6.shp"
    # Execute ExtractByMask
    outExtractByMask = ExtractByMask(outRaster,inMaskData)
    # 栅格转点
    arcpy.RasterToPoint_conversion(outExtractByMask, inPointFeatures, "VALUE")

#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            zipf.write(pathfile, filename)
    zipf.close()
if __name__ == '__main__':
    getcontent()