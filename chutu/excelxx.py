# coding=utf-8
import numpy as np 
import os
import pandas as pd
import csv,time,traceback
station_LonLat = u'E:\\新乡爬虫\\新乡周边监测点.xls'
station = pd.read_excel(station_LonLat)
Lon = list(station[u'经度'].values)
Lat = list(station[u'纬度'].values)

# 写入csv文件
def readCsv(file,h,date,val,zField):
    filename=os.path.split(file)[1][:-4]
    data = pd.read_csv(file,encoding='gbk')
    header=[u'date',u'hour',u'type','1316A',u'1317A',u'1318A',u'1319A',u'1320A',u'1321A',u'1322A',u'1323A',u'1324A',u'1718A',u'1719A',u'1720A',u'1727A',u'1728A',u'1729A',u'1730A',u'1731A',u'1818A',u'1819A',u'1820A',u'1821A',u'1822A',u'1823A',u'1824A',u'1825A',u'1826A',u'1827A',u'1828A',u'1829A',u'1830A',u'2160A',u'2161A',u'2162A',u'2163A',u'2164A',u'2165A',u'2385A',u'2386A',u'2387A',u'2388A',u'2389A',u'2390A',u'2391A',u'2392A',u'2393A',u'2394A',u'2395A',u'2845A']
    rows=data[[u'date',u'hour',u'type','1316A',u'1317A',u'1318A',u'1319A',u'1320A',u'1321A',u'1322A',u'1323A',u'1324A',u'1718A',u'1719A',u'1720A',u'1727A',u'1728A',u'1729A',u'1730A',u'1731A',u'1818A',u'1819A',u'1820A',u'1821A',u'1822A',u'1823A',u'1824A',u'1825A',u'1826A',u'1827A',u'1828A',u'1829A',u'1830A',u'2160A',u'2161A',u'2162A',u'2163A',u'2164A',u'2165A',u'2385A',u'2386A',u'2387A',u'2388A',u'2389A',u'2390A',u'2391A',u'2392A',u'2393A',u'2394A',u'2395A',u'2845A']]
    rows=np.array(rows.fillna(0).values)
    lists=[]
    pm25list=[]
    for row in rows:
        # row[2]==u'AQI' or 
        if int(row[1])==int(h) and row[2]==val:
            pm25list.append(row)
    pm25list=np.array(pm25list).transpose()[3:50]
    pm25xlslist=[]
    site = list(station[u'监测点编码'].values)
    for i in range(0,47): 
        pm25_station_data = [site[i] , float(pm25list[i][0]) , float(Lon[i]) , float(Lat[i])]
        pm25xlslist.append(pm25_station_data)
    # 常熟市环保局数据，新乡可注释
    # 新乡将cspm25list替换为pm25xlslist
    pm25_out_data = np.array(pm25xlslist)
    pm25_out_columns = [u'站点 ',zField ,u'Long',u'Lat']
    pm25_out_data = pd.DataFrame(pm25_out_data,columns=pm25_out_columns)
    # columns that can be converted to number(int,float) types will be converted,
    # while columns that cannot (for example, they contain non-digital strings or dates) will be retained separately.
    pm25_out_data = pm25_out_data.apply(pd.to_numeric, errors= "ignore")
    pm25_outname = zField+'_'+date+(str(h) if (h>9) else '0'+str(h))+'.xls'
    ymd=time.strftime('%Y%m%d',time.localtime(time.time()))
    pm25_out_file="E:\\xxeidata\\{}\\11{}\\{}".format(zField,date,pm25_outname)
    try:
        os.makedirs("E:\\xxeidata\\{}\\11{}".format(zField,date))
    except:
        pass
    try:
        pm25_out_data.to_excel(pm25_out_file,sheet_name='Sheet1')
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(normaltime+":"+pm25_outname+"  创建成功")
    except Exception as err:
        print(pm25_out_file+" 创建失败")
        print(pm25_out_file+" "+err.message)
        traceback.print_exc()
    
if __name__ == '__main__':
    for i in range(28,29):
        print('------------------ Hello World ------------------------')
        date='{}'.format(i)
        print('------------------ '+date+' ------------------------')
        csvfile=u'E:\\新乡爬虫\\china_sites_201911{}.csv'.format(date)
        print('------------------ Hello World ------------------------')
        for j in range(0,24):
            try:
                # readCsv(csvfile,xlsfile,j,date)
                readCsv(csvfile,j,date,'PM2.5','PM25')
                readCsv(csvfile,j,date,'PM10','PM10')
                #readCsv(csvfile,j,date,'SO2','SO2')
                #readCsv(csvfile,j,date,'NO2','NO2')
                #readCsv(csvfile,j,date,'CO','CO')
                #readCsv(csvfile,j,date,'O3','O3')
            except:
                traceback.print_exc()
   