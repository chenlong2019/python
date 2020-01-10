# coding=utf-8
import xml.etree.ElementTree as ET 
def createSLD(rastername,elevMAXIMUM,elevMINIMUM,outSLDPath):
    tree = ET.parse(u"D:\\sld\\pm252019083009.sld")
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
    leng=(elevMAXIMUM-elevMINIMUM)/10
    for i in range(0,10):
        min=str(elevMINIMUM+leng*i+0.000000001)
        max=str(elevMINIMUM+leng*(i+1))
        Rule=FeatureTypeStyle._children[i+1]
        rclist=Rule._children
        for rc in rclist:
            if(rc.tag==u'Name'):
                rc.text=min+"-"+max
            if(rc.tag==u'Title'):
                rc.text=min+"-"+max
            if(rc.tag==u'{http://www.opengis.net/ogc}Filter'):
                # ns0:LowerBoundary
                rc._children[0]._children[1]._children[0].text=min
                # ns0:LowerBoundary
                rc._children[0]._children[2]._children[0].text=max
                
    tree.write(outSLDPath+"\\"+rastername+".sld", encoding='utf-8', xml_declaration=True) 