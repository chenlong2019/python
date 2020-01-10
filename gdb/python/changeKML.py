import os
dirname='D:\\bysj\\data\\KMLDataLoading\\'
li=os.listdir(dirname)
for filename in li:
    newname=filename
    newname=newname.split('.')
    if newname[-1]=='kml':
        newname[-1]='txt'
        newname=newname[-2]+'.'+newname[-1]
        filename=dirname+filename
        newname=dirname+newname
        os.rename(filename,newname)
        print(newname,'Updated Successfully')