# coding=utf-8
import arcpy
import os,time
import csv
def create_csv(rows,path):
    with open(path,'wb') as f:
        csv_write = csv.writer(f)
        csv_head = [u"时间",u"环保西院",u"环保东院",u"开发区",u"市委党校"]
        csv_write.writerow(csv_head)
        csv_write.writerows(rows)


if __name__ == '__main__':
    # 文件目录
    arcpy.env.workspace = "C:/Workspace"
    path=u"F:\\数据\\lsat\\LC81660522019274LGN00"
    filelist=os.listdir(path)
    rows=[]
    for filename in filelist:
        filepath=os.path.join(path,filename)
        if filepath[-4:].lower() == '.tif':
            try:
                points=["286232.457 1266004.205","286242.457 1266004.205","286252.457 1266004.205","286262.457 1266004.205"]
                name=filename[:-4]
                row=[name]
                for point in points:
                    result = arcpy.GetCellValue_management(filepath, point)
                    cellvalue = int(result.getOutput(0))
                    row.append(cellvalue)
                rows.append(row)
            except:
                pass
    csvpath=u'E:\\csv\\{}.csv'.format(int(time.time()))
    create_csv(rows,csvpath)