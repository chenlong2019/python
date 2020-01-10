# coding=utf-8
import numpy as np 
import os
import pandas as pd
import csv,time,traceback
station_LonLat = u'F:\\eightdata\\1025\\station.xls'
station = pd.read_excel(station_LonLat)
Lon = list(station['LON'].values)
Lat = list(station['LAT'].values)
statlist=[u'海虞子站',u'菱塘子站',u'兴福子站',u'福山子站',u'沿江子站',u'东南子站',u'琴湖子站',u'湖东子站',u'常福子站',u'莫城子站',u'梅李子站',u'辛庄子站',u'支塘子站',u'沙家浜子站',u'董浜子站',u'尚湖子站',u'古里子站']

def getHourPath(hour):
    dt=time.strftime('%m%d',time.localtime(time.time()))
    ho=str(hour) if (hour>9) else '0'+str(hour)
    print(dt+ho)
    return dt+ho


# 写入csv文件
def readCsv(file,xlsfile,h,date):
    filename=os.path.split(file)[1][:-4]
    data = pd.read_csv(file,encoding='gbk')
    header=[u'date',u'hour',u'type',u'1142A',u'1143A',u'1144A',u'1145A',u'1146A',u'1147A',u'1148A',u'1149A',u'1150A',u'1151A',u'1152A',u'1153A',u'1154A',u'1155A',u'1156A',u'1157A',u'1158A',u'1159A',u'1160A',u'1161A',u'1162A',u'1163A',u'1164A',u'1165A',u'1166A',u'1167A',u'1168A',u'1169A',u'1170A',u'1171A',u'1172A',u'1184A',u'1185A',u'1186A',u'1187A',u'1188A',u'1189A',u'1193A',u'1194A',u'1195A',u'1196A',u'1197A',u'1198A',u'1199A',u'1200A',u'1201A',u'1203A',u'1204A',u'1205A',u'1206A',u'1207A',u'1208A',u'1209A',u'1223A',u'1224A',u'1226A',u'1227A',u'1228A',u'1229A',u'1230A',u'1231A',u'1232A',u'1233A',u'1234A',u'1235A',u'1236A',u'1237A',u'1239A',u'1240A',u'1241A',u'1246A',u'1247A',u'1248A',u'1249A',u'1250A',u'1251A',u'1252A',u'1253A',u'1258A',u'1259A',u'1260A',u'1794A',u'1795A',u'1796A',u'1797A',u'1798A',u'1799A',u'1800A',u'1801A',u'1802A',u'1985A',u'1986A',u'1987A',u'1988A',u'1989A',u'1990A',u'1991A',u'1992A',u'1993A',u'1994A',u'1995A',u'1996A',u'1997A',u'1998A',u'1999A',u'2000A',u'2001A',u'2002A',u'2003A',u'2004A',u'2005A',u'2006A',u'2007A',u'2008A',u'2009A',u'2010A',u'2011A',u'2012A',u'2013A',u'2016A',u'2017A',u'2285A',u'2286A',u'2287A',u'2288A',u'2289A',u'2290A',u'2295A',u'2296A',u'2297A',u'2298A',u'2299A',u'2300A',u'2316A',u'2317A',u'2318A']
    rows=data[[u'date',u'hour',u'type','1142A',u'1143A',u'1144A',u'1145A',u'1146A',u'1147A',u'1148A',u'1149A',u'1150A',u'1151A',u'1152A',u'1153A',u'1154A',u'1155A',u'1156A',u'1157A',u'1158A',u'1159A',u'1160A',u'1161A',u'1162A',u'1163A',u'1164A',u'1165A',u'1166A',u'1167A',u'1168A',u'1169A',u'1170A',u'1171A',u'1172A',u'1184A',u'1185A',u'1186A',u'1187A',u'1188A',u'1189A',u'1193A',u'1194A',u'1195A',u'1196A',u'1197A',u'1198A',u'1199A',u'1200A',u'1201A',u'1203A',u'1204A',u'1205A',u'1206A',u'1207A',u'1208A',u'1209A',u'1223A',u'1224A',u'1226A',u'1227A',u'1228A',u'1229A',u'1230A',u'1231A',u'1232A',u'1233A',u'1234A',u'1235A',u'1236A',u'1237A',u'1239A',u'1240A',u'1241A',u'1246A',u'1247A',u'1248A',u'1249A',u'1250A',u'1251A',u'1252A',u'1253A',u'1258A',u'1259A',u'1260A',u'1794A',u'1795A',u'1796A',u'1797A',u'1798A',u'1799A',u'1800A',u'1801A',u'1802A',u'1985A',u'1986A',u'1987A',u'1988A',u'1989A',u'1990A',u'1991A',u'1992A',u'1993A',u'1994A',u'1995A',u'1996A',u'1997A',u'1998A',u'1999A',u'2000A',u'2001A',u'2002A',u'2003A',u'2004A',u'2005A',u'2006A',u'2007A',u'2008A',u'2009A',u'2010A',u'2011A',u'2012A',u'2013A',u'2016A',u'2017A',u'2285A',u'2286A',u'2287A',u'2288A',u'2289A',u'2290A',u'2295A',u'2296A',u'2297A',u'2298A',u'2299A',u'2300A',u'2316A',u'2317A',u'2318A']]
    rows=np.array(rows.fillna(0).values)
    lists=[]
    pm25list=[]
    for row in rows:
        # row[2]==u'AQI' or 
        if int(row[1])==int(h) and row[2]==u'PM2.5':
            pm25list.append(row)
    pm25list=np.array(pm25list).transpose()[3:139]
    pm25xlslist=[]
    site = list(station[u'监测点编码'].values)
    for i in range(0,136): 
        print(site[i] +'------------------{}'.format(pm25list[i][0]))
        if pm25list[i][0]>0:
            pm25_station_data = [site[i] , float(pm25list[i][0]) , float(Lon[i]) , float(Lat[i])]
            pm25xlslist.append(pm25_station_data)
        else:
            print('---------------------------'+site[i]+str(h)+'时'+'无PM25数据----------------------------')
    cspm25list=getList(xlsfile,h,date,pm25xlslist)
    pm25_out_data = np.array(cspm25list)
    pm25_out_columns = [u'站点 ','PM25' ,u'Long',u'Lat']
    pm25_out_data = pd.DataFrame(pm25_out_data,columns=pm25_out_columns)
    # columns that can be converted to number(int,float) types will be converted,
    # while columns that cannot (for example, they contain non-digital strings or dates) will be retained separately.
    pm25_out_data = pm25_out_data.apply(pd.to_numeric, errors= "ignore")
    pm25_outname = 'PM25'+'_'+date+(str(h) if (h>9) else '0'+str(h))+'.xls'
    ymd=time.strftime('%Y%m%d',time.localtime(time.time()))
    pm25_out_file="F:\\eidata\\20191102\\PM25\\11"+date+"\\"+pm25_outname
    try:
        os.makedirs("F:\\eidata\\20191102\\PM25\\11"+date)
    except :
        pass
    try:
        pm25_out_data.to_excel(pm25_out_file,sheet_name='Sheet1')
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(normaltime+":"+pm25_outname+"  创建成功")
    except Exception as err:
        print(pm25_out_file+" 创建失败")
        print(pm25_out_file+" "+err.message)
        traceback.print_exc()

