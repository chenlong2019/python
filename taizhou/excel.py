# coding=utf-8
# 处理excel，提取站点数据
import numpy as np 
import arcpy,os
import pandas as pd
import csv,time,traceback
station_LonLat = u'F:\\taizhou\\tzstation.xls'
station = pd.read_excel(station_LonLat)
Lon = list(station['LON'].values)
Lat = list(station['LAT'].values)
site = list(station[u'station'].values)
siteindex = list(station[u'stationindex'].values)

def getHourPath(hour):
    dt=time.strftime('%m%d',time.localtime(time.time()))
    ho=str(hour) if (hour>9) else '0'+str(hour)
    print(dt+ho)
    return dt+ho

# 写入csv文件
def readCsv(file,h):
    fields='PM25'
    filename=os.path.split(file)[1][:-4]
    data = pd.read_csv(file,encoding='gbk')
    header=[u'date',u'hour',u'type',u'1151A',u'1152A',u'1153A',u'1154A',u'1155A',u'1156A',u'1157A',u'1158A',u'1159A',u'1160A',u'1161A',u'1162A',u'1163A',u'1164A',u'1165A',u'1166A',u'1167A',u'1168A',u'1169A',u'1170A',u'1171A',u'1172A',u'1184A',u'1185A',u'1186A',u'1187A',u'1188A',u'1189A',u'1190A',u'1191A',u'1192A',u'1193A',u'1194A',u'1195A',u'1196A',u'1197A',u'1198A',u'1199A',u'1200A',u'1201A',u'1203A',u'1204A',u'1205A',u'1206A',u'1207A',u'1208A',u'1209A',u'1210A',u'1211A',u'1212A',u'1213A',u'1214A',u'1215A',u'1216A',u'1217A',u'1218A',u'1985A',u'1986A',u'1987A',u'1988A',u'1989A',u'1990A',u'1991A',u'1992A',u'1993A',u'1994A',u'1995A',u'1996A',u'1997A',u'1998A',u'1999A',u'2000A',u'2001A',u'2002A',u'2003A',u'2004A',u'2005A',u'2006A',u'2007A',u'2008A',u'2009A',u'2298A',u'2299A',u'2300A']
    rows=data[[u'date',u'hour',u'type',u'1151A',u'1152A',u'1153A',u'1154A',u'1155A',u'1156A',u'1157A',u'1158A',u'1159A',u'1160A',u'1161A',u'1162A',u'1163A',u'1164A',u'1165A',u'1166A',u'1167A',u'1168A',u'1169A',u'1170A',u'1171A',u'1172A',u'1184A',u'1185A',u'1186A',u'1187A',u'1188A',u'1189A',u'1190A',u'1191A',u'1192A',u'1193A',u'1194A',u'1195A',u'1196A',u'1197A',u'1198A',u'1199A',u'1200A',u'1201A',u'1203A',u'1204A',u'1205A',u'1206A',u'1207A',u'1208A',u'1209A',u'1210A',u'1211A',u'1212A',u'1213A',u'1214A',u'1215A',u'1216A',u'1217A',u'1218A',u'1985A',u'1986A',u'1987A',u'1988A',u'1989A',u'1990A',u'1991A',u'1992A',u'1993A',u'1994A',u'1995A',u'1996A',u'1997A',u'1998A',u'1999A',u'2000A',u'2001A',u'2002A',u'2003A',u'2004A',u'2005A',u'2006A',u'2007A',u'2008A',u'2009A',u'2298A',u'2299A',u'2300A']]
    rows=np.array(rows.fillna(0).values)
    vallists=[]
    for row in rows:
        # row[2]==u'AQI' or 
        if int(row[1])==int(h) and row[2]==u'PM2.5':
            vallists.append(row)
    vallists=np.array(vallists).transpose()[3:87]
    xlslist=[]  
    for i in range(0,84): 
        print(vallists[i][0])     
        if vallists[i][0]>0:
            station_data = [siteindex[i],site[i] , float(vallists[i][0]) , float(Lon[i]) , float(Lat[i])]
            xlslist.append(station_data)
        else:
            arcpy.AddMessage('---------------------------'+site[i]+str(h)+'时'+'无'+fields+'数据----------------------------')
    out_data = np.array(xlslist)
    out_columns = [u'监测点编码',u'站点 ',fields ,u'Long',u'Lat']
    out_data = pd.DataFrame(out_data,columns=out_columns)
    out_data = out_data.apply(pd.to_numeric, errors= "ignore")
    outname = fields+'_'+getHourPath(h)+'.xls'
    ymd=time.strftime('%Y%m%d',time.localtime(time.time()))
    filepath="F:\\taizhou\\"+'20191010'
    try:
        os.makedirs(filepath)
    except :
        pass
    out_file=filepath+"\\"+outname
    try:
        out_data.to_excel(out_file,sheet_name='Sheet1')
        normaltime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        arcpy.AddMessage(normaltime+":"+outname+"  创建成功")
    except Exception as err:
        arcpy.AddMessage(out_file+" 创建失败")
        arcpy.AddMessage(out_file+" "+err.message)
        traceback.print_exc()
    
if __name__ == '__main__':
    csvfile='F:\\taizhou\\china_sites_20191010.csv'
    for h in range(10,18):
        print '------------------ Hello World ------------------------'
        print '------------------ '+str(h)+' -----------------------------'
        try:
            readCsv(csvfile,h)
        except:
            traceback.print_exc()