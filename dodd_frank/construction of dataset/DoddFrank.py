#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 08:46:32 2022

@author: bogdanolena
"""


# Importing the libraries
import numpy as np
import pandas as pd
from datetime import datetime #to measure the time the program takes to execute 

# Importing the datasets



"""
I begin by importing the keys proposed by Colliard and Georg 2020 (working paper)
The dictionary consists on 9099 keys built after classifying words in the 
16 Titles of the Dodd-Frank Act plus its introduction


I also highligh the time each specific part takes to be executed :
    This is the analysis of the final version of Dodd Frank Act
#Duration Dodd-Frank Title 1 : 0:29:09.111118
#Duration Dodd-Frank Title 2: 4:16:19.453143
#Duration Dodd-Frank Title 3: 0:31:10.577241
#Duration Dodd-Frank Title 4: 0:06:49.095974
#Duration Dodd-Frank Title 5: 0:11:46.537933
#Duration Dodd-Frank Title 6: 0:35:28.795415
#Duration Dodd-Frank Title 7: 1:00:19.981395
#Duration Dodd-Frank Title 8: 0:04:31.567262
#Duration Dodd-Frank Title 9: 0:50:35.580203
#Duration Dodd-Frank Title 10: 0:46:42.902834

---------------------------------------------
#Duration Dodd-Frank Title 11: 0:04:37.614630
#Duration Dodd-Frank Title 12: 0:01:33.005377
#Duration Dodd-Frank Title 13: 0:01:12.280072
#Duration Dodd-Frank Title 14: 0:33:01.500716
#Duration Dodd-Frank Title 15: 0:04:21.484850
"""


#Importing the dictionary of terms created by Colliard and Georg 2020

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

f = open("dodd_frankTitle1.txt")
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
column_names = [ "EconomicOperands", "Other", "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
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

grouped_data_1=pd.DataFrame(grouped_data_1)
grouped_data_1 = grouped_data_1.T
grouped_data_1=grouped_data_1.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_1.to_csv('DFTitle1Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle1Categories.csv', sep='/',  header=None)

end_time1 = datetime.now()

duration1=end_time1-start_time1
print(duration1)

"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

There are 6 main measures proposed in Colliard and Georg 2020 (working paper) and 
the literature they base on, i.e. length, cyclomatic measure, quantity, diversity, 
potential. Another way to consider complexity of the text is to define its level
which accounts for both length and potential and ranges from  0 to 1.
The paper gives more detailed description of and rationales behind the complexity measures.  
"""

grouped_data_1["section"]=["Dodd_frankT1VF"]
#Length 
grouped_data_1["length"] = grouped_data_1['EconomicOperands_t'] + grouped_data_1["LogicalConnectors_t"]+grouped_data_1["MathematicalOperators_t"]+grouped_data_1["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_1['cyclomatic'] = grouped_data_1['LogicalConnectors_t']
#Quantity 
grouped_data_1['quantity'] = grouped_data_1['RegulatoryOperators_t']
#Potential 
grouped_data_1['potential'] = 2+ grouped_data_1["EconomicOperands_s"]
#Diversity 
grouped_data_1['diversity'] = grouped_data_1["MathematicalOperators_s"]+grouped_data_1["RegulatoryOperators_s"]+grouped_data_1["LogicalConnectors_s"]
#Level 
grouped_data_1['level']= grouped_data_1['potential']/grouped_data_1['length']
grouped_data_1.to_csv('DFTitle1VFCategories.csv', index=False, sep='/') 

#Dodd-Frank Title II

start_time2 = datetime.now()

"""
I follow the same procedure with other Titles of Dodd-Frank Act 
"""

f = open("dodd_frankTitle2.txt")
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

grouped_data_2=pd.DataFrame(grouped_data_2)
grouped_data_2 = grouped_data_2.T
grouped_data_2=grouped_data_2.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t", "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_2.to_csv('DFTitle2Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle2Categories.csv', sep='/',  header=None)

end_time2 = datetime.now()

duration2= end_time2-start_time2
print(duration2)


"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_2["section"]=["Dodd_frankT2VF"]
#Length 
grouped_data_2["length"] = grouped_data_2['EconomicOperands_t']+ grouped_data_2["LogicalConnectors_t"]+grouped_data_2["MathematicalOperators_t"]+grouped_data_2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_2['cyclomatic'] = grouped_data_2['LogicalConnectors_t']
#Quantity 
grouped_data_2['quantity'] = grouped_data_2['RegulatoryOperators_t']
#Potential 
grouped_data_2['potential'] = 2+ grouped_data_2["EconomicOperands_s"]
#Diversity 
grouped_data_2['diversity'] = grouped_data_2["MathematicalOperators_s"]+grouped_data_2["RegulatoryOperators_s"]+grouped_data_2["LogicalConnectors_s"]
#Level 
grouped_data_2['level']= grouped_data_2['potential']/grouped_data_2['length']
grouped_data_2.to_csv('DFTitle2VFCategories.csv', index=False, sep='/') 

#Dodd-Frank Title III

start_time3 = datetime.now()

"""
I follow the same procedure with other Titles of Dodd-Frank Act 
"""

f = open("dodd_frankTitle3.txt")
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
for j in range(len( final_DoddFrank3)-1):
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

grouped_data_3=pd.DataFrame(grouped_data_3)
grouped_data_3 = grouped_data_3.T
grouped_data_3=grouped_data_3.set_axis([ "EconomicOperands_s", "Other_s", "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_3.to_csv('DFTitle3Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle3Categories.csv', sep='/',  header=None)

end_time3 = datetime.now()

duration3= end_time3-start_time3
print(duration3)




"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_3["section"]=["Dodd_frankT3VF"]
#Length 
grouped_data_3["length"] = grouped_data_3['EconomicOperands_t'] + grouped_data_3["LogicalConnectors_t"]+grouped_data_2["MathematicalOperators_t"]+grouped_data_3["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_3['cyclomatic'] = grouped_data_3['LogicalConnectors_t']
#Quantity 
grouped_data_3['quantity'] = grouped_data_3['RegulatoryOperators_t']
#Potential 
grouped_data_3['potential'] = 2+ grouped_data_3["EconomicOperands_s"]
#Diversity 
grouped_data_3['diversity'] = grouped_data_3["MathematicalOperators_s"]+grouped_data_3["RegulatoryOperators_s"]+grouped_data_3["LogicalConnectors_s"]
#Level 
grouped_data_3['level']= grouped_data_3['potential']/grouped_data_3['length']
grouped_data_3.to_csv('DFTitle3VFCategories.csv', index=False, sep='/') 



#Dodd-Frank Title IV

start_time4 = datetime.now()

"""
I follow the same procedure with other Titles of Dodd-Frank Act 
"""

f = open("dodd_frankTitle4.txt")
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
column_names = [ "EconomicOperands", "Other", "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
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

grouped_data_4=pd.DataFrame(grouped_data_4)
grouped_data_4 = grouped_data_4.T
grouped_data_4=grouped_data_4.set_axis([ "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_4.to_csv('DFTitle4Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle4Categories.csv', sep='/',  header=None)

end_time4 = datetime.now()

duration4= end_time4-start_time4
print(duration4)


"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_4["section"]=["Dodd_frankT4VF"]
#Length 
grouped_data_4["length"] = grouped_data_4['EconomicOperands_t'] + grouped_data_4["LogicalConnectors_t"]+grouped_data_4["MathematicalOperators_t"]+grouped_data_4["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_4['cyclomatic'] = grouped_data_4['LogicalConnectors_t']
#Quantity 
grouped_data_4['quantity'] = grouped_data_4['RegulatoryOperators_t']
#Potential 
grouped_data_4['potential'] = 2+ grouped_data_4["EconomicOperands_s"]
#Diversity 
grouped_data_4['diversity'] = grouped_data_4["MathematicalOperators_s"]+grouped_data_4["RegulatoryOperators_s"]+grouped_data_4["LogicalConnectors_s"]
#Level 
grouped_data_4['level']= grouped_data_4['potential']/grouped_data_4['length']
grouped_data_4.to_csv('DFTitle4Categories.csv', index=False, sep='/') 


#Dodd-Frank Title V


start_time5 = datetime.now()

f = open("dodd_frankTitle5.txt")
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

grouped_data_5=pd.DataFrame(grouped_data_5)
grouped_data_5 = grouped_data_5.T
grouped_data_5=grouped_data_5.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_5.to_csv('DFTitle5Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle5Categories.csv', sep='/',  header=None)

end_time5 = datetime.now()

duration5=end_time5-start_time5
print(duration5)

"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_5["section"]=["Dodd_frankT5VF"]
#Length 
grouped_data_5["length"] = grouped_data_5['EconomicOperands_t'] + grouped_data_5["LogicalConnectors_t"]+grouped_data_5["MathematicalOperators_t"]+grouped_data_5["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_5['cyclomatic'] = grouped_data_5['LogicalConnectors_t']
#Quantity 
grouped_data_5['quantity'] = grouped_data_5['RegulatoryOperators_t']
#Potential 
grouped_data_5['potential'] = 2+ grouped_data_5["EconomicOperands_s"]
#Diversity 
grouped_data_5['diversity'] = grouped_data_5["MathematicalOperators_s"]+grouped_data_5["RegulatoryOperators_s"]+grouped_data_5["LogicalConnectors_s"]
#Level 
grouped_data_5['level']= grouped_data_5['potential']/grouped_data_5['length']
grouped_data_5.to_csv('DFTitle5Categories.csv', index=False, sep='/') 

#Dodd-Frank Title VI


start_time6 = datetime.now()

f = open("dodd_frankTitle6.txt")
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

grouped_data_6=pd.DataFrame(grouped_data_6)
grouped_data_6 = grouped_data_6.T
grouped_data_6=grouped_data_6.set_axis([  "EconomicOperands_s", "Other_s", "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t", "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_6.to_csv('DFTitle6Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle6Categories.csv', sep='/',  header=None)

end_time6 = datetime.now()

duration6=end_time6-start_time6
print(duration6)


"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_6["section"]=["Dodd_frankT6VF"]
#Length 
grouped_data_6["length"] = grouped_data_6['EconomicOperands_t'] + grouped_data_6["LogicalConnectors_t"]+grouped_data_6["MathematicalOperators_t"]+grouped_data_6["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_6['cyclomatic'] = grouped_data_6['LogicalConnectors_t']
#Quantity 
grouped_data_6['quantity'] = grouped_data_6['RegulatoryOperators_t']
#Potential 
grouped_data_6['potential'] = 2+ grouped_data_6["EconomicOperands_s"]
#Diversity 
grouped_data_6['diversity'] = grouped_data_6["MathematicalOperators_s"]+grouped_data_6["RegulatoryOperators_s"]+grouped_data_6["LogicalConnectors_s"]
#Level 
grouped_data_6['level']= grouped_data_6['potential']/grouped_data_6['length']
grouped_data_6.to_csv('DFTitle6Categories.csv', index=False, sep='/') 


#Dodd-Frank Title VII 

start_time7 = datetime.now()

f = open("dodd_frankTitle7.txt")
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

grouped_data_7=pd.DataFrame(grouped_data_7)
grouped_data_7 = grouped_data_7.T
grouped_data_7=grouped_data_7.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_7.to_csv('DFTitle7Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle7Categories.csv', sep='/',  header=None)

end_time7 = datetime.now()

duration7=end_time7-start_time7
print(duration7)

"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_7["section"]=["Dodd_frankT7VF"]
#Length 
grouped_data_7["length"] = grouped_data_7['EconomicOperands_t']+ grouped_data_7["LogicalConnectors_t"]+grouped_data_7["MathematicalOperators_t"]+grouped_data_7["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_7['cyclomatic'] = grouped_data_7['LogicalConnectors_t']
#Quantity 
grouped_data_7['quantity'] = grouped_data_7['RegulatoryOperators_t']
#Potential 
grouped_data_7['potential'] = 2+ grouped_data_7["EconomicOperands_s"]
#Diversity 
grouped_data_7['diversity'] = grouped_data_7["MathematicalOperators_s"]+grouped_data_7["RegulatoryOperators_s"]+grouped_data_7["LogicalConnectors_s"]
#Level 
grouped_data_7['level']= grouped_data_7['potential']/grouped_data_7['length']
grouped_data_7.to_csv('DFTitle7Categories.csv', index=False, sep='/') 

#Dodd-Frank Title VIII 

start_time8 = datetime.now()

f = open("dodd_frankTitle8.txt")
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

grouped_data_8=pd.DataFrame(grouped_data_8)
grouped_data_8 = grouped_data_8.T
grouped_data_8=grouped_data_8.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_8.to_csv('DFTitle8Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle8Categories.csv', sep='/',  header=None)

end_time8 = datetime.now()

duration8=end_time8-start_time8
print(duration8)


"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_8["section"]=["Dodd_frankT8VF"]
#Length 
grouped_data_8["length"] = grouped_data_8['EconomicOperands_t'] + grouped_data_8["LogicalConnectors_t"]+grouped_data_8["MathematicalOperators_t"]+grouped_data_8["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_8['cyclomatic'] = grouped_data_8['LogicalConnectors_t']
#Quantity 
grouped_data_8['quantity'] = grouped_data_8['RegulatoryOperators_t']
#Potential 
grouped_data_8['potential'] = 2+ grouped_data_8["EconomicOperands_s"]
#Diversity 
grouped_data_8['diversity'] = grouped_data_8["MathematicalOperators_s"]+grouped_data_8["RegulatoryOperators_s"]+grouped_data_8["LogicalConnectors_s"]
#Level 
grouped_data_8['level']= grouped_data_8['potential']/grouped_data_8['length']
grouped_data_8.to_csv('DFTitle8Categories.csv', index=False, sep='/') 



#Dodd-Frank Title IX

start_time9 = datetime.now()

f = open("dodd_frankTitle9.txt")
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
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
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

grouped_data_9=pd.DataFrame(grouped_data_9)
grouped_data_9 = grouped_data_9.T
grouped_data_9=grouped_data_9.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_9.to_csv('DFTitle9Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle9Categories.csv', sep='/',  header=None)

end_time9 = datetime.now()

duration9=end_time9-start_time9
print(duration9)



"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_9["section"]=["Dodd_frankT9VF"]
#Length 
grouped_data_9["length"] = grouped_data_9['EconomicOperands_t'] + grouped_data_9["LogicalConnectors_t"]+grouped_data_9["MathematicalOperators_t"]+grouped_data_9["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_9['cyclomatic'] = grouped_data_9['LogicalConnectors_t']
#Quantity 
grouped_data_9['quantity'] = grouped_data_9['RegulatoryOperators_t']
#Potential 
grouped_data_9['potential'] = 2+ grouped_data_9["EconomicOperands_s"]
#Diversity 
grouped_data_9['diversity'] = grouped_data_9["MathematicalOperators_s"]+grouped_data_9["RegulatoryOperators_s"]+grouped_data_9["LogicalConnectors_s"]
#Level 
grouped_data_9['level']= grouped_data_9['potential']/grouped_data_9['length']
grouped_data_9.to_csv('DFTitle9Categories.csv', index=False, sep='/') 



#Dodd-Frank Title X

start_time10 = datetime.now()

f = open("dodd_frankTitle10.txt")
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
column_names = [ "EconomicOperands", "Other", "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
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

grouped_data_10=pd.DataFrame(grouped_data_10)
grouped_data_10 = grouped_data_10.T
grouped_data_10=grouped_data_10.set_axis([  "EconomicOperands_s", "Other_s", "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t", "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_10.to_csv('DFTitle10Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle10Categories.csv', sep='/',  header=None)

end_time10 = datetime.now()

duration10=end_time10-start_time10
print(duration10)

"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_10["section"]=["Dodd_frankT10VF"]
#Length 
grouped_data_10["length"] = grouped_data_10['EconomicOperands_t'] + grouped_data_10["LogicalConnectors_t"]+grouped_data_10["MathematicalOperators_t"]+grouped_data_10["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_10['cyclomatic'] = grouped_data_10['LogicalConnectors_t']
#Quantity 
grouped_data_10['quantity'] = grouped_data_10['RegulatoryOperators_t']
#Potential 
grouped_data_10['potential'] = 2+ grouped_data_10["EconomicOperands_s"]
#Diversity 
grouped_data_10['diversity'] = grouped_data_10["MathematicalOperators_s"]+grouped_data_10["RegulatoryOperators_s"]+grouped_data_10["LogicalConnectors_s"]
#Level 
grouped_data_10['level']= grouped_data_10['potential']/grouped_data_10['length']
grouped_data_10.to_csv('DFTitle10Categories.csv', index=False, sep='/') 


#--------------------------------

#Dodd-Frank Title XI

start_time11 = datetime.now()

f = open("dodd_frankTitle11.txt")
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

grouped_data_11=pd.DataFrame(grouped_data_11)
grouped_data_11 = grouped_data_11.T
grouped_data_11=grouped_data_11.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_11.to_csv('DFTitle11Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle11Categories.csv', sep='/',  header=None)

end_time11 = datetime.now()

duration11=end_time11-start_time11
print(duration11)


"""
Computing complexity measures given the formulas introduced in Colliard and Georg 2020

"""

grouped_data_11["section"]=["Dodd_frankT11VF"]
#Length 
grouped_data_11["length"] = grouped_data_11['EconomicOperands_t'] + grouped_data_11["LogicalConnectors_t"]+grouped_data_11["MathematicalOperators_t"]+grouped_data_11["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_11['cyclomatic'] = grouped_data_11['LogicalConnectors_t']
#Quantity 
grouped_data_11['quantity'] = grouped_data_11['RegulatoryOperators_t']
#Potential 
grouped_data_11['potential'] = 2+ grouped_data_11["EconomicOperands_s"]
#Diversity 
grouped_data_11['diversity'] = grouped_data_11["MathematicalOperators_s"]+grouped_data_11["RegulatoryOperators_s"]+grouped_data_11["LogicalConnectors_s"]
#Level 
grouped_data_11['level']= grouped_data_11['potential']/grouped_data_11['length']
grouped_data_11.to_csv('DFTitle11Categories.csv', index=False, sep='/') 


#Dodd-Frank Title XII

start_time12 = datetime.now()

f = open("dodd_frankTitle12.txt")
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

grouped_data_12= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank12= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF12= pd.DataFrame(index=range(len(final_DoddFrank12)),columns=range(3))
for j in range(len( final_DoddFrank12)):
    if final_DoddFrank12.iloc[j,2]!=0:
        final_DF12.iloc[j,0]=final_DoddFrank12.iloc[j,0] 
        final_DF12.iloc[j,1]=final_DoddFrank12.iloc[j,1]
        final_DF12.iloc[j,2]=final_DoddFrank12.iloc[j,2] 
final_DF12['key'] = final_DF12[0]
final_DF12['category'] = final_DF12[1]
final_DF12['freq'] = final_DF12[2]
            #Droping missing (nan) values
final_DF12=final_DF12.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF12.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF12.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_12=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_12)

grouped_data_12=pd.DataFrame(grouped_data_12)
grouped_data_12 = grouped_data_12.T
grouped_data_12=grouped_data_12.set_axis([  "EconomicOperands_s", "Other_s", "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_12.to_csv('DFTitle12Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle12Categories.csv', sep='/',  header=None)

end_time12 = datetime.now()

duration12=end_time12-start_time12
print(duration12)

#Dodd-Frank Title XIII

start_time13 = datetime.now()

f = open("dodd_frankTitle13.txt")
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

grouped_data_13= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank13= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF13= pd.DataFrame(index=range(len(final_DoddFrank13)),columns=range(3))
for j in range(len( final_DoddFrank13)):
    if final_DoddFrank13.iloc[j,2]!=0:
        final_DF13.iloc[j,0]=final_DoddFrank13.iloc[j,0] 
        final_DF13.iloc[j,1]=final_DoddFrank13.iloc[j,1]
        final_DF13.iloc[j,2]=final_DoddFrank13.iloc[j,2] 
final_DF13['key'] = final_DF13[0]
final_DF13['category'] = final_DF13[1]
final_DF13['freq'] = final_DF13[2]
            #Droping missing (nan) values
final_DF13=final_DF13.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other", "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF13.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF13.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_13=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_13)

grouped_data_13=pd.DataFrame(grouped_data_13)
grouped_data_13 = grouped_data_13.T
grouped_data_13=grouped_data_13.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_13.to_csv('DFTitle13Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle13Categories.csv', sep='/',  header=None)

end_time13 = datetime.now()

duration13=end_time13-start_time13
print(duration13)


#Dodd-Frank Title XIV

start_time14 = datetime.now()

f = open("dodd_frankTitle14.txt")
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

grouped_data_14= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank14= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF14= pd.DataFrame(index=range(len(final_DoddFrank14)),columns=range(3))
for j in range(len( final_DoddFrank14)):
    if final_DoddFrank14.iloc[j,2]!=0:
        final_DF14.iloc[j,0]=final_DoddFrank14.iloc[j,0] 
        final_DF14.iloc[j,1]=final_DoddFrank14.iloc[j,1]
        final_DF14.iloc[j,2]=final_DoddFrank14.iloc[j,2] 
final_DF14['key'] = final_DF14[0]
final_DF14['category'] = final_DF14[1]
final_DF14['freq'] = final_DF14[2]
            #Droping missing (nan) values
final_DF14=final_DF14.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other", "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF14.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF14.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_14=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_14)

grouped_data_14=pd.DataFrame(grouped_data_14)
grouped_data_14 = grouped_data_14.T
grouped_data_14=grouped_data_14.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_14.to_csv('DFTitle14Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle14Categories.csv', sep='/',  header=None)

end_time14 = datetime.now()

duration14=end_time14-start_time14
print(duration14)



#Dodd-Frank Title XV

start_time15 = datetime.now()

f = open("dodd_frankTitle15.txt")
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

grouped_data_15= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DoddFrank15= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final_DF15= pd.DataFrame(index=range(len(final_DoddFrank15)),columns=range(3))
for j in range(len( final_DoddFrank15)):
    if final_DoddFrank15.iloc[j,2]!=0:
        final_DF15.iloc[j,0]=final_DoddFrank15.iloc[j,0] 
        final_DF15.iloc[j,1]=final_DoddFrank15.iloc[j,1]
        final_DF15.iloc[j,2]=final_DoddFrank15.iloc[j,2] 
final_DF15['key'] = final_DF15[0]
final_DF15['category'] = final_DF15[1]
final_DF15['freq'] = final_DF15[2]
            #Droping missing (nan) values
final_DF15=final_DF15.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final_DF15.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final_DF15.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_15=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_15)

grouped_data_15=pd.DataFrame(grouped_data_15)
grouped_data_15 = grouped_data_15.T
grouped_data_15=grouped_data_15.set_axis([  "EconomicOperands_s", "Other_s",  "LogicalConnectors_s", "MathematicalOperators_s",  "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",  "LogicalConnectors_t", "MathematicalOperators_t",  "RegulatoryOperators_t"], axis=1)
grouped_data_15.to_csv('DFTitle15Categories.csv', index=False, sep='/')
datasetx = pd.read_csv('DFTitle15Categories.csv', sep='/',  header=None)

end_time15 = datetime.now()

duration15=end_time15-start_time15
print(duration15)