def getList(xlsfile,h,date,pm25xlslist):
    df=pd.read_excel(xlsfile,encoding='gbk')
    data=df[[u'测点',u'日期',u'PM2.5(μg/m3)',u'PM10(μg/m3)',u'二氧化硫(μg/m3)',u'二氧化氮(μg/m3)',u'一氧化碳(mg/m3)',u'臭氧(μg/m3)']]
    rows=np.array(data.fillna(0).values)
    hour=str(h) if (h>9) else '0'+str(h)
    for row in rows:
        if(row[1]=='2019-10-'+date+' '+hour+':00:00'):
            i=statlist.index(row[0])
            if(row[2]>0):
                pm25_station_data = [row[0] , float(row[2]) , float(Lon[i+136]) , float(Lat[i+136])]
                pm25xlslist.append(pm25_station_data)
    return pm25xlslist
    
if __name__ == '__main__':
    print('------------------ Hello World ------------------------')
    date='29'
    print('------------------ '+date+' ------------------------')
    csvfile=u'F:\\eidata\\20191029\\china_sites_20191029.csv'
    xlsfile=u'F:\\eidata\\20191029\\20191029122107.xls'
    print('------------------ Hello World ------------------------')
    for i in range(11,12):
        print('------------------ '+str(i)+' -----------------------------')
        try:
            readCsv(csvfile,xlsfile,i,date)
        except:
            traceback.print_exc()
    for i in range(14,15):
        print('------------------ '+str(i)+' -----------------------------')
        try:
            readCsv(csvfile,xlsfile,i,date)
        except:
            traceback.print_exc()
   