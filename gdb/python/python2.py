import arcgisscripting

gp = arcgisscripting.create(10.0)

gp.setProduct("ArcEngine")
GetAoModule('esriSystem.olb')

import comtypes.gen.esriSystem as esriSystem

pInit = AoObj(esriSystem.AoInitialize,esriSystem.IAoInitialize)

eProduct = esriSystem.esriLicenseProductCodeEngine 

licenseStatus = pInit.IsProductCodeAvailable(eProduct)

if licenseStatus == esriSystem.esriLicenseAvailable:

 pInit.Initialize(eProduct)

 
GetAoModule('esriGeoDatabase.olb')

import comtypes.gen.esriGeoDatabase as esriGeoDatabase

GetAoModule('esriDataSourcesFile.olb')

import comtypes.gen.esriDataSourcesFile as esriDataSourcesFile

GetAoModule('esriDataSourcesGDB.olb')

import comtypes.gen.esriDataSourcesGDB as esriDataSourcesGDB

GetAoModule('esriGeometry.olb')

import comtypes.gen.esriGeometry as esriGeometry

 

fileWorkspaceFactory=AoObj(esriDataSourcesFile.ShapefileWorkspaceFactory,esriGeoDatabase.IWorkspaceFactory)

pfw=fileWorkspaceFactory.OpenFromFile('D:/bysj/数据/四川矢量',0)

featureWorkspce = AoCType(pfw, esriGeoDatabase.IFeatureWorkspace)

featureClass=AoObj(esriGeoDatabase.FeatureClass,esriGeoDatabase.IFeatureClass)

featureClass=featureWorkspce.OpenFeatureClass("带市界.shp")

 

#选择所有要素

queryFilter2=AoObj(esriGeoDatabase.QueryFilter,esriGeoDatabase.IQueryFilter2)

queryFilter2.WhereClause =''

fs=featureClass.Search(queryFilter2,0)#0就是Fasle

featureCursor=AoCType(fs, esriGeoDatabase.IFeatureCursor)

#创建txt

f=open('D:/bysj/data/M值表.txt','w')

 

fc = featureCursor.NextFeature()

#循环输出每个线要素的所有结点的M值

while fc:    

    pFeat = AoCType(fc, esriGeoDatabase.IFeature)    

    ps=pFeat.Shape 

    pPl=AoCType(ps, esriGeometry.IPolyline)    

    pPC=AoCType(pPl, esriGeometry.IPointCollection)    

 

    f.write('OBJECTID  ' + ','+repr(pFeat.OID)+'\n')

    f.write('节点' + "," + '  M值'+'\n')

    for i in range(0,pPC.PointCount):

        ppct=pPC.Point[i]       

        pPoint =AoCType(ppct, esriGeometry.IPoint)

        ID=i+1

        f.write(repr(ID) + ",  " + repr(pPoint.M)+'\n')

    fc = featureCursor.NextFeature()

#关闭文件输入

f.close()