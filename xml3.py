# -*- coding: UTF-8 -*-
 
from xml.dom.minidom import parse
import xml.dom.minidom

 
# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("D:\\csys\\pm252019083009.sld")
collection = DOMTree.documentElement
if collection.hasAttribute("Rule"):
   print "Root element : %s" % collection.getAttribute("Rule")
 
# 在集合中获取所有电影
movies = collection.getElementsByTagName("Rule")
 
# 打印每部电影的详细信息
for movie in movies:
   print "*****Rule*****"
   if movie.hasAttribute("Name"):
      print "Name: %s" % movie.getAttribute("Name")
 
   type = movie.getElementsByTagName('Name')[0]
   print "Name: %s" % type.childNodes[0].data
   format = movie.getElementsByTagName('Title')[0]
   print "Title: %s" % format.childNodes[0].data