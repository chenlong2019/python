path='D:\\bysj\\file\\chen.gdb'
fd='FirstRd'
def createRD(path,fd):
    import arcpy
    import os
    from arcpy import env
    env.overwriteOutput=True
    env.workspace=path
    if arcpy.Exists(fd):
        print(fd+' dataset already exists!')
    else:
        fd=arcpy.CreateRasterDataset_management(path,fd)
    return fd
fd=createRD(path,fd)