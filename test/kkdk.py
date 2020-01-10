# coding=utf-8
with open('D:\\chrome\\citydata.txt',"r",encoding='utf-8') as f:    #设置文件对象
    straa = f.read()
    aa=straa.encode('utf-8').decode()
    print(aa)