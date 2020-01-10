import arcpy
def eachFile(shppath,filepath):
    pathDir =  os.listdir(filepath)
    path_file_number=glob.glob(pathname=filepath+'\\*.tif')
    path_file_number = bytes(len(path_file_number))
    print "alter "+path_file_number+" files"
    count = 0
    for inRaster in pathDir:
        outExtractByMask = ExtractByMask(outRaster, inMaskData)
        outPoint = shppath+os.path.splitext(inRaster)[0]+".shp"
        field = "VALUE"
        count+=1
        if(os.path.exists(outPoint)):
            print outPoint+" alderly exists!"
            continue
        print "exporting "+inRaster
        arcpy.RasterToPoint_conversion(inRaster, outPoint, field)
        print inRaster+" alderly exported"
        file_number = bytes(count)
        print "alderly exported "+file_number+" file"
    print "success!"
arcpy.Clip_management("image.tif", "#", "clip.tif","feature.shp", "0", "ClippingGeometry")