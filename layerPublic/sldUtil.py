# coding=utf-8
# 按固定值划分等级
import xml.etree.ElementTree as ET 
def createSLD(rastername,outSLDPath):
    tree = ET.parse(u"D:\\sld\\vocmoudle.sld")
    for NamedLayer in tree.iter(tag='NamedLayer'):
        Namelist=NamedLayer._children
        for Name in Namelist:
            if(Name.tag==u'Name'):
                Name.text=rastername
    for FeatureTypeStyle in tree.iter(tag='FeatureTypeStyle'):
        FeatureTypeNamelist=FeatureTypeStyle._children
        for FeatureTypeName in FeatureTypeNamelist:
            if(FeatureTypeName.tag==u'FeatureTypeName'):
                FeatureTypeName.text=rastername          
    tree.write(outSLDPath+"\\"+rastername+".sld", encoding='utf-8', xml_declaration=True) 