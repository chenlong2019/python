
    try:
        os.makedirs(pm25zippath)
    except :
        print('')
    try:
        os.makedirs(voczippath)
    except :
        print('')
    db=pymysql.connect("122.114.191.161","newchangshu","slkj1234","newchangshu")
    cursor = db.cursor()
    for contents in pathDir:
        filepath=os.path.join("F:\\zouhangshuju",contents)
        dateDir =  os.listdir(filepath)
        for datecontents in dateDir:
            datecontent=os.path.join(filepath,datecontents)
            if os.path.isdir(datecontent):
                PM25='pm252019_'+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                VOC='voc2019_'+datecontents[0:2]+'_'+datecontents[2:4]+'_'+datecontents[4:6]
                timeformat='2019'+"-"+datecontents[0:2]+"-"+datecontents[2:4]+" "+datecontents[4:6]+":"+"00"+":"+"00"
                timeArray = time.strptime(timeformat, "%Y-%m-%d %H:%M:%S")
                timestamp=time.mktime(timeArray)
                pm25dir=os.path.join(datecontent+"\\PM25\\tif",PM25+'.tif')
                vocdir=os.path.join(datecontent+"\\VOC\\tif",VOC+'.tif')
                print pm25dir
                print vocdir
                pm25shpdir=os.path.join("F:\\changshu\\sitedata\\pm25",PM25)
                vocshpdir=os.path.join("F:\\changshu\\sitedata\\voc",VOC)
                try:
                    os.makedirs(pm25shpdir)
                except :
                    print('')
                try:
                    os.makedirs(vocshpdir)
                except :
                    print('')
                pm25PointFeatures=os.path.join(pm25shpdir,PM25+'.shp')
                vocPointFeatures=os.path.join(vocshpdir,VOC+'.shp')
                try:
                    RasterToPoint_conversion(pm25dir,pm25PointFeatures)
                    try:
                # 执行sql语句
                        sql='INSERT INTO newchangshu.ams_cssite (imagedate, layername, type, workspace, store) VALUES ({},{},{},{},{})'.format(timestamp,'"'+PM25+'"','"site"','"cssite"','"pm25"')
                        #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
                        cursor.execute(sql)
                        # 提交到数据库执行
                        db.commit()
                    except:
                        # 如果发生错误则回滚
                        traceback.print_exc()
                        db.rollback()
                except Exception as Error: 
                    print Error
                try:
                    make_zip(pm25shpdir,pm25zippath+"\\"+PM25+".zip")
                except Exception as Error: 
                    print Error
                try:
                    RasterToPoint_conversion(vocdir,vocPointFeatures)
                    try:
                # 执行sql语句
                        sql='INSERT INTO newchangshu.ams_cssite (imagedate, layername, type, workspace, store) VALUES ({},{},{},{},{})'.format( timestamp,'"'+ VOC+'"', '"site"', '"cssite"', '"voc"')
                        #sql='insert into ams_sixindex values({},{},{},{},{},{})'.format(inspection_num,car_id,238,create_time,update_time)
                        cursor.execute(sql)
                        # 提交到数据库执行
                        db.commit()
                    except:
                        # 如果发生错误则回滚
                        traceback.print_exc()
                        db.rollback()
                except Exception as Error: 
                    print Error
                try:
                    make_zip(vocshpdir, voczippath+"\\"+VOC+".zip")
                except Exception as Error: 
                    print Error
    try:
        db.close()
    except:
        print('error')
                              
# 按掩模提取
def RasterToPoint_conversion(outRaster,inPointFeatures):
    inMaskData="F:\\result\\changshu\\cs.shp"
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