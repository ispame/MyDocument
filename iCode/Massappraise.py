# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import groupby
from operator import itemgetter
# import parawrap
import calendar
import datetime as dtm
import xlwt

def zoneAVE(mylist=a,windowwidth=1000,step =100,rate=0.5):
    '''
    :param mylist:
    :param windowwidth:
    :param step:
    :param rate:
    :return:  avg,mmin,mmax
    '''
    orderlist= np.sort(mylist)
    numlist = []
    # print orderlist

    if len(orderlist)==0:
        mmax= max(orderlist)
        mmin= min(orderlist)
        avg=np.average(orderlist)
    else:
        maxrange= orderlist[-1]- orderlist[0]
        if int(maxrange/step)>=1:
            for n in range(0,int(maxrange/step)):
                down=orderlist[0]+ step*n
                up= windowwidth+down
                numofwindow=0
                for i,value in enumerate(orderlist):
                    if value>=down and value <up:
                        numofwindow+=1
                numlist.append(numofwindow)
            renumlist = numlist[::-1]
            # maxix 最大的最多数量的index
            maxvalue= max(renumlist)
            maxix=len(renumlist)- np.argmax(renumlist)-1
            i=0
            while (numlist[maxix+i]>=maxvalue*rate) :
                i= i+1
                if maxix+i>len(numlist)-1:
                    break
            j=0
            while (numlist[maxix-j]>= maxvalue*rate):
                j= j+1
                if (maxix-j)<0:
                    break
            qualifiedlist=[]
            mmax= orderlist[0]+(maxix+i-1)*step+windowwidth
            mmin= orderlist[0]+ (maxix-j+1)*step
            for value in orderlist:
                if value>=mmin and value<mmax:
                   qualifiedlist.append(value)
            print numlist[maxix]
            print mmax,mmin,
            print "Testlist",qualifiedlist
            avg=np.average(qualifiedlist)
        # 样本密度集中，小于步长，无法移动。
        else:
            mmax= max(orderlist)
            mmin= min(orderlist)
            avg=np.average(orderlist)
    return avg,mmin,mmax


def last_day(i):
    '''
    #给任意datetime i, 半月最后一天判断
    '''
     if i.day>15:
        _,days_in_months=calendar.monthrange(i.year,i.month)
        return dtm.datetime(i.year,i.month,days_in_months)
     elif i.day<=15:
        return dtm.datetime(i.year,i.month,15)
def first_day(i)
    if i.day>15:
        return dtm.datetime(i.year,i.month,16)
    elif i.day<=15:
        return dtm.datetime(i.year,i.month,1)


def dd(sameMonthTable,i,data,maxPushTimes,miniCaseNum,onePush):
    pushtime=1
     # 添加最小样例数目
    avg=-1
    while sameMonthTable.shape[0]<miniCaseNum:
        start_day=i-dtm.timedelta(days=onePush*pushtime)
        end_day=last_day(i)+dtm.timedelta(days=1)
        sameMonthTable= data[(data.t>=start_day) & (data.t<end_day)]
        pushtime+=1
        # 达到最大前推次数，案例不够，
        if pushtime>=maxPushTimes:
            if sameMonthTable.shape[0]<miniCaseNum:
                sameMonthTable['price']=0
                print i ,"have not enough cases"
                avg=0
                break
    if avg<>0:
        avg,mmin,mmax= zoneAVE(sameMonthTable.price)
    return i,avg


