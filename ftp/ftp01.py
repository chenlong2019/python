#coding: utf-8
from ftplib import FTP
import time
import tarfile
from tqdm import *
import traceback
import os
#!/usr/bin/python
#-*- coding: utf-8 -*-

from ftplib import FTP

def ftpconnect(host, username, password):
    ftp = FTP()
    #ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
    ftp.connect(host, 21)          #连接
    ftp.login(username, password)  #登录，如果匿名登录则用空串代替即可
    return ftp 

def isDir(filename):
    path = filename
    path.replace('/','\\')
    try:
        os.makedirs(path)        
        return True
    except:
        return False

def downloadfile(ftp):    
    print(ftp.getwelcome()) #显示ftp服务器欢迎信息
    with tqdm(range(811,830), ncols=90) as t:
            for i in t:
                try:
                    path="0"+str(i)
                    li = ftp.nlst(path)
                    for eachfile in li:
                        localpath = 'F:\\hexin\\'+path
                        print('-- open localpath --'+localpath)
                        bufsize = 1024
                        isDir(localpath)
                        if os.path.exists(localpath+"\\"+eachfile):
                            continue
                        fp = open(localpath+"\\"+eachfile,'wb')
                        ftp.retrbinary('RETR {}'.format(path+"\\"+eachfile),fp.write,bufsize)
                        fp.flush()
                except Exception as Error:
                    print(Error)          
    ftp.set_debuglevel(0) #关闭调试
    ftp.quit() #退出ftp服务器  
    ftp.close()
                             

if __name__ == "__main__":
    ftp = ftpconnect("122.114.63.177", "hexin", "HexinFtp@2019")
    ftp.encoding="utf-8"
    downloadfile(ftp)