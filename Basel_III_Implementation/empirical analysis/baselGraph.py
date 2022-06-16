#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 11:07:40 2022

@author: bogdanolena
"""


"Combining all datasets to produce a visual representation"





import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 

SEC=pd.read_csv('SECcategoriesNew.csv', sep='/')
DIS=pd.read_csv('DIScategoriesNew.csv', sep='/')
LEX=pd.read_csv('LEXcategoriesNew.csv', sep='/')
LCR=pd.read_csv('LCRcategoriesNew.csv', sep='/')
NSF=pd.read_csv('NSFcategoriesNew.csv', sep='/')
IDL=pd.read_csv('IDLcategoriesNew.csv', sep='/')
IRRBB=pd.read_csv('IRRBBcategoriesNew.csv', sep='/')
DSIB=pd.read_csv('DSIBcategoriesNew.csv', sep='/')
LEV=pd.read_csv('LEVcategoriesNew.csv', sep='/')
TLAC=pd.read_csv('TLACcategoriesNew.csv', sep='/')
SACCR=pd.read_csv('SACCRcategoriesNew.csv', sep='/')
EIF=pd.read_csv('EIFcategoriesNew.csv', sep='/')
RBC=pd.read_csv('RBCcategoriesNew.csv', sep='/')
CCP=pd.read_csv('CCPcategoriesNew.csv', sep='/')
MARNCCD=pd.read_csv('MARNCCDcategoriesNew.csv', sep='/')
CCyB=pd.read_csv('CCyBcategoriesNew.csv', sep='/')



baselIII=pd.concat([TLAC, MARNCCD, DIS, IRRBB, SEC,  LEX, EIF, CCP,  IDL,
                    DSIB, LEV, NSF,  CCyB, RBC, LCR
    ])
baselIII= baselIII.set_index('section')



fig, ax = plt.subplots(figsize=(10, 5))

#ax.plot(baselIII["length"], color = 'green', label = 'length')
#ax.plot(baselIII["cyclomatic"], color = 'red', label = 'cyclomatic')
#ax.plot(baselIII["quantity"], color = 'orange', label = 'quantity')
#ax.plot(baselIII["potential"], color = 'blue', label = 'potential')
#ax.plot(baselIII["diversity"], color = 'magenta', label = 'diversity')
ax.plot(baselIII["level"], color = 'purple', label = 'level')
sns.set_style("whitegrid")
ax.legend(loc = 'upper right', fontsize=15)
plt.xticks(rotation=45, fontsize=10)
plt.yticks( fontsize=15)
plt.grid(False)
plt.rcParams['figure.dpi'] = 500
plt.rcParams['savefig.dpi'] = 500
plt.show()


baselIIIdev=pd.concat([TLAC, MARNCCD, DIS, IRRBB,CCP,  LEX, EIF,   IDL,
                    SEC, DSIB, NSF,  CCyB, LEV, RBC, LCR
    ])
baselIIIdev= baselIIIdev.set_index('section')


fig, ax = plt.subplots(figsize=(10, 5))

#ax.plot(baselIIIdev["length"], color = 'green', label = 'length')
ax.plot(baselIIIdev["cyclomatic"], color = 'red', label = 'cyclomatic')
#ax.plot(baselIIIdev["quantity"], color = 'orange', label = 'quantity')
#ax.plot(baselIIIdev["potential"], color = 'blue', label = 'potential')
#ax.plot(baselIIIdev["diversity"], color = 'magenta', label = 'diversity')
#ax.plot(baselIIIdev["level"], color = 'purple', label = 'level')
sns.set_style("whitegrid")
ax.legend(loc = 'upper right', fontsize=15)
plt.xticks(rotation=45, fontsize=10)
plt.yticks( fontsize=15)
plt.grid(False)
plt.rcParams['figure.dpi'] = 500
plt.rcParams['savefig.dpi'] = 500
plt.show()