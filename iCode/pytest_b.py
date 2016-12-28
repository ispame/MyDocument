# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.datasets.longley import load_pandas
from statsmodels.stats.outliers_influence import  variance_inflation_factor
from sklearn.decomposition import PCA

def get_excel(url= r'E:\MyWork\MyPcCharm\iData\a.xlsx',sheetname='Sheet5'):
    '''
    get the data, calculate the avg
    :return: 拟合值
    '''
    # df= pd.read_excel(r'E:\MyWork\MyPcCharm\MrYangPro\testFor2M.xlsx',sheetname= 'Sheet5',header= None,skiprows=1)
    df= pd.read_excel(url,sheetname= sheetname,header=0 ,skiprows=0)
    return df

mydata= get_excel(sheetname='Sheet11')
mat= mydata.iloc[0:70,1:120].as_matrix()
corrMat= np.corrcoef(mat.T)

X2013= np.ones(len(mydata) )
n=0
namelist= []
for i, name in enumerate(mydata):
    if '2013' in name:
        X2013= np.column_stack((X2013,mydata[name]))
        namelist.append(name)
        n=n+1
# print n
# print X2013
y=X2013[:,1:2]
X=X2013[:,2:]
X=pd.DataFrame(X)
y=pd.DataFrame(y)
def normlise(X=X):

    normX= X.apply(lambda x :(x-np.mean(x))/np.std(x,ddof=1))
    return normX
X= normlise(X=X)
def pca(X=X,n=2):
    pca = PCA(n_components=n)
    pca.fit(X)
    print (pca.explained_variance_ratio_)
    print (sum(pca.explained_variance_ratio_))
    Z=np.dot(X,pca.components_.T)
    return Z

Z= pca(X=X,n=3)
y= normlise(X=y)
def OLS(Z=Z,y=y):
    res= sm.OLS(y,Z).fit()
    print (res.summary())
    print (res.resid)
    return res
res= OLS()


print "google"