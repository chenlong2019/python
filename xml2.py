# coding=UTF-8
 
import xml.sax
class MovieHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.Name = ""
      self.Title = ""
      self.op = ""
      self.ol = ""
 
   # 元素开始事件处理
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "StyledLayerDescriptor":
         print "*****StyledLayerDescriptor*****"
         Name = attributes["NamedLayer"]
         print "NamedLayer:", Name
 
   # 元素结束事件处理
   def endElement(self, tag):
      if self.CurrentData == "Name":
         print "Name:", self.Name
      elif self.CurrentData == "Title":
         print "Title:", self.Title
      elif self.CurrentData == "ogc:PropertyName":
         print "ogc:PropertyName:", self.op
      elif self.CurrentData == "ogc:Literal":
         print "ogc:Literal:", self.ol
 
   # 内容事件处理
   def characters(self, content):
      self.Name = ""
      self.Title = ""
      self.op = ""
      self.ol = ""
      if self.CurrentData == "Name":
         self.Name = content
      elif self.CurrentData == "Title":
         self.Title = content
      elif self.CurrentData == "ogc:PropertyName":
         self.op = content
      elif self.CurrentData == "ogc:Literal":
         self.ol = content
  
if ( __name__ == "__main__"):
   
   # 创建一个 XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
 
   # 重写 ContextHandler
   Handler = MovieHandler()
   parser.setContentHandler( Handler )
   
   parser.parse("D:\\csys\\pm252019083009.sld")