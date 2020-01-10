import xlrd  #引入模块
 
#打开文件，获取excel文件的workbook（工作簿）对象
workbook=xlrd.open_workbook("F:\\pytserver\\company.xls")  #文件路径
#获取所有sheet的名字
names=workbook.sheet_names()
print(names) #['各省市', '测试表']  输出所有的表名，以列表的形式

