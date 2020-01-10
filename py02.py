import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
import pandas as pd
import os
f=os.path.join("F:\result\orag\20190812","数据查询20190812090440.xls")
print(unicode(f,"gb18030"))
df=pd.read_excel(f.decode('utf8'))
sss="数据查询20190812090440.xls"
print sss[-18:]