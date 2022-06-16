#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 20:50:20 2022

@author: bogdanolena
"""

# Importing the libraries
import numpy as np
import pandas as pd
import fitz  # this is pymupdf, to import the text
from datetime import datetime #to measure the time the program takes to execute 
# Importing the datasets



"""
I begin by importing the keys proposed by Colliard and Georg 2020 (working paper)
The dictionary consists on 9099 keys built after classifying words in the 
16 Titles of the Dodd-Frank Act plus its introduction


I also highligh the time each specific part takes to be executed :
    This is the analysis of the version of Dodd Frank Act that was presented to the Senat
#Duration Dodd-Frank Title 1 : 0:13:32.538567
#Duration Dodd-Frank Title 2: 0:34:57.370724
#Duration Dodd-Frank Title 3: 0:13:57.701768
#Duration Dodd-Frank Title 4: 0:02:51.942673
#Duration Dodd-Frank Title 5: 0:09:20.419117
#Duration Dodd-Frank Title 6: 0:11:59.472058
#Duration Dodd-Frank Title 7: 0:47:48.756486
#Duration Dodd-Frank Title 8: 0:08:29.141264
#Duration Dodd-Frank Title 9: 0:52:42.020809
#Duration Dodd-Frank Title 10: 2:10:46.377749
---------------------------------------------

#Duration Dodd-Frank Title 11: 0:02:12.046859

"""


dataset = pd.read_csv('category_cons_all_titles_most_frequent_keys.csv', sep=';',  header=None)
for i in range(0, len(dataset[1])):
    if dataset[1][i]=="Attributes":
        dataset[1][i]="EconomicOperands"
    if dataset[1][i]=="FunctionWords":
        dataset[1][i]="Other"
    if dataset[1][i]=="LegalReferences":
        dataset[1][i]="Other"
dataset=dataset.iloc[1:, :].values
dataset= pd.DataFrame(dataset)
dataset['key'] = dataset[0]
dataset['category'] = dataset[1]
dataset= dataset.drop(dataset.columns[[0, 1]], axis = 1)
#dataset['key']= dataset['key'].str.lower()
keys=dataset.drop(dataset.columns[[ 1]], axis = 1)

#Adding a column of n numbers from 1 to length(keys) in order to create a dictionary 
keys['number'] = 0


keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(keys_dict)


keys_dict = {k: v for k, v in keys_dict.items()}



#Dodd-Frank Title I


"""
I then open the first text, i.e. Dodd-Frank Section 1, to investigate the complexity 
using my dictionary (keys_dict) dataframe

