import xml.etree.cElementTree as ET
a = ET.Element('elem')
c = ET.SubElement(a, 'child1')
c.text = "some text"
d = ET.SubElement(a, 'child2')
b = ET.Element('elem_b')
root = ET.Element('root')
root.extend((a, b))
tree = ET.ElementTree(root)
tree.write("D:\\sld\\test\\test1.sld")