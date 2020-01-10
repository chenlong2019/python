from bs4 import BeautifulSoup
import requests
import csv
import re
 
#调用百度地图API查询位置
def getlocation(name):
    bdurl='http://api.map.baidu.com/geocoder/v2/?address='
    output='json'
    ak='8X1KwIIVjO4H9FPuSmueH92wRRM3HrxB'#输入百度地图上申请的密匙,代码如果给别人，这个密钥一定要删掉
    callback='showLocation'
    uri=bdurl+name+'&output=t'+output+'&ak='+ak+'&callback='+callback
    headers = {'Connection': 'close'}
    res=requests.get(uri,headers = headers)
    s=BeautifulSoup(res.text,'lxml')
    lng=s.find('lng')#经度
    lat=s.find('lat')#纬度
    if lng:
        return lng.get_text()+','+lat.get_text()
 
 
#将csv文件中的地址读取出来并构建成一个list
with open('result.csv','r',newline='',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    data = []
    for row in reader:
        try:
            data.append((row[0]))
        except:
            pass
        
#print(data)
 
 
#houses=[]#定义列表用于存放房子的信息
 
#特别注意一个问题，当查询的数据量大时（len(p)约>900时），会出现ConnectionAbortedError问题，查了一下有人说了异步提交的问题
#也有人说是电脑防火墙等软件的问题阻止的,经过自己的尝试，最后锁定是并发问题，普通API用户的并发是60/秒，认证用户是160/秒，需要设置休眠
import time
n=1
num=len(data)-1#去掉标题行
file=open('yyc.csv', 'w', newline='')#自己定义一个文件yyc，用于备份保存地址、经纬度信息
headers = ['name', 'loc', 'count']
writers = csv.DictWriter(file, headers)
writers.writeheader()
while n<num:#循环将信息存放进列表
    name = data[n]
    loc = getlocation(name)
    house = {
        'name': '',
        'loc': '',
        'count': ''
    }
    #将房子的信息放进一个dict中
    house['name'] = name
    house['loc'] = loc
    house['count'] = 10
    writers.writerow(house)#将dict写入到csv文件中
    n+=1
    if n%100 == 0:
        time.sleep(10) #避免ConnectionAbortedError问题
        print(n)
file.close()
 
#将坐标按照百度API的格式进行整理
import csv
 
reader=csv.reader(open('yyc.csv'))
for row in reader:
    loc=row[1]
    sloc=loc.split(',')
    lng=''
    lat=''
    if len(sloc)==2:#第一行是列名需要做判断
        lng=sloc[0]
        lat=sloc[1]
        count='30'
        #row[2]
        out='{\"lng\":'+lng+',\"lat\":'+lat+',\"count\":'+count+'},'
        print(out)