# -*- coding: utf-8 -*-

import pyodbc as odb
import numpy as np
import xlwt
import pandas as pd

def unicodeTostr():
    u='你好吗'
    s=u'不好'
    print u.decode('utf-8')+s
    print u+s.encode('utf-8')


def writexcel():
    myexcel = xlwt.Workbook(encoding = 'utf-8',style_compression=0)
    sheetA = myexcel.add_sheet('test',cell_overwrite_ok=True)
    sheetA.write(0,0,'content')
    sheetA.write(0,1,'中国人民有dddsaaaaaaaad力量'.decode('utf-8'))
    myexcel.save(r'E:\Desktop\bb.xls')


def sqlexcute(sql):
    DataConnStr = 'DRIVER={SQL Server};DATABASE=RiskAnalysis;SERVER=172.16.2.7;UID=Chao;PWD=123'
    DataConn=odb.connect(DataConnStr)
    DataCursor= DataConn.cursor()
    DataCursor.execute(sql)
    DataCursor.close()
    DataConn.close()



myexcel = xlwt.Workbook(encoding = 'utf-8',style_compression=0)
sheet1 = myexcel.add_sheet('sheet1',cell_overwrite_ok=True)
# 创建数据库连接
DataConnStr = 'DRIVER={SQL Server};DATABASE=RiskAnalysis;SERVER=172.16.2.7;UID=Chao;PWD=123'
DataConn=odb.connect(DataConnStr)
DataCursor= DataConn.cursor()
# 筛选数据
getTime= "'2017-01-05'"
getData_Query= 'SELECT * INTO #T1 FROM [RiskAnalysis].[dbo].[trainTickets] WHERE LEFT(getTime,10)= '
DataCursor.execute(getData_Query+getTime)
citylist_Query=r"SELECT  arrCity FROM #T1  GROUP BY arrCity  ORDER BY arrCity"
citytable=np.array(DataCursor.execute(citylist_Query).fetchall())

typecode=0
cityrow=0
for i in range(len(citytable)):
    for j in range(i+1,len(citytable)):
        aa= "'"+citytable[i][0]+"'"
        bb="'"+citytable[j][0]+"'"
        r= i+cityrow+ typecode
        sheet1.write(r,1,aa)
        sheet1.write(r,2,bb)
        sheet1.write(r,7,bb)
        sheet1.write(r,8,aa)
        print aa,bb
        x_Query= "SELECT trainType, CASE WHEN 1.0*notickNum/num IS NOT NULL THEN  1.0*notickNum/num ELSE 0 END AS scarcity,num FROM (SELECT LEFT(trainNo,1) AS trainType,COUNT(1) AS num\
                     FROM  #T1  WHERE dptCity = %s AND arrCity = %s GROUP BY  LEFT(trainNo,1))a LEFT JOIN\
                     (SELECT LEFT(trainNo,1) AS notickType,COUNT(1) AS notickNum\
                     FROM  #T1  WHERE dptCity =%s AND arrCity =%s AND totalTickets=0 GROUP BY  LEFT(trainNo,1))b ON\
                     a.trainType= b.notickType" % (aa,bb,aa,bb)
        x= np.array(DataCursor.execute(x_Query).fetchall())

        type1= typecode
        for m in x:
            # print m
            p= 3
            for k in m:
                r= i+cityrow+ type1
                sheet1.write(r,p,str(k))
                p=p+1
            type1=type1+1
        # print bb,aa
        y_Query= "SELECT trainType, CASE WHEN 1.0*notickNum/num IS NOT NULL THEN  1.0*notickNum/num ELSE 0 END AS scarcity,num FROM (SELECT LEFT(trainNo,1) AS trainType,COUNT(1) AS num\
                     FROM  #T1  WHERE dptCity = %s AND arrCity = %s GROUP BY  LEFT(trainNo,1))a LEFT JOIN\
                     (SELECT LEFT(trainNo,1) AS notickType,COUNT(1) AS notickNum\
                     FROM  #T1  WHERE dptCity =%s AND arrCity =%s AND totalTickets=0 GROUP BY  LEFT(trainNo,1))b ON\
                     a.trainType= b.notickType" % (bb,aa,bb,aa)
        y= np.array(DataCursor.execute(y_Query).fetchall())
        for n in y:
            # print n
            q=9
            for l in n:
                r= i+cityrow+ typecode
                sheet1.write(r,q,str(l))
                q=q+1
            typecode=typecode+1
        if typecode< type1:
            typecode= type1

        # print '#####################################################'
        cityrow =cityrow+1
DataCursor.close()
DataConn.close()

myexcel.save(r'E:\Desktop\bb.xls')


def sqldecode():
    y_Query=r"SELECT top 100 * FROM  #T1 where dptCity= '北京'".decode('utf8')
    y= np.array(DataCursor.execute(y_Query).fetchall())
    print y_Query
    print y.shape