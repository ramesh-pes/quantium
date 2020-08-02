#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 10:04:54 2020

@author: ar-ramesh.s
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline




#pandas dataviewing tools
pd.set_option('display.max_rows',20)
pd.set_option('display.max_columns', 40)
pd.set_option('display.width', 1000)

custDf=pd.read_csv('QVI_purchase_behaviour.csv')
tranDf=pd.read_excel("QVI_transaction_data.xlsx",sheet_name='in')
print(custDf.head())
print(tranDf.head())


#describe dataframes
print(tranDf.describe())
print(tranDf.info())

#change date fromat Datetime from 5 digit
from datetime import datetime
import xlrd

tranDf.DATE=tranDf.DATE.apply(lambda x: datetime(*xlrd.xldate_as_tuple(x, 0)))
print(tranDf.head())
print(tranDf.info())

#identifying chips only in product_name
##remove number and special charecters
#tranDf.PROD_NAME=[x[:-4] for x in tranDf.PROD_NAME]
#tranDf.PROD_NAME=tranDf.PROD_NAME.str.rstrip().replace("&"," ")

##removing salsa products that are not chips
tranDf['PROD_NAME']=tranDf['PROD_NAME'].apply(lambda x: x if "salsa" not in x.lower() else None)

print(tranDf.info(),
tranDf.isnull().sum(),
tranDf[tranDf.PROD_NAME.isnull()])
tranDf=tranDf.dropna()
print(tranDf.describe())

#outlier in PROD_QTY 
print(tranDf.PROD_QTY.plot.box())
print(tranDf.PROD_QTY.value_counts())

print(tranDf[tranDf.PROD_QTY>5])
"""
    There are two transactions where 200 packets of chips are bought in one transaction
and both of these transactions were by the same customer. 
LYLTY_CARD_NBR==226000 seems like wholesale customer . so drop hi cardnumber in customer data
"""
tranDf[tranDf.LYLTY_CARD_NBR==226000]
tranDf=tranDf[tranDf['PROD_QTY']!=200]
#custDf=custDf.drop(custDf[custDf.LYLTY_CARD_NBR==226000])
custDf=custDf[custDf.LYLTY_CARD_NBR!=226000]


#tranction verses time , to find missing data on certain date

#PACK SIZE
tranDf['PACK_SIZE']=tranDf['PROD_NAME'].str.extract(r'(\d{1,3})')
tranDf['PACK_SIZE']=tranDf['PACK_SIZE'].astype(str).astype(int)



