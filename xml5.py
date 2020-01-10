# coding=utf-8
import xml.etree.ElementTree as ET   
tree = ET.parse(u"D:\\sld\\pm252019083009.sld")  
for NamedLayer in tree.iter(tag=u'NamedLayer'):
    Namelist=NamedLayer._children
    for Name in Namelist:
        if(Name.tag==u'Name'):
            Name.text=u"咖啡机公检法机关" 
for FeatureTypeStyle in tree.iter(tag=u'FeatureTypeStyle'):
    FeatureTypeNamelist=FeatureTypeStyle._children
    for FeatureTypeName in FeatureTypeNamelist:
        if(FeatureTypeName.tag==u'FeatureTypeName'):
            FeatureTypeName.text=u"咖啡机公检法机关"
    for i in range(1,11):
        Rule=FeatureTypeStyle._children[i]
        rclist=Rule._children
        for rc in rclist:
            if(rc.tag==u'Name'):
                rc.text=u"咖啡机公检法机关"
            if(rc.tag==u'Title'):
                rc.text=u"咖啡机公检法机关"
            if(rc.tag==u'{http://www.opengis.net/ogc}Filter'):
                # ns0:LowerBoundary
                rc._children[0]._children[1]._children[0].text='233'
                # ns0:LowerBoundary
                rc._children[0]._children[2]._children[0].text='677'
                print '1222'

for Rule in tree.iter(tag=u'Rule'):
    rclist=Rule._children
    for rc in rclist:
        if(rc.tag==u'Name'):
            rc.text=u"咖啡机公检法机关"
        if(rc.tag==u'Title'):
            rc.text=u"咖啡机公检法机关"
        if(rc.tag==u'{http://www.opengis.net/ogc}Filter'):
            # ns0:LowerBoundary
            rc._children[0]._children[1]._children[0].text='233'
            # ns0:LowerBoundary
            rc._children[0]._children[2]._children[0].text='677'
            print '1222'
tree.write(u"D:\\sld\\test\\test9.xml", encoding='utf-8', xml_declaration=True)  