def getcase_calcuAVG(data,miniCaseNum=10,maxPushTimes=12,onePush=5,appraisalTime= dtm.datetime(day=15, month=12,year=2016)):
    # 样本取样时间选择
    label_start=[]
    label_end=[]
    indexs=[]
    if appraisalTime.day==1:
        appraisalTime=appraisalTime-dtm.timedelta(days=1)
    data=data[data.t<=appraisalTime]
    # print "dddddddddddddddddddddddddddd"
    # print appraisalTime
    # print data
    for index,i in enumerate(data.t):
        # 后15天
        if i.day>15:
            k= dtm.datetime((i.year),(i.month), 16)
        # 前15天
        elif i.day<= 15:
            k= dtm.datetime((i.year),(i.month), 1)
        j=last_day(i)
        label_start.append(k)
        label_end.append(j)
        indexs.append(int(index))
    data['YM_start']=pd.DataFrame(label_start,index=indexs)
    data['YM_end'] =pd.DataFrame(label_end,index=indexs)
    by_YM=data.groupby(by='YM_start')
    # test
    # write_excel
    # writer=pd.ExcelWriter('bb.xlsx')
    # data.to_excel(writer,'sheetK')
    # writer.save()

    # if appraisalTime.day<15:
       # print  data[(data.t<=appraisalTime) & (data.t>appraisalTime-dtm.timedelta(15))]
    avglist=pd.Series()
    for i,sameMonthTable in by_YM:
        print i

        pushtime=1
         # 添加最小样例数目
        avg=-1
        while sameMonthTable.shape[0]<miniCaseNum:
            start_day=i-dtm.timedelta(days=onePush*pushtime)
            end_day=last_day(i)+dtm.timedelta(days=1)
            sameMonthTable= data[(data.t>=start_day) & (data.t<end_day)]
            pushtime+=1
            # 达到最大前推次数，案例不够，
            if pushtime>=maxPushTimes:
                if sameMonthTable.shape[0]<miniCaseNum:
                    sameMonthTable['price']=0
                    print i ,"have not enough cases"
                    avg=0
                    break

        if avg<>0:
            avg,mmin,mmax= zoneAVE(sameMonthTable.price)

        avglist.set_value(i,avg)

    # print avglist
    # print appraisalTime-dtm.timedelta(months=1)
    if appraisalTime.day<=15:
        avglist=avglist.drop(labels=dtm.datetime(appraisalTime.year,appraisalTime.month,1))
        avglist=avglist.drop(labels=dtm.datetime(appraisalTime.year,appraisalTime.month-1,16))
        i,avg=dd(sameMonthTable=data[(data.t<=appraisalTime) & (data.t>appraisalTime-dtm.timedelta(15))],i=i,data=data,maxPushTimes=maxPushTimes,miniCaseNum=miniCaseNum,onePush=onePush)
        avglist.set_value(i,avg)
        # print avglist
    elif appraisalTime.day>15:
        print dtm.datetime(appraisalTime.year,appraisalTime.month,16)
        # avglist=avglist.drop(labels=dtm.datetime(appraisalTime.year,appraisalTime.month,16))
        i,avg=dd(sameMonthTable=data[(data.t<=appraisalTime) & (data.t>appraisalTime-dtm.timedelta(15))],i=i,data=data,maxPushTimes=maxPushTimes,miniCaseNum=miniCaseNum,onePush=onePush)
        print "ddddd" ,data[(data.t<=appraisalTime) & (data.t>appraisalTime-dtm.timedelta(15))]
        avglist.set_value(i,avg)
        print avglist
    return avglist




def writexcel(data):
    myexcel = xlwt.Workbook(encoding = 'utf-8',style_compression=0)
    sheetA = myexcel.add_sheet('test',cell_overwrite_ok=True)

    for p,value in enumerate(data):

        print value
        for q in value:
             sheetA.write(p,q,value)

    myexcel.save(r'E:\Desktop\bb.xls')

#导入数据
def start_proc():
    '''
    get the data, calculate the avg，
    :return: 拟合值
    '''
    names=['id','name','type','dtype','layer','tlayer','area','totalprice','price','t','block']
    df= pd.read_excel(r'E:\MyWork\MyPcCharm\MrYangPro\a.xlsx',sheetname= 'Sheet2',header=None,names = names,skiprows=1)
    df['t'] = pd.to_datetime(df.t,format='%Y-%m-%d %H:%M:%S.%f')
    df.set_index(keys='t')


    # 板块、物业类型循环
    by_block_dtype= df.groupby(by= ['block','dtype'])
    for block_dtyep, datablock in by_block_dtype:
        for block in block_dtyep:
            print block
        # 小区循环
        by_name= df.groupby(by=['name'])
        blockRate=pd.Series()
        for name,df in by_name:
            print "                                     "
            print name
            df_time= pd.DataFrame(df,columns=['t','price'])
            # 排序
            sorted_data=df_time.sort_values(by='t')
            sort_ix_data=sorted_data.reset_index(drop=True)
            avglist= getcase_calcuAVG(data=sort_ix_data)
            # print "avglist",avglist
            blockRate.set_value(name,avglist)

        avg_blockRate,min_block, max_block= zoneAVE(blockRate,windowwidth=0.1,step=0.01,rate=0.5)
        print '最小值和最大值',min_block, max_block
        print avg_blockRate
        
    # print sort_ix_data
    def left_dfcol():
    # 对pandas 列进行字符串操作
        print df.t.str[0:7]
    def addlist():
    # 添加辅助列
        df_time['addtional']= df_time.name==df.name[0]
    #  剔除重复
    def dropduplicate(df):
         df.drop_duplicates

    # 筛选
    def filerx():
        print df_time[df_time.price>60000]
    def grouped():
        grouped= df.groupby(['id','dtype','block'])
        for table in grouped:
            # print table
            pass

start_proc()