"""

start_time1 = datetime.now()

f = open("dodd_frankTitle1V2.txt")
lines=f.readlines()

        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()

  
# Loop through each line of the file

grouped_data_1= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank1= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF1= pd.DataFrame(index=range(len(final_DoddFrank1)),columns=range(3))
for j in range(len( final_DoddFrank1)):
    if final_DoddFrank1.iloc[j,2]!=0:
        final_DF1.iloc[j,0]=final_DoddFrank1.iloc[j,0] 
        final_DF1.iloc[j,1]=final_DoddFrank1.iloc[j,1]
        final_DF1.iloc[j,2]=final_DoddFrank1.iloc[j,2] 
final_DF1['key'] = final_DF1[0]
final_DF1['category'] = final_DF1[1]
final_DF1['freq'] = final_DF1[2]
            #Droping missing (nan) values
final_DF1=final_DF1.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF1.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF1.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_1=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_1)

grouped_data_1V2=pd.DataFrame(grouped_data_1)
grouped_data_1V2 = grouped_data_1V2.T
grouped_data_1V2=grouped_data_1V2.set_axis([  "EconomicOperands_s", "Other_s", "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_1V2.to_csv('DFTitle1V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle1V2Categories.csv', sep='/',  header=None)

end_time1 = datetime.now()

duration1=end_time1-start_time1
print(duration1)


"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_1V2["section"]=["Dodd_frankT1V2"]
#Length 
grouped_data_1V2["length"] = grouped_data_1V2['EconomicOperands_t'] + grouped_data_1V2["LogicalConnectors_t"]+grouped_data_1V2["MathematicalOperators_t"]+grouped_data_1V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_1V2['cyclomatic'] = grouped_data_1V2['LogicalConnectors_t']
#Quantity 
grouped_data_1V2['quantity'] = grouped_data_1V2['RegulatoryOperators_t']
#Potential 
grouped_data_1V2['potential'] = 2+ grouped_data_1V2["EconomicOperands_s"]
#Diversity 
grouped_data_1V2['diversity'] = grouped_data_1V2["MathematicalOperators_s"]+grouped_data_1V2["RegulatoryOperators_s"]+grouped_data_1V2["LogicalConnectors_s"]
#Level 
grouped_data_1V2['level']= grouped_data_1V2['potential']/grouped_data_1V2['length']
grouped_data_1V2.to_csv('DFTitle1V2Categories.csv', index=False, sep='/') 

#Title 2 

start_time2 = datetime.now()

"""
I follow the same procedure with other Titles of Dodd-Frank Act 
"""

f = open("dodd_frankTitle2V2.txt")
lines=f.readlines()
        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()

  
# Loop through each line of the file

grouped_data_2= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank2= pd.merge(dataset, Freq, on='key')
    #Droping keys for which frequency==0
final_DF2= pd.DataFrame(index=range(len(final_DoddFrank2)),columns=range(3))
for j in range(len( final_DoddFrank2)):
    if final_DoddFrank2.iloc[j,2]!=0:
        final_DF2.iloc[j,0]=final_DoddFrank2.iloc[j,0] 
        final_DF2.iloc[j,1]=final_DoddFrank2.iloc[j,1]
        final_DF2.iloc[j,2]=final_DoddFrank2.iloc[j,2] 
final_DF2['key'] = final_DF2[0]
final_DF2['category'] = final_DF2[1]
final_DF2['freq'] = final_DF2[2]
            #Droping missing (nan) values
final_DF2=final_DF2.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF2.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF2.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_2=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_2)

grouped_data_2V2=pd.DataFrame(grouped_data_2)
grouped_data_2V2 = grouped_data_2V2.T
grouped_data_2V2=grouped_data_2V2.set_axis([  "EconomicOperands_s", "Other_s", "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_2V2.to_csv('DFTitle2V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle2V2Categories.csv', sep='/',  header=None)

end_time2 = datetime.now()

duration2= end_time2-start_time2
print(duration2)


"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_2V2["section"]=["Dodd_frankT2V2"]
#Length 
grouped_data_2V2["length"] = grouped_data_2V2['EconomicOperands_t']+ grouped_data_2V2["LogicalConnectors_t"]+grouped_data_2V2["MathematicalOperators_t"]+grouped_data_2V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_2V2['cyclomatic'] = grouped_data_2V2['LogicalConnectors_t']
#Quantity 
grouped_data_2V2['quantity'] = grouped_data_2V2['RegulatoryOperators_t']
#Potential 
grouped_data_2V2['potential'] = 2+ grouped_data_2V2["EconomicOperands_s"]
#Diversity 
grouped_data_2V2['diversity'] = grouped_data_2V2["MathematicalOperators_s"]+grouped_data_2V2["RegulatoryOperators_s"]+grouped_data_2V2["LogicalConnectors_s"]
#Level 
grouped_data_2V2['level']= grouped_data_2V2['potential']/grouped_data_2V2['length']
grouped_data_2V2.to_csv('DFTitle2V2Categories.csv', index=False, sep='/') 



#Title III

start_time3 = datetime.now()

"""
I follow the same procedure with other Titles of Dodd-Frank Act 
"""

f = open("dodd_frankTitle3V2.txt")
lines=f.readlines()
        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()

  
# Loop through each line of the file

grouped_data_3= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank3= pd.merge(dataset, Freq, on='key')
    #Droping keys for which frequency==0
final_DF3= pd.DataFrame(index=range(len(final_DoddFrank3)),columns=range(3))
for j in range(len( final_DoddFrank3)):
    if final_DoddFrank3.iloc[j,2]!=0:
        final_DF3.iloc[j,0]=final_DoddFrank3.iloc[j,0] 
        final_DF3.iloc[j,1]=final_DoddFrank3.iloc[j,1]
        final_DF3.iloc[j,2]=final_DoddFrank3.iloc[j,2] 
final_DF3['key'] = final_DF3[0]
final_DF3['category'] = final_DF3[1]
final_DF3['freq'] = final_DF3[2]
            #Droping missing (nan) values
final_DF3=final_DF3.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF3.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF3.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_3=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_3)

grouped_data_3V2=pd.DataFrame(grouped_data_3)
grouped_data_3V2 = grouped_data_3V2.T
grouped_data_3V2=grouped_data_3V2.set_axis([ "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_3V2.to_csv('DFTitle3V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle3V2Categories.csv', sep='/',  header=None)

end_time3 = datetime.now()

duration3= end_time3-start_time3
print(duration3)



"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_3V2["section"]=["Dodd_frankT3V2"]
#Length 
grouped_data_3V2["length"] = grouped_data_3V2['EconomicOperands_t'] + grouped_data_3V2["LogicalConnectors_t"]+grouped_data_3V2["MathematicalOperators_t"]+grouped_data_3V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_3V2['cyclomatic'] = grouped_data_3V2['LogicalConnectors_t']
#Quantity 
grouped_data_3V2['quantity'] = grouped_data_3V2['RegulatoryOperators_t']
#Potential 
grouped_data_3V2['potential'] = 2+ grouped_data_3V2["EconomicOperands_s"]
#Diversity 
grouped_data_3V2['diversity'] = grouped_data_3V2["MathematicalOperators_s"]+grouped_data_3V2["RegulatoryOperators_s"]+grouped_data_3V2["LogicalConnectors_s"]
#Level 
grouped_data_3V2['level']= grouped_data_3V2['potential']/grouped_data_3V2['length']
grouped_data_3V2.to_csv('DFTitle3V2Categories.csv', index=False, sep='/') 



#Title IV 

f = open("dodd_frankTitle4V2.txt")
lines=f.readlines()
        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()


# Loop through each line of the file

start_time4 = datetime.now()

grouped_data_4= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank4= pd.merge(dataset, Freq, on='key')
    #Droping keys for which frequency==0
final_DF4= pd.DataFrame(index=range(len(final_DoddFrank4)),columns=range(3))
for j in range(len( final_DoddFrank4)):
    if final_DoddFrank4.iloc[j,2]!=0:
        final_DF4.iloc[j,0]=final_DoddFrank4.iloc[j,0] 
        final_DF4.iloc[j,1]=final_DoddFrank4.iloc[j,1]
        final_DF4.iloc[j,2]=final_DoddFrank4.iloc[j,2] 
final_DF4['key'] = final_DF4[0]
final_DF4['category'] = final_DF4[1]
final_DF4['freq'] = final_DF4[2]
            #Droping missing (nan) values
final_DF4=final_DF4.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF4.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF4.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_4=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_4)

grouped_data_4V2=pd.DataFrame(grouped_data_4)
grouped_data_4V2 = grouped_data_4V2.T
grouped_data_4V2=grouped_data_4V2.set_axis([ "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t", "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_4V2.to_csv('DFTitle4V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle4V2Categories.csv', sep='/',  header=None)

end_time4 = datetime.now()

duration4= end_time4-start_time4
print(duration4)


"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_4V2["section"]=["Dodd_frankT4V2"]
#Length 
grouped_data_4V2["length"] = grouped_data_4V2['EconomicOperands_t'] + grouped_data_4V2["LogicalConnectors_t"]+grouped_data_4V2["MathematicalOperators_t"]+grouped_data_4V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_4V2['cyclomatic'] = grouped_data_4V2['LogicalConnectors_t']
#Quantity 
grouped_data_4V2['quantity'] = grouped_data_4V2['RegulatoryOperators_t']
#Potential 
grouped_data_4V2['potential'] = 2+ grouped_data_4V2["EconomicOperands_s"]
#Diversity 
grouped_data_4V2['diversity'] = grouped_data_4V2["MathematicalOperators_s"]+grouped_data_4V2["RegulatoryOperators_s"]+grouped_data_4V2["LogicalConnectors_s"]
#Level 
grouped_data_4V2['level']= grouped_data_4V2['potential']/grouped_data_4V2['length']
grouped_data_4V2.to_csv('DFTitle4V2Categories.csv', index=False, sep='/') 


#Title 5 

start_time5 = datetime.now()

f = open("dodd_frankTitle5V2.txt")
lines=f.readlines()

        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()

  
# Loop through each line of the file

grouped_data_5= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank5= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF5= pd.DataFrame(index=range(len(final_DoddFrank5)),columns=range(3))
for j in range(len( final_DoddFrank5)):
    if final_DoddFrank5.iloc[j,2]!=0:
        final_DF5.iloc[j,0]=final_DoddFrank5.iloc[j,0] 
        final_DF5.iloc[j,1]=final_DoddFrank5.iloc[j,1]
        final_DF5.iloc[j,2]=final_DoddFrank5.iloc[j,2] 
final_DF5['key'] = final_DF5[0]
final_DF5['category'] = final_DF5[1]
final_DF5['freq'] = final_DF5[2]
            #Droping missing (nan) values
final_DF5=final_DF5.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other", "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF5.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF5.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_5=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_5)

grouped_data_5V2=pd.DataFrame(grouped_data_5)
grouped_data_5V2 = grouped_data_5V2.T
grouped_data_5V2=grouped_data_5V2.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_5V2.to_csv('DFTitle5V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle5V2Categories.csv', sep='/',  header=None)

end_time5 = datetime.now()

duration5=end_time5-start_time5
print(duration5)

"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_5V2["section"]=["Dodd_frankT5V2"]
#Length 
grouped_data_5V2["length"] = grouped_data_5V2['EconomicOperands_t'] + grouped_data_5V2["LogicalConnectors_t"]+grouped_data_5V2["MathematicalOperators_t"]+grouped_data_5V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_5V2['cyclomatic'] = grouped_data_5V2['LogicalConnectors_t']
#Quantity 
grouped_data_5V2['quantity'] = grouped_data_5V2['RegulatoryOperators_t']
#Potential 
grouped_data_5V2['potential'] = 2+ grouped_data_5V2["EconomicOperands_s"]
#Diversity 
grouped_data_5V2['diversity'] = grouped_data_5V2["MathematicalOperators_s"]+grouped_data_5V2["RegulatoryOperators_s"]+grouped_data_5V2["LogicalConnectors_s"]
#Level 
grouped_data_5V2['level']= grouped_data_5V2['potential']/grouped_data_5V2['length']
grouped_data_5V2.to_csv('DFTitle5V2Categories.csv', index=False, sep='/') 



#Title 6 



start_time6 = datetime.now()

f = open("dodd_frankTitle6V2.txt")
lines=f.readlines()

        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()

  
# Loop through each line of the file

grouped_data_6= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank6= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF6= pd.DataFrame(index=range(len(final_DoddFrank6)),columns=range(3))
for j in range(len( final_DoddFrank6)):
    if final_DoddFrank6.iloc[j,2]!=0:
        final_DF6.iloc[j,0]=final_DoddFrank6.iloc[j,0] 
        final_DF6.iloc[j,1]=final_DoddFrank6.iloc[j,1]
        final_DF6.iloc[j,2]=final_DoddFrank6.iloc[j,2] 
final_DF6['key'] = final_DF6[0]
final_DF6['category'] = final_DF6[1]
final_DF6['freq'] = final_DF6[2]
            #Droping missing (nan) values
final_DF6=final_DF6.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF6.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF6.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_6=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_6)

grouped_data_6V2=pd.DataFrame(grouped_data_6)
grouped_data_6V2 = grouped_data_6V2.T
grouped_data_6V2=grouped_data_6V2.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_6V2.to_csv('DFTitle6V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle6V2Categories.csv', sep='/',  header=None)

end_time6 = datetime.now()

duration6=end_time6-start_time6
print(duration6)


"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_6V2["section"]=["Dodd_frankT6V2"]
#Length 
grouped_data_6V2["length"] = grouped_data_6V2['EconomicOperands_t'] + grouped_data_6V2["LogicalConnectors_t"]+grouped_data_6V2["MathematicalOperators_t"]+grouped_data_6V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_6V2['cyclomatic'] = grouped_data_6V2['LogicalConnectors_t']
#Quantity 
grouped_data_6V2['quantity'] = grouped_data_6V2['RegulatoryOperators_t']
#Potential 
grouped_data_6V2['potential'] = 2+ grouped_data_6V2["EconomicOperands_s"]
#Diversity 
grouped_data_6V2['diversity'] = grouped_data_6V2["MathematicalOperators_s"]+grouped_data_6V2["RegulatoryOperators_s"]+grouped_data_6V2["LogicalConnectors_s"]
#Level 
grouped_data_6V2['level']= grouped_data_6V2['potential']/grouped_data_6V2['length']
grouped_data_6V2.to_csv('DFTitle6V2Categories.csv', index=False, sep='/') 




# Title VII 

start_time7 = datetime.now()

f = open("dodd_frankTitle7V2.txt")
lines=f.readlines()

        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()

  
# Loop through each line of the file

grouped_data_7= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank7= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF7= pd.DataFrame(index=range(len(final_DoddFrank7)),columns=range(3))
for j in range(len( final_DoddFrank7)):
    if final_DoddFrank7.iloc[j,2]!=0:
        final_DF7.iloc[j,0]=final_DoddFrank7.iloc[j,0] 
        final_DF7.iloc[j,1]=final_DoddFrank7.iloc[j,1]
        final_DF7.iloc[j,2]=final_DoddFrank7.iloc[j,2] 
final_DF7['key'] = final_DF7[0]
final_DF7['category'] = final_DF7[1]
final_DF7['freq'] = final_DF7[2]
            #Droping missing (nan) values
final_DF7=final_DF7.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF7.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF7.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_7=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_7)

grouped_data_7V2=pd.DataFrame(grouped_data_7)
grouped_data_7V2 = grouped_data_7V2.T
grouped_data_7V2=grouped_data_7V2.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_7V2.to_csv('DFTitle7V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle7V2Categories.csv', sep='/',  header=None)

end_time7 = datetime.now()

duration7=end_time7-start_time7
print(duration7)

"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_7V2["section"]=["Dodd_frankT7V2"]
#Length 
grouped_data_7V2["length"] = grouped_data_7V2['EconomicOperands_t']+ grouped_data_7V2["LogicalConnectors_t"]+grouped_data_7V2["MathematicalOperators_t"]+grouped_data_7V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_7V2['cyclomatic'] = grouped_data_7V2['LogicalConnectors_t']
#Quantity 
grouped_data_7V2['quantity'] = grouped_data_7V2['RegulatoryOperators_t']
#Potential 
grouped_data_7V2['potential'] = 2+ grouped_data_7V2["EconomicOperands_s"]
#Diversity 
grouped_data_7V2['diversity'] = grouped_data_7V2["MathematicalOperators_s"]+grouped_data_7V2["RegulatoryOperators_s"]+grouped_data_7V2["LogicalConnectors_s"]
#Level 
grouped_data_7V2['level']= grouped_data_7V2['potential']/grouped_data_7V2['length']
grouped_data_7V2.to_csv('DFTitle7V2Categories.csv', index=False, sep='/') 


#Title VIII 

start_time8 = datetime.now()

f = open("dodd_frankTitle8V2.txt")
lines=f.readlines()

        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()

  
# Loop through each line of the file

grouped_data_8= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank8= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF8= pd.DataFrame(index=range(len(final_DoddFrank8)),columns=range(3))
for j in range(len( final_DoddFrank8)):
    if final_DoddFrank8.iloc[j,2]!=0:
        final_DF8.iloc[j,0]=final_DoddFrank8.iloc[j,0] 
        final_DF8.iloc[j,1]=final_DoddFrank8.iloc[j,1]
        final_DF8.iloc[j,2]=final_DoddFrank8.iloc[j,2] 
final_DF8['key'] = final_DF8[0]
final_DF8['category'] = final_DF8[1]
final_DF8['freq'] = final_DF8[2]
            #Droping missing (nan) values
final_DF8=final_DF8.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF8.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF8.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_8=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_8)

grouped_data_8V2=pd.DataFrame(grouped_data_8)
grouped_data_8V2 = grouped_data_8V2.T
grouped_data_8V2=grouped_data_8V2.set_axis([  "EconomicOperands_s", "Other_s", "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_8V2.to_csv('DFTitle8V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle8V2Categories.csv', sep='/',  header=None)

end_time8 = datetime.now()

duration8=end_time8-start_time8
print(duration8)

"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_8V2["section"]=["Dodd_frankT8V2"]
#Length 
grouped_data_8V2["length"] = grouped_data_8V2['EconomicOperands_t'] + grouped_data_8V2["LogicalConnectors_t"]+grouped_data_8V2["MathematicalOperators_t"]+grouped_data_8V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_8V2['cyclomatic'] = grouped_data_8V2['LogicalConnectors_t']
#Quantity 
grouped_data_8V2['quantity'] = grouped_data_8V2['RegulatoryOperators_t']
#Potential 
grouped_data_8V2['potential'] = 2+ grouped_data_8V2["EconomicOperands_s"]
#Diversity 
grouped_data_8V2['diversity'] = grouped_data_8V2["MathematicalOperators_s"]+grouped_data_8V2["RegulatoryOperators_s"]+grouped_data_8V2["LogicalConnectors_s"]
#Level 
grouped_data_8V2['level']= grouped_data_8V2['potential']/grouped_data_8V2['length']
grouped_data_8V2.to_csv('DFTitle8V2Categories.csv', index=False, sep='/') 



#Title IX

start_time9 = datetime.now()

f = open("dodd_frankTitle9V2.txt")
lines=f.readlines()

        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()

  
# Loop through each line of the file

grouped_data_9= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank9= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF9= pd.DataFrame(index=range(len(final_DoddFrank9)),columns=range(3))
for j in range(len( final_DoddFrank9)):
    if final_DoddFrank9.iloc[j,2]!=0:
        final_DF9.iloc[j,0]=final_DoddFrank9.iloc[j,0] 
        final_DF9.iloc[j,1]=final_DoddFrank9.iloc[j,1]
        final_DF9.iloc[j,2]=final_DoddFrank9.iloc[j,2] 
final_DF9['key'] = final_DF9[0]
final_DF9['category'] = final_DF9[1]
final_DF9['freq'] = final_DF9[2]
            #Droping missing (nan) values
final_DF9=final_DF9.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other", "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF9.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF9.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_9=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_9)

grouped_data_9V2=pd.DataFrame(grouped_data_9)
grouped_data_9V2 = grouped_data_9V2.T
grouped_data_9V2=grouped_data_9V2.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_9V2.to_csv('DFTitle9V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle9V2Categories.csv', sep='/',  header=None)

end_time9 = datetime.now()

duration9=end_time9-start_time9
print(duration9)



"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_9V2["section"]=["Dodd_frankT9V2"]
#Length 
grouped_data_9V2["length"] = grouped_data_9V2['EconomicOperands_t'] + grouped_data_9V2["LogicalConnectors_t"]+grouped_data_9V2["MathematicalOperators_t"]+grouped_data_9V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_9V2['cyclomatic'] = grouped_data_9V2['LogicalConnectors_t']
#Quantity 
grouped_data_9V2['quantity'] = grouped_data_9V2['RegulatoryOperators_t']
#Potential 
grouped_data_9V2['potential'] = 2+ grouped_data_9V2["EconomicOperands_s"]
#Diversity 
grouped_data_9V2['diversity'] = grouped_data_9V2["MathematicalOperators_s"]+grouped_data_9V2["RegulatoryOperators_s"]+grouped_data_9V2["LogicalConnectors_s"]
#Level 
grouped_data_9V2['level']= grouped_data_9V2['potential']/grouped_data_9V2['length']
grouped_data_9V2.to_csv('DFTitle9V2Categories.csv', index=False, sep='/') 


# Title X

start_time10 = datetime.now()

f = open("dodd_frankTitle10V2.txt")
lines=f.readlines()

        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()

  
# Loop through each line of the file

grouped_data_10= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank10= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF10= pd.DataFrame(index=range(len(final_DoddFrank10)),columns=range(3))
for j in range(len( final_DoddFrank10)):
    if final_DoddFrank10.iloc[j,2]!=0:
        final_DF10.iloc[j,0]=final_DoddFrank10.iloc[j,0] 
        final_DF10.iloc[j,1]=final_DoddFrank10.iloc[j,1]
        final_DF10.iloc[j,2]=final_DoddFrank10.iloc[j,2] 
final_DF10['key'] = final_DF10[0]
final_DF10['category'] = final_DF10[1]
final_DF10['freq'] = final_DF10[2]
            #Droping missing (nan) values
final_DF10=final_DF10.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF10.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF10.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_10=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_10)

grouped_data_10V2=pd.DataFrame(grouped_data_10)
grouped_data_10V2 = grouped_data_10V2.T
grouped_data_10V2=grouped_data_10V2.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",   "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_10V2.to_csv('DFTitle10V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle10V2Categories.csv', sep='/',  header=None)

end_time10 = datetime.now()

duration10=end_time10-start_time10
print(duration10)


"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_10V2["section"]=["Dodd_frankT10V2"]
#Length 
grouped_data_10V2["length"] = grouped_data_10V2['EconomicOperands_t'] + grouped_data_10V2["LogicalConnectors_t"]+grouped_data_10V2["MathematicalOperators_t"]+grouped_data_10V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_10V2['cyclomatic'] = grouped_data_10V2['LogicalConnectors_t']
#Quantity 
grouped_data_10V2['quantity'] = grouped_data_10V2['RegulatoryOperators_t']
#Potential 
grouped_data_10V2['potential'] = 2+ grouped_data_10V2["EconomicOperands_s"]
#Diversity 
grouped_data_10V2['diversity'] = grouped_data_10V2["MathematicalOperators_s"]+grouped_data_10V2["RegulatoryOperators_s"]+grouped_data_10V2["LogicalConnectors_s"]
#Level 
grouped_data_10V2['level']= grouped_data_10V2['potential']/grouped_data_10V2['length']
grouped_data_10V2.to_csv('DFTitle10V2Categories.csv', index=False, sep='/') 


#Title XI

start_time11 = datetime.now()

f = open("dodd_frankTitle11V2.txt")
lines=f.readlines()

        
lines = [s.replace('<', '') for s in lines]
lines = [s.replace('>', '') for s in lines]
lines = [s.upper() for s in lines]
lines = [s.strip() for s in lines]
lines = [s.replace("``", '') for s in lines]
lines = [s.replace("''", '') for s in lines]
lines = [s.replace("--", ' ') for s in lines]
lines = [s.replace(";", '') for s in lines]
#Text analysis 

nan_value = float("NaN")
text = pd.DataFrame(lines, columns = ['text'])
text= text.replace("", nan_value)
text=text.dropna()
text= text['text'].values.tolist()

  
# Loop through each line of the file

grouped_data_11= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank11= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF11= pd.DataFrame(index=range(len(final_DoddFrank11)),columns=range(3))
for j in range(len( final_DoddFrank11)):
    if final_DoddFrank11.iloc[j,2]!=0:
        final_DF11.iloc[j,0]=final_DoddFrank11.iloc[j,0] 
        final_DF11.iloc[j,1]=final_DoddFrank11.iloc[j,1]
        final_DF11.iloc[j,2]=final_DoddFrank11.iloc[j,2] 
final_DF11['key'] = final_DF11[0]
final_DF11['category'] = final_DF11[1]
final_DF11['freq'] = final_DF11[2]
            #Droping missing (nan) values
final_DF11=final_DF11.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF11.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF11.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_11=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_11)

grouped_data_11V2=pd.DataFrame(grouped_data_11)
grouped_data_11V2 = grouped_data_11V2.T
grouped_data_11V2=grouped_data_11V2.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t", "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_11V2.to_csv('DFTitle11V2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle11V2Categories.csv', sep='/',  header=None)

end_time11 = datetime.now()

duration11=end_time11-start_time11
print(duration11)



"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_11V2["section"]=["Dodd_frankT11V2"]
#Length 
grouped_data_11V2["length"] = grouped_data_11V2['EconomicOperands_t'] + grouped_data_11V2["LogicalConnectors_t"]+grouped_data_11V2["MathematicalOperators_t"]+grouped_data_11V2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_11V2['cyclomatic'] = grouped_data_11V2['LogicalConnectors_t']
#Quantity 
grouped_data_11V2['quantity'] = grouped_data_11V2['RegulatoryOperators_t']
#Potential 
grouped_data_11V2['potential'] = 2+ grouped_data_11V2["EconomicOperands_s"]
#Diversity 
grouped_data_11V2['diversity'] = grouped_data_11V2["MathematicalOperators_s"]+grouped_data_11V2["RegulatoryOperators_s"]+grouped_data_11V2["LogicalConnectors_s"]
#Level 
grouped_data_11V2['level']= grouped_data_11V2['potential']/grouped_data_11V2['length']
grouped_data_11V2.to_csv('DFTitle11V2Categories.csv', index=False, sep='/') 
