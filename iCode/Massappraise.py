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

#可以删掉
def zoneAve1(data,b=1000,a=100):
    '''
    区间移动，剔除异常值，计算平均值
    '''
    orderlist= np.sort(data)
    count = []
    dif= orderlist[-1]- orderlist[0]
    for n in range(1,dif/100):

        for i,value in enumerate(orderlist):
            basedata= orderlist[0]+ n*a
            topdata= orderlist[0]+n*a+b
            if basedata <=i and  i <= topdata:
                number=number+1
        # if number!=0.0:
        count.append(number)
    # 拿到最远以个最大值的区间位置
    recount = count[::-1]
    n=len(recount)- np.argmax(recount)-1
    i=0
    while (count[n+i]>= max(count)/2) :
        i= i+1
        if len(count)>=n+i:
            break
    j=0
    while (count[n-j]>= max(count)/2):
        j= j+1
        if (n-j-1)<=0:
            break
    mylist=[]
    for m in orderlist:
        mmax= orderlist[0]+(n+i-1)*a+b
        mmin= orderlist[0]+ (n-j+1)*a
        if orderlist[0]+(n+i-1)*a+b>=m and  m>=orderlist[0]+ (n-j+1)*a:
            mylist.append(m)
    return np.average(mylist)





a=[23715.00,23715.00,22500.00,22500.00,23334.00,22364.00,26286.00,29167.00,30000.00,22500.00,25410.00,22858.00,28000.00,30000.00,30556.00,23143.00,27587.00,25715.00,27500.00,28000.00,30685.00,32512.00,35850.00,22728.00,23685.00,30685.00,30882.00,34286.00,43479.00,23750.00,34723.00,22059.00,22223.00,22223.00,22369.00,25000.00,34723.00,24000.00,26487.00,27006.00,30858.00,34723.00,34723.00]




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

        # 判断样本密度集中，大于步长，至少可以进行一次移动。
        if int(maxrange/step)>=1:
        # print orderlist
        # n represent the number of move-window times
            for n in range(0,int(maxrange/step)):
                down=orderlist[0]+ step*n
                up= windowwidth+down
                # print down,up,maxrange/step, orderlist[-1]
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
            #  for test ()
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
# print zoneAVE()


def AES(data, beta=0.1):

    '''
    自适应指数平滑
    :rtype: object
    '''
    S = []
    s = data[0]
    E = 1
    M = 1
    for each in data:
        y = each
        e = y - s
        E = beta * e + (1 - beta) * E
        M = beta * abs( e ) + (1 - beta) * M
        T = E / float(M)
        a = abs(T)
        s = a * y + (1 - a) * s
        S.append(s)
    return S

'''
def findcase(data,leastCaseNum=10,day=5,time=3):

    if casenum<leastCaseNum:
        push day
        add.case
'''


def get_nearAvg(aa):
    '''
        #补充拟合值
    '''
    nonzeroix=pd.Series()
    i=0
    for ix,avg in enumerate(aa):
        if avg<>0.0:
            nonzeroix.set_value(i,value=ix)
            i+=1
    for index,avg in enumerate(aa):
        if avg==0.0:
            ixx=minstance(index,nonzeroix)
            if ixx==None:
                aa[index]=0
            # print index, ixx
            # print aa[ixx]
            else:
                aa[index] = aa[ixx]
    return aa


def draw(aa,ss):
    plt.plot(aa)
    plt.plot(ss)
    # plt.plot(cc)
    plt.show()


def minstance(index,listIx):
    '''
    return 距离list index 最近的index(同等情况去向前一个月)
    '''
    minD= 10000000
    minX=None
    for ix in listIx:
        dd= ix-index
        if dd<0:
            dd = -dd-0.5
        if dd<minD:
            minD=dd
            minX = ix
    return minX




def last_day(i):
     if i.day>15:
        _,days_in_months=calendar.monthrange(i.year,i.month)
        return dtm.datetime(i.year,i.month,days_in_months)
     elif i.day<=15:
        return dtm.datetime(i.year,i.month,15)




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
    # sheetA.write(0,1,'中国人民有dddsaaaaaaaad力量'.decode('utf-8'))
    myexcel.save(r'E:\Desktop\bb.xls')
'''
def getrate(dat):
    data=dat
    avglist= getcase_calcuAVG(data=data)
    # print "avglist",avglist
    aa=list(avglist.fillna(value=0))
    cc=['{:.2f}'.format(i) for i in aa]
    print 'aa1',cc
    # 补充拟合值
    aa=get_nearAvg(aa)
    s = AES(aa, beta=0.3)
    ss = AES(s, beta=0.1)
    cc=['{:.2f}'.format(i) for i in aa]
    print "aa2" ,cc
    ss=['{:.2f}'.format(i) for i in ss]
    print 'ss2',ss
    # draw()
    if len(ss)<=1:
        result= None
    elif float(ss[-1])==0.0 or float(ss[-2])==0.0:
        result=None
    else:
        result= 1.0*float(ss[-1])/float(ss[-2])
    print "小区该物业类型增长率",result
    return result

'''
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
        print "###########################################################################################"
        for block in block_dtyep:
            print block
        print "###########################################################################################"
        # 小区循环
        by_name= df.groupby(by=['name'])
        blockRate=pd.Series()
        for name,df in by_name:
            print "                        "
            print name
            df_time= pd.DataFrame(df,columns=['t','price'])
            # 排序
            sorted_data=df_time.sort_values(by='t')
            sort_ix_data=sorted_data.reset_index(drop=True)
            print "number of sample", sort_ix_data.shape[0]
            if False:
                pass
                # sort_ix_data.shape[0]==1
                # result=None
                # print "case not enough"
            else:
                # 补充案例，计算拟合值
                avglist= getcase_calcuAVG(data=sort_ix_data)
                # print "avglist",avglist
                aa=list(avglist.fillna(value=0))
                cc=['{:.2f}'.format(i) for i in aa]
                # test
                dd= [48646.09302,48528.84615,49772.57895,41667,49312,43400,43400,43400,25340,25340,25340,25340,23006.03125,30241.53333,30054.45455,22566.75,22566.75,22566.75,22566.75,22566.75,22566.75,22566.75,22566.75,22566.75]
                kk= dd[::-1]
                kk=['{:.2f}'.format(i) for i in kk]
                print 'tddddddddd',kk
                print '原始拟合值',cc
                # 拟合值缺失， 补充拟合值
                aa=get_nearAvg(aa)
                # 二次平滑值计算
                s = AES(aa, beta=0.3)
                ss = AES(s, beta=0.1)
                cc=['{:.2f}'.format(i) for i in aa]
                print "补充拟合值" ,cc
                ss=['{:.2f}'.format(i) for i in ss]
                print '二次平滑值',ss
                # draw()
                if len(ss)<=1:
                    result= None
                elif float(ss[-1])==0.0 or float(ss[-2])==0.0:
                    result=None
                else:
                    result= 1.0*float(ss[-1])/float(ss[-2])

                print name,block[0],block[1],"原始涨跌幅",result
                # result= getrate(sort_ix_data)
            if result<>None:
                blockRate.set_value(name,result)
                break
            break


        print "板块原始涨跌幅列表"
        print blockRate
        avg_blockRate,min_block, max_block= zoneAVE(blockRate,windowwidth=0.1,step=0.01,rate=0.5)
        print '最小值和最大值',min_block, max_block

        for name,value in enumerate(blockRate):
            if value< min_block:
                blockRate[name]=min_block
            elif value>max_block:
                blockRate[name]=max_block
            else:
                pass
        print "最终涨跌幅"
        print blockRate

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





#
# def test():
#     # dd= [48646.09302,48528.84615,49772.57895,41667,49312,43400,43400,43400,25340,25340,25340,25340,23006.03125,30241.53333,30054.45455,]
#     # aa= dd[::-1]
#
#     # 原始拟合值
#     # aa=['22566.75', '30054.45', '30229.00', '23006.03', '25340.00', '25340.00', '25340.00', '25340.00', '0.00', '43400.00', '43400.00', '49312.00', '416  67.00', '49772.58', '48646.09']
#     # kk= ['22566.75','22566.75','22566.75','22566.75','22566.75','22566.75','22566.75','22566.75','22566.75', '30054.45', '30229.00', '23006.03', '25340.00', '25340.00', '25340.00', '25340.00', '25340.00', '43400.00', '43400.00', '49312.00', '41667.00', '49772.58', '48646.09']
#     # aa=[]
#     # for i in kk:
#     #     print i
#     #     aa.append(float(i))
#     # print len(aa)
#     #
#     dd=['22566.75', '22566.75', '22566.75', '22566.75', '22566.75', '22566.75', '22566.75', '22566.75', '22566.75', '30054.45', '30241.53', '23006.03', '25340.00', '25340.00', '25340.00', '25340.00', '43400.00', '43400.00', '43400.00', '49312.00', '41667.00', '49772.58', '48528.85', '48646.09']
#     aa=[]
#     for i in dd:
#         print i
#
#         aa.append(float(i))
#     print len(dd)
#     s = AES((aa), beta=0.3)
#     ss = AES(s, beta=0.1)
#     cc=['{:.2f}'.format(i) for i in aa]
#
#     print "补充拟合值" ,cc
#
#     ss=['{:.2f}'.format(i) for i in ss]
#     print '二次平滑值',ss
#     draw(cc,ss)
#
#
#     s = AES(aa[3:], beta=0.3)
#     ss = AES(s, beta=0.1)
#     cc=['{:.2f}'.format(i) for i in aa]
#
#     print "补充拟合值" ,cc
#
#     ss=['{:.2f}'.format(i) for i in ss]
#     print '二次平滑值',ss
#     draw(cc,ss)
#
#     # print float(ss[-1])/float(ss[-3])
# test()

