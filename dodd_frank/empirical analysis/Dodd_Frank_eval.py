#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 09:19:07 2022

@author: bogdanolena
"""
import pandas as pd 

df1VF=pd.read_csv('DFTitle1VFCategories.csv', sep='/')
df2VF=pd.read_csv('DFTitle2VFCategories.csv', sep='/')
df3VF=pd.read_csv('DFTitle3VFCategories.csv', sep='/')
df4VF=pd.read_csv('DFTitle4VFCategories.csv', sep='/')
df5VF=pd.read_csv('DFTitle5VFCategories.csv', sep='/')
df6VF=pd.read_csv('DFTitle6VFCategories.csv', sep='/')
df7VF=pd.read_csv('DFTitle7VFCategories.csv', sep='/')
df8VF=pd.read_csv('DFTitle8VFCategories.csv', sep='/')
df9VF=pd.read_csv('DFTitle9VFCategories.csv', sep='/')
df10VF=pd.read_csv('DFTitle10VFCategories.csv', sep='/')

df1V2=pd.read_csv('DFTitle1V2Categories.csv', sep='/')
df2V2=pd.read_csv('DFTitle2V2Categories.csv', sep='/')
df3V2=pd.read_csv('DFTitle3V2Categories.csv', sep='/')
df4V2=pd.read_csv('DFTitle4V2Categories.csv', sep='/')
df5V2=pd.read_csv('DFTitle5V2Categories.csv', sep='/')
df6V2=pd.read_csv('DFTitle6V2Categories.csv', sep='/')
df7V2=pd.read_csv('DFTitle7V2Categories.csv', sep='/')
df8V2=pd.read_csv('DFTitle8V2Categories.csv', sep='/')
df9V2=pd.read_csv('DFTitle9V2Categories.csv', sep='/')
df10V2=pd.read_csv('DFTitle10V2Categories.csv', sep='/')

"Combining all Dodd-Frank datasets to produce a visual representation"



measures1=pd.DataFrame()
columns=["length", "cyclomatic", "quantity", "potential", "diversity", "level"]
for i in columns:
    measures1[i]=(df1VF[i]-df1V2[i])/df1V2[i]
measures1["section"]="DF1"

measures2=pd.DataFrame()
columns=["length", "cyclomatic", "quantity", "potential", "diversity", "level"]
for i in columns:
    measures2[i]=(df2VF[i]-df2V2[i])/df2V2[i]
measures2["section"]="DF2"


measures3=pd.DataFrame()
columns=["length", "cyclomatic", "quantity", "potential", "diversity", "level"]
for i in columns:
    measures3[i]=(df3VF[i]-df3V2[i])/df3V2[i]    
measures3["section"]="DF3"

measures4=pd.DataFrame()
columns=["length", "cyclomatic", "quantity", "potential", "diversity", "level"]
for i in columns:
    measures4[i]=(df4VF[i]-df4V2[i])/df4V2[i]
measures4["section"]="DF4"

    
measures5=pd.DataFrame()
columns=["length", "cyclomatic", "quantity", "potential", "diversity", "level"]
for i in columns:
    measures5[i]=(df5VF[i]-df5V2[i])/df5V2[i] 
measures5["section"]="DF5"

    
measures6=pd.DataFrame()
columns=["length", "cyclomatic", "quantity", "potential", "diversity", "level"]
for i in columns:
    measures6[i]=(df6VF[i]-df6V2[i])/df6V2[i] 
measures6["section"]="DF6"

    
measures7=pd.DataFrame()
columns=["length", "cyclomatic", "quantity", "potential", "diversity", "level"]
for i in columns:
    measures7[i]=(df7VF[i]-df7V2[i])/df7V2[i] 
measures7["section"]="DF7"

measures8=pd.DataFrame()
columns=["length", "cyclomatic", "quantity", "potential", "diversity", "level"]
for i in columns:
    measures8[i]=(df8VF[i]-df8V2[i])/df8V2[i] 
measures8["section"]="DF8"

measures9=pd.DataFrame()
columns=["length", "cyclomatic", "quantity", "potential", "diversity", "level"]
for i in columns:
    measures9[i]=(df9VF[i]-df9V2[i])/df9V2[i] 
measures9["section"]="DF9"


measures10=pd.DataFrame()
columns=["length", "cyclomatic", "quantity", "potential", "diversity", "level"]
for i in columns:
    measures10[i]=(df10VF[i]-df10V2[i])/df10V2[i] 
measures10["section"]="DF10"



dFd=pd.concat([measures8, measures5, measures2, measures1, measures4, measures3, measures9, measures10, measures7, measures6])
dFd= dFd.set_index('section')

import matplotlib.pyplot as plt



fig, ax = plt.subplots(figsize=(10, 5))

#ax.plot(dFd["length"], color = 'green', label = 'length')
ax.plot(dFd["cyclomatic"], color = 'red', label = 'cyclomatic', linewidth=2.5)
ax.plot(dFd["quantity"], color = 'orange', label = 'quantity', linewidth=2.5)
ax.plot(dFd["potential"], color = 'blue', label = 'potential', linewidth=2.5)
ax.plot(dFd["diversity"], color = 'black', label = 'diversity', linewidth=2.5)
#ax.plot(dFd["level"], color = 'brown', label = 'level')
ax.legend(loc = 'upper right', fontsize=15)
plt.xticks(rotation=45, fontsize=15)
plt.yticks( fontsize=15)
plt.rcParams['figure.dpi'] = 2000
plt.rcParams['savefig.dpi'] = 2000
plt.show()
plt.savefig("Dodd_FrankComplexity.png",dpi=300)


dFd=pd.concat([measures1, measures6, measures7, measures9, measures10, measures3, measures4, measures2, measures5, measures8])
dFd= dFd.set_index('section')

import matplotlib.pyplot as plt



fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(dFd["length"], color = 'green', label = 'length')
#ax.plot(dFd["cyclomatic"], color = 'red', label = 'cyclomatic', linewidth=2.5)
#ax.plot(dFd["quantity"], color = 'orange', label = 'quantity', linewidth=2.5)
#ax.plot(dFd["potential"], color = 'blue', label = 'potential', linewidth=2.5)
#ax.plot(dFd["diversity"], color = 'violet', label = 'diversity', linewidth=2.5)
#ax.plot(dFd["level"], color = 'brown', label = 'level')
ax.legend(loc = 'upper right', fontsize=15)
plt.xticks(rotation=45, fontsize=15)
plt.yticks( fontsize=15)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.show()
plt.savefig("Dodd_FrankComplexity.png",dpi=300)
