#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 16:18:53 2022

@author: bogdanolena
"""
# Importing the libraries
import numpy as np
import pandas as pd
import fitz  # this is pymupdf, to import the text
from datetime import datetime #to measure the time the program takes to execute 


"""
CCyb : 0:09:57.896232
MAR_NCCD: 0:07:27.604859
CCP: 0:03:46.795912
RBC: 0:07:18.020107
IER: 0:02:25.945071
SA_CRR:0:09:00.568368
TLAC:0:10:57.349474
LEV: 0:05:38.387867
DSIB: 0:01:40.200607
IRRBB: 0:14:27.572081
IDL: 0:11:44.350488
NSF: 0:07:45.110273
LCR: 0:26:51.173598
LEX:0:05:46.963937
DIS 0:46:41.529407
SEC: 0:13:57.528117
"""

#Importing the dictionary 

key = pd.read_csv('category_cons_all_titles_most_frequent_keys.csv', sep=';', 
                  header=None)
testing = pd.read_csv('verificationSet.csv',  sep=';',  header=0)
dataset = pd.concat([classifier, testing], axis=0)
dataset=dataset.reset_index()
del dataset["index"]

for i in range(0, len(dataset["category"])):
    if dataset["category"][i]=="Attributes":
        dataset["category"][i]="Other"
    if dataset["category"][i]=="FunctionWords":
        dataset["category"][i]="Other"
dataset=dataset.iloc[1:, :].values
dataset= pd.DataFrame(dataset)
dataset['key'] = dataset[0]
dataset['category'] = dataset[1]
dataset= dataset.drop(dataset.columns[[0, 1]], axis = 1)
#dataset['key']= dataset['key'].str.lower()
keys=dataset.drop(dataset.columns[[ 1]], axis = 1)

#Adding a column of n numbers from 1 to length(keys) 
#in order to create a dictionary 
keys['number'] = 0


keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(keys_dict)


keys_dict = {k: v for k, v in keys_dict.items()}



# Importing the datasets

start_time1 = datetime.now()

with fitz.open('CCyB.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('CCyBNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_1= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_CCyB= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_CCyB)),columns=range(3))
for j in range(len( final_CCyB)):
    if final_CCyB.iloc[j,2]!=0:
        final.iloc[j,0]=final_CCyB.iloc[j,0] 
        final.iloc[j,1]=final_CCyB.iloc[j,1]
        final.iloc[j,2]=final_CCyB.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", 
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_1=grouped_data_1.set_axis([  "EconomicOperands_s", "Other_s", 
        "LogicalConnectors_s", "MathematicalOperators_s",  
        "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t", 
        "LogicalConnectors_t", "MathematicalOperators_t", 
        "RegulatoryOperators_t"], axis=1)
grouped_data_1.to_csv('CCyBcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('CCyBcategoriesNew.csv', sep='/',  header=None)

end_time1 = datetime.now()
duration1=end_time1-start_time1
print(duration1)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_1["section"]=["CCyB"]
#Length 
grouped_data_1["length"] = grouped_data_1['EconomicOperands_t'] 
            + grouped_data_1["LogicalConnectors_t"]
            +grouped_data_1["MathematicalOperators_t"]
            +grouped_data_1["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_1['cyclomatic'] = grouped_data_1['LogicalConnectors_t']
#Quantity 
grouped_data_1['quantity'] = grouped_data_1['RegulatoryOperators_t']
#Potential 
grouped_data_1['potential'] = 2+ grouped_data_1["EconomicOperands_s"]
#Diversity 
grouped_data_1['diversity'] = grouped_data_1["MathematicalOperators_s"]
            +grouped_data_1["RegulatoryOperators_s"]
            +grouped_data_1["LogicalConnectors_s"]
#Level 
grouped_data_1['level']= grouped_data_1['potential']/grouped_data_1['length']
grouped_data_1.to_csv('CCyBcategoriesNew.csv', index=False, sep='/') 



# Importing the datasets

start_time2 = datetime.now()

with fitz.open('MAR_NCCD.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('MAR_NCCDNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_2= pd.DataFrame( columns=range(12))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_MAR= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_MAR)),columns=range(3))
for j in range(len( final_MAR)):
    if final_MAR.iloc[j,2]!=0:
        final.iloc[j,0]=final_MAR.iloc[j,0] 
        final.iloc[j,1]=final_MAR.iloc[j,1]
        final.iloc[j,2]=final_MAR.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other", 
                "LogicalConnectors", "MathematicalOperators",
                "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_2=grouped_data_2.set_axis([  "EconomicOperands_s", "Other_s", 
                "LogicalConnectors_s", "MathematicalOperators_s",  
                "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",
                "LogicalConnectors_t", "MathematicalOperators_t",  
                "RegulatoryOperators_t"], axis=1)
grouped_data_2.to_csv('MARNCCDcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('MARNCCDcategoriesNew.csv', sep='/',  header=None)

end_time2 = datetime.now()

duration2=end_time2-start_time2
print(duration2)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_2["section"]=["MAR_NCCD"]
#Length 
grouped_data_2["length"] = grouped_data_2['EconomicOperands_t']
        + grouped_data_2["LogicalConnectors_t"]
        +grouped_data_2["MathematicalOperators_t"]
        +grouped_data_2["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_2['cyclomatic'] = grouped_data_2['LogicalConnectors_t']
#Quantity 
grouped_data_2['quantity'] = grouped_data_2['RegulatoryOperators_t']
#Potential 
grouped_data_2['potential'] = 2+ grouped_data_2["EconomicOperands_s"]
#Diversity 
grouped_data_2['diversity'] = grouped_data_2["MathematicalOperators_s"]
        +grouped_data_2["RegulatoryOperators_s"]
        +grouped_data_2["LogicalConnectors_s"]
#Level 
grouped_data_2['level']= grouped_data_2['potential']/grouped_data_2['length']
grouped_data_2.to_csv('MARNCCDcategoriesNew.csv', index=False, sep='/') 



# Importing the datasets

start_time3 = datetime.now()

with fitz.open('CCP.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('CCPNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_3= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_CCP= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_CCP)),columns=range(3))
for j in range(len( final_CCP)):
    if final_CCP.iloc[j,2]!=0:
        final.iloc[j,0]=final_CCP.iloc[j,0] 
        final.iloc[j,1]=final_CCP.iloc[j,1]
        final.iloc[j,2]=final_CCP.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", 
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_3=grouped_data_3.set_axis([  "EconomicOperands_s", "Other_s", 
                "LogicalConnectors_s", "MathematicalOperators_s",  
                "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",
                "LogicalConnectors_t", "MathematicalOperators_t",  
                "RegulatoryOperators_t"], axis=1)
grouped_data_3.to_csv('CCPcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('CCPcategoriesNew.csv', sep='/',  header=None)

end_time3 = datetime.now()

duration3=end_time3-start_time3
print(duration3)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_3["section"]=["CCP"]
#Length 
grouped_data_3["length"] = grouped_data_3['EconomicOperands_t'] 
                + grouped_data_3["LogicalConnectors_t"]
                +grouped_data_3["MathematicalOperators_t"]
                +grouped_data_3["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_3['cyclomatic'] = grouped_data_3['LogicalConnectors_t']
#Quantity 
grouped_data_3['quantity'] = grouped_data_3['RegulatoryOperators_t']
#Potential 
grouped_data_3['potential'] = 2+ grouped_data_3["EconomicOperands_s"]
#Diversity 
grouped_data_3['diversity'] = grouped_data_3["MathematicalOperators_s"]
                +grouped_data_3["RegulatoryOperators_s"]
                +grouped_data_3["LogicalConnectors_s"]
#Level 
grouped_data_3['level']= grouped_data_3['potential']/grouped_data_3['length']
grouped_data_3.to_csv('CCPcategoriesNew.csv', index=False, sep='/') 



# Importing the datasets

start_time4 = datetime.now()

with fitz.open('RBC.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('RBCNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_4= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_RBC= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_RBC)),columns=range(3))
for j in range(len( final_RBC)):
    if final_RBC.iloc[j,2]!=0:
        final.iloc[j,0]=final_RBC.iloc[j,0] 
        final.iloc[j,1]=final_RBC.iloc[j,1]
        final.iloc[j,2]=final_RBC.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", 
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_4=grouped_data_4.set_axis([  "EconomicOperands_s", "Other_s",  
                        "LogicalConnectors_s", "MathematicalOperators_s",  
                        "RegulatoryOperators_s",  "EconomicOperands_t", 
                        "Other_t",  "LogicalConnectors_t", 
                        "MathematicalOperators_t",  "RegulatoryOperators_t"],
                                       axis=1)
grouped_data_4.to_csv('RBCcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('RBCcategoriesNew.csv', sep='/',  header=None)

end_time4 = datetime.now()

duration4=end_time4-start_time4
print(duration4)

"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""


grouped_data_4["section"]=["RBC"]
#Length 
grouped_data_4["length"] = grouped_data_4['EconomicOperands_t']
                + grouped_data_4["LogicalConnectors_t"]
                +grouped_data_4["MathematicalOperators_t"]
                +grouped_data_4["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_4['cyclomatic'] = grouped_data_4['LogicalConnectors_t']
#Quantity 
grouped_data_4['quantity'] = grouped_data_4['RegulatoryOperators_t']
#Potential 
grouped_data_4['potential'] = 2+ grouped_data_4["EconomicOperands_s"]
#Diversity 
grouped_data_4['diversity'] = grouped_data_4["MathematicalOperators_s"]
                +grouped_data_4["RegulatoryOperators_s"]
                +grouped_data_4["LogicalConnectors_s"]
#Level 
grouped_data_4['level']= grouped_data_4['potential']/grouped_data_4['length']
grouped_data_4.to_csv('RBCcategoriesNew.csv', index=False, sep='/') 



# Importing the datasets

start_time5 = datetime.now()

with fitz.open('EIR.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('EIRNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_5= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_EIR= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_EIR)),columns=range(3))
for j in range(len( final_EIR)):
    if final_EIR.iloc[j,2]!=0:
        final.iloc[j,0]=final_EIR.iloc[j,0] 
        final.iloc[j,1]=final_EIR.iloc[j,1]
        final.iloc[j,2]=final_EIR.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors",
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_5=grouped_data_5.set_axis([  "EconomicOperands_s", "Other_s",  
                    "LogicalConnectors_s", "MathematicalOperators_s", 
                    "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",
                    "LogicalConnectors_t", "MathematicalOperators_t",  
                    "RegulatoryOperators_t"], axis=1)
grouped_data_5.to_csv('EIRcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('EIRcategoriesNew.csv', sep='/',  header=None)

end_time5 = datetime.now()

duration5=end_time5-start_time5
print(duration5)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_5["section"]=["EIF"]
#Length 
grouped_data_5["length"] = grouped_data_5['EconomicOperands_t'] 
                    + grouped_data_5["LogicalConnectors_t"]
                    +grouped_data_5["MathematicalOperators_t"]
                    +grouped_data_5["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_5['cyclomatic'] = grouped_data_5['LogicalConnectors_t']
#Quantity 
grouped_data_5['quantity'] = grouped_data_5['RegulatoryOperators_t']
#Potential 
grouped_data_5['potential'] = 2+ grouped_data_5["EconomicOperands_s"]
#Diversity 
grouped_data_5['diversity'] = grouped_data_5["MathematicalOperators_s"]
                    +grouped_data_5["RegulatoryOperators_s"]
                    +grouped_data_5["LogicalConnectors_s"]
#Level 
grouped_data_5['level']= grouped_data_5['potential']/grouped_data_5['length']
grouped_data_5.to_csv('EIFcategoriesNew.csv', index=False, sep='/') 

#Importing the dataset


start_time6 = datetime.now()

with fitz.open('SA_CCR.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('SA_CCRNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_6= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_SA_CCR= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_SA_CCR)),columns=range(3))
for j in range(len( final_SA_CCR)):
    if final_SA_CCR.iloc[j,2]!=0:
        final.iloc[j,0]=final_SA_CCR.iloc[j,0] 
        final.iloc[j,1]=final_SA_CCR.iloc[j,1]
        final.iloc[j,2]=final_SA_CCR.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other", "LogicalConnectors", 
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_6=grouped_data_6.set_axis([  "EconomicOperands_s", "Other_s",  
                "LogicalConnectors_s", "MathematicalOperators_s",  
                "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",
                "LogicalConnectors_t", "MathematicalOperators_t", 
                "RegulatoryOperators_t"], axis=1)
grouped_data_6.to_csv('SACCRcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('SACCRcategoriesNew.csv', sep='/',  header=None)

end_time6 = datetime.now()

duration6=end_time6-start_time6
print(duration6)

"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_6["section"]=["SA_CCR"]
#Length 
grouped_data_6["length"] = grouped_data_6['EconomicOperands_t']
                    + grouped_data_6["LogicalConnectors_t"]
                    +grouped_data_6["MathematicalOperators_t"]
                    +grouped_data_6["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_6['cyclomatic'] = grouped_data_6['LogicalConnectors_t']
#Quantity 
grouped_data_6['quantity'] = grouped_data_6['RegulatoryOperators_t']
#Potential 
grouped_data_6['potential'] = 2+ grouped_data_6["EconomicOperands_s"]
#Diversity 
grouped_data_6['diversity'] = grouped_data_6["MathematicalOperators_s"]
                    +grouped_data_6["RegulatoryOperators_s"]
                    +grouped_data_6["LogicalConnectors_s"]
#Level 
grouped_data_6['level']= grouped_data_6['potential']/grouped_data_6['length']
grouped_data_6.to_csv('SACCRcategoriesNew.csv', index=False, sep='/') 

#Importing the dataset


start_time7 = datetime.now()

with fitz.open('TLAC.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('TLACNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_7= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_TLAC= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_TLAC)),columns=range(3))
for j in range(len( final_TLAC)):
    if final_TLAC.iloc[j,2]!=0:
        final.iloc[j,0]=final_TLAC.iloc[j,0] 
        final.iloc[j,1]=final_TLAC.iloc[j,1]
        final.iloc[j,2]=final_TLAC.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", 
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_7=grouped_data_7.set_axis([  "EconomicOperands_s", "Other_s",
                        "LogicalConnectors_s", "MathematicalOperators_s", 
                        "RegulatoryOperators_s",  "EconomicOperands_t", 
                        "Other_t",  "LogicalConnectors_t", 
                        "MathematicalOperators_t",  "RegulatoryOperators_t"], 
                                       axis=1)
grouped_data_7.to_csv('TLACcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('TLACcategoriesNew.csv', sep='/',  header=None)

end_time7 = datetime.now()

duration7=end_time7-start_time7
print(duration7)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_7["section"]=["TLAC"]
#Length 
grouped_data_7["length"] = grouped_data_7['EconomicOperands_t']
                        + grouped_data_7["LogicalConnectors_t"]
                        +grouped_data_7["MathematicalOperators_t"]
                        +grouped_data_7["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_7['cyclomatic'] = grouped_data_7['LogicalConnectors_t']
#Quantity 
grouped_data_7['quantity'] = grouped_data_7['RegulatoryOperators_t']
#Potential 
grouped_data_7['potential'] = 2+ grouped_data_7["EconomicOperands_s"]
#Diversity 
grouped_data_7['diversity'] = grouped_data_7["MathematicalOperators_s"]
                        +grouped_data_7["RegulatoryOperators_s"]
                        +grouped_data_7["LogicalConnectors_s"]
#Level 
grouped_data_7['level']= grouped_data_7['potential']/grouped_data_7['length']
grouped_data_7.to_csv('TLACcategoriesNew.csv', index=False, sep='/') 


#Importing the dataset


start_time8 = datetime.now()

with fitz.open('LEV.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('LEVNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_8= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_LEV= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_LEV)),columns=range(3))
for j in range(len( final_LEV)):
    if final_LEV.iloc[j,2]!=0:
        final.iloc[j,0]=final_LEV.iloc[j,0] 
        final.iloc[j,1]=final_LEV.iloc[j,1]
        final.iloc[j,2]=final_LEV.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors",
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_8=grouped_data_8.set_axis([  "EconomicOperands_s", "Other_s", 
                    "LogicalConnectors_s", "MathematicalOperators_s", 
                    "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",
                    "LogicalConnectors_t", "MathematicalOperators_t",  
                    "RegulatoryOperators_t"], axis=1)
grouped_data_8.to_csv('LEVcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('LEVcategoriesNew.csv', sep='/',  header=None)

end_time8 = datetime.now()

duration8=end_time8-start_time8
print(duration8)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_8["section"]=["LEV"]
#Length 
grouped_data_8["length"] = grouped_data_8['EconomicOperands_t']
                    + grouped_data_8["LogicalConnectors_t"]
                    +grouped_data_8["MathematicalOperators_t"]
                    +grouped_data_8["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_8['cyclomatic'] = grouped_data_8['LogicalConnectors_t']
#Quantity 
grouped_data_8['quantity'] = grouped_data_8['RegulatoryOperators_t']
#Potential 
grouped_data_8['potential'] = 2+ grouped_data_8["EconomicOperands_s"]
#Diversity
grouped_data_8['diversity'] = grouped_data_8["MathematicalOperators_s"]
                    +grouped_data_8["RegulatoryOperators_s"]
                    +grouped_data_8["LogicalConnectors_s"]
#Level 
grouped_data_8['level']= grouped_data_8['potential']/grouped_data_8['length']
grouped_data_8.to_csv('LEVcategoriesNew.csv', index=False, sep='/') 



#Importing the dataset


start_time9 = datetime.now()

with fitz.open('D_SIB.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('D_SIBNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_9= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DSIB= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_DSIB)),columns=range(3))
for j in range(len( final_DSIB)):
    if final_DSIB.iloc[j,2]!=0:
        final.iloc[j,0]=final_DSIB.iloc[j,0] 
        final.iloc[j,1]=final_DSIB.iloc[j,1]
        final.iloc[j,2]=final_DSIB.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other", "LogicalConnectors",
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_9=grouped_data_9.set_axis([  "EconomicOperands_s", "Other_s",
                    "LogicalConnectors_s", "MathematicalOperators_s",  
                    "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",
                    "LogicalConnectors_t", "MathematicalOperators_t",  
                    "RegulatoryOperators_t"], axis=1)
grouped_data_9.to_csv('DSIBcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('DSIBcategoriesNew.csv', sep='/',  header=None)

end_time9 = datetime.now()

duration9=end_time9-start_time9
print(duration9)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_9["section"]=["DSIB"]
#Length 
grouped_data_9["length"] = grouped_data_9['EconomicOperands_t']
                    + grouped_data_9["LogicalConnectors_t"]
                    +grouped_data_9["MathematicalOperators_t"]
                    +grouped_data_9["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_9['cyclomatic'] = grouped_data_9['LogicalConnectors_t']
#Quantity 
grouped_data_9['quantity'] = grouped_data_9['RegulatoryOperators_t']
#Potential 
grouped_data_9['potential'] = 2+ grouped_data_9["EconomicOperands_s"]
#Diversity 
grouped_data_9['diversity'] = grouped_data_9["MathematicalOperators_s"]
                    +grouped_data_9["RegulatoryOperators_s"]
                    +grouped_data_9["LogicalConnectors_s"]
#Level 
grouped_data_9['level']= grouped_data_9['potential']/grouped_data_9['length']
grouped_data_9.to_csv('DSIBcategoriesNew.csv', index=False, sep='/') 


#Importing the dataset


start_time10 = datetime.now()

with fitz.open('IRRBB.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('IRRBBcategoriesNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_10= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_IRRBB= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_IRRBB)),columns=range(3))
for j in range(len( final_IRRBB)):
    if final_IRRBB.iloc[j,2]!=0:
        final.iloc[j,0]=final_IRRBB.iloc[j,0] 
        final.iloc[j,1]=final_IRRBB.iloc[j,1]
        final.iloc[j,2]=final_IRRBB.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", 
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_10=grouped_data_10.set_axis([  "EconomicOperands_s", "Other_s", 
                    "LogicalConnectors_s", "MathematicalOperators_s",  
                    "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",
                    "LogicalConnectors_t", "MathematicalOperators_t",
                    "RegulatoryOperators_t"], axis=1)
grouped_data_10.to_csv('IRRBBcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('IRRBBcategoriesNew.csv', sep='/',  header=None)

end_time10 = datetime.now()

duration10=end_time10-start_time10
print(duration10)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_10["section"]=["IRRBB"]
#Length 
grouped_data_10["length"] = grouped_data_10['EconomicOperands_t']
                    + grouped_data_10["LogicalConnectors_t"]
                    +grouped_data_10["MathematicalOperators_t"]
                    +grouped_data_10["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_10['cyclomatic'] = grouped_data_10['LogicalConnectors_t']
#Quantity 
grouped_data_10['quantity'] = grouped_data_10['RegulatoryOperators_t']
#Potential 
grouped_data_10['potential'] = 2+ grouped_data_10["EconomicOperands_s"]
#Diversity 
grouped_data_10['diversity'] = grouped_data_10["MathematicalOperators_s"]
                    +grouped_data_10["RegulatoryOperators_s"]
                    +grouped_data_10["LogicalConnectors_s"]
#Level 
grouped_data_10['level']= grouped_data_10['potential']/grouped_data_10['length']
grouped_data_10.to_csv('IRRBBcategoriesNew.csv', index=False, sep='/') 


#Importing the dataset


start_time11 = datetime.now()

with fitz.open('IDL.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('IDLNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_11= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_IDL= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_IDL)),columns=range(3))
for j in range(len( final_IDL)):
    if final_IDL.iloc[j,2]!=0:
        final.iloc[j,0]=final_IDL.iloc[j,0] 
        final.iloc[j,1]=final_IDL.iloc[j,1]
        final.iloc[j,2]=final_IDL.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors",
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_11=grouped_data_11.set_axis([  "EconomicOperands_s", "Other_s", 
                    "LogicalConnectors_s", "MathematicalOperators_s",  
                    "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t", 
                    "LogicalConnectors_t", "MathematicalOperators_t",  
                    "RegulatoryOperators_t"], axis=1)
grouped_data_11.to_csv('IDLcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('IDLcategoriesNew.csv', sep='/',  header=None)

end_time11 = datetime.now()

duration11=end_time11-start_time11
print(duration11)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_11["section"]=["IDL"]
#Length 
grouped_data_11["length"] = grouped_data_11['EconomicOperands_t'] 
                    + grouped_data_11["LogicalConnectors_t"]
                    +grouped_data_11["MathematicalOperators_t"]
                    +grouped_data_11["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_11['cyclomatic'] = grouped_data_11['LogicalConnectors_t']
#Quantity 
grouped_data_11['quantity'] = grouped_data_11['RegulatoryOperators_t']
#Potential 
grouped_data_11['potential'] = 2+ grouped_data_11["EconomicOperands_s"]
#Diversity 
grouped_data_11['diversity'] = grouped_data_11["MathematicalOperators_s"]
                    +grouped_data_11["RegulatoryOperators_s"]
                    +grouped_data_11["LogicalConnectors_s"]
#Level 
grouped_data_11['level']= grouped_data_11['potential']/grouped_data_11['length']
grouped_data_11.to_csv('IDLcategoriesNew.csv', index=False, sep='/') 

#Importing the dataset


start_time12 = datetime.now()

with fitz.open('NSF.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('NSFNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_12= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_NSF= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_NSF)),columns=range(3))
for j in range(len( final_NSF)):
    if final_NSF.iloc[j,2]!=0:
        final.iloc[j,0]=final_NSF.iloc[j,0] 
        final.iloc[j,1]=final_NSF.iloc[j,1]
        final.iloc[j,2]=final_NSF.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", 
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_12=grouped_data_12.set_axis([  "EconomicOperands_s", "Other_s", 
                    "LogicalConnectors_s", "MathematicalOperators_s",  
                    "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",
                    "LogicalConnectors_t", "MathematicalOperators_t",  
                    "RegulatoryOperators_t"], axis=1)
grouped_data_12.to_csv('NSFcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('NSFcategoriesNew.csv', sep='/',  header=None)

end_time12 = datetime.now()

duration12=end_time12-start_time12
print(duration12)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_12["section"]=["NSF"]
#Length 
grouped_data_12["length"] = grouped_data_12['EconomicOperands_t']
                        + grouped_data_12["LogicalConnectors_t"]
                        +grouped_data_12["MathematicalOperators_t"]
                        +grouped_data_12["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_12['cyclomatic'] = grouped_data_12['LogicalConnectors_t']
#Quantity 
grouped_data_12['quantity'] = grouped_data_12['RegulatoryOperators_t']
#Potential 
grouped_data_12['potential'] = 2+ grouped_data_12["EconomicOperands_s"]
#Diversity 
grouped_data_12['diversity'] = grouped_data_12["MathematicalOperators_s"]
                        +grouped_data_12["RegulatoryOperators_s"]
                        +grouped_data_12["LogicalConnectors_s"]
#Level 
grouped_data_12['level']= grouped_data_12['potential']/grouped_data_12['length']
grouped_data_12.to_csv('NSFcategoriesNew.csv', index=False, sep='/') 


#Importing the dataset


start_time13 = datetime.now()

with fitz.open('LCR.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('LCRNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_13= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_LCR= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_LCR)),columns=range(3))
for j in range(len( final_LCR)):
    if final_LCR.iloc[j,2]!=0:
        final.iloc[j,0]=final_LCR.iloc[j,0] 
        final.iloc[j,1]=final_LCR.iloc[j,1]
        final.iloc[j,2]=final_LCR.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", 
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_13=grouped_data_13.set_axis([  "EconomicOperands_s", "Other_s", 
                    "LogicalConnectors_s", "MathematicalOperators_s",  
                    "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",
                    "LogicalConnectors_t", "MathematicalOperators_t",  
                    "RegulatoryOperators_t"], axis=1)
grouped_data_13.to_csv('LCRcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('LCRcategoriesNew.csv', sep='/',  header=None)

end_time13 = datetime.now()

duration13=end_time13-start_time13
print(duration13)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_13["section"]=["LCR"]
#Length 
grouped_data_13["length"] = grouped_data_13['EconomicOperands_t']
                    + grouped_data_13["LogicalConnectors_t"]
                    +grouped_data_13["MathematicalOperators_t"]
                    +grouped_data_13["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_13['cyclomatic'] = grouped_data_13['LogicalConnectors_t']
#Quantity 
grouped_data_13['quantity'] = grouped_data_13['RegulatoryOperators_t']
#Potential 
grouped_data_13['potential'] = 2+ grouped_data_13["EconomicOperands_s"]
#Diversity 
grouped_data_13['diversity'] = grouped_data_13["MathematicalOperators_s"]
                    +grouped_data_13["RegulatoryOperators_s"]
                    +grouped_data_13["LogicalConnectors_s"]
#Level 
grouped_data_13['level']= grouped_data_13['potential']/grouped_data_13['length']
grouped_data_13.to_csv('LCRcategoriesNew.csv', index=False, sep='/') 


#Importing the dataset


start_time14 = datetime.now()

with fitz.open('LEX.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('LEXNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_14= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_LEX= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_LEX)),columns=range(3))
for j in range(len( final_LEX)):
    if final_LEX.iloc[j,2]!=0:
        final.iloc[j,0]=final_LEX.iloc[j,0] 
        final.iloc[j,1]=final_LEX.iloc[j,1]
        final.iloc[j,2]=final_LEX.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors", 
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_14=grouped_data_14.set_axis([  "EconomicOperands_s", "Other_s", 
                    "LogicalConnectors_s", "MathematicalOperators_s",  
                    "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t", 
                    "LogicalConnectors_t", "MathematicalOperators_t",  
                    "RegulatoryOperators_t"], axis=1)
grouped_data_14.to_csv('LEXcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('LEXcategoriesNew.csv', sep='/',  header=None)

end_time14 = datetime.now()

duration14=end_time14-start_time14
print(duration14)


"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_14["section"]=["LEX"]
#Length 
grouped_data_14["length"] = grouped_data_14['EconomicOperands_t'] 
                    + grouped_data_14["LogicalConnectors_t"]
                    +grouped_data_14["MathematicalOperators_t"]
                    +grouped_data_14["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_14['cyclomatic'] = grouped_data_14['LogicalConnectors_t']
#Quantity 
grouped_data_14['quantity'] = grouped_data_14['RegulatoryOperators_t']
#Potential 
grouped_data_14['potential'] = 2+ grouped_data_14["EconomicOperands_s"]
#Diversity
grouped_data_14['diversity'] = grouped_data_14["MathematicalOperators_s"]
                    +grouped_data_14["RegulatoryOperators_s"]
                    +grouped_data_14["LogicalConnectors_s"]
#Level 
grouped_data_14['level']= grouped_data_14['potential']/grouped_data_14['length']
grouped_data_14.to_csv('LEXcategoriesNew.csv', index=False, sep='/') 



#Importing the dataset


start_time15 = datetime.now()

with fitz.open('DIS.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('DISNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_15= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_DIS= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_DIS)),columns=range(3))
for j in range(len( final_DIS)):
    if final_DIS.iloc[j,2]!=0:
        final.iloc[j,0]=final_DIS.iloc[j,0] 
        final.iloc[j,1]=final_DIS.iloc[j,1]
        final.iloc[j,2]=final_DIS.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors",
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
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
grouped_data_15=grouped_data_15.set_axis([  "EconomicOperands_s", "Other_s", 
                "LogicalConnectors_s", "MathematicalOperators_s", 
                "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t", 
                "LogicalConnectors_t", "MathematicalOperators_t",  
                "RegulatoryOperators_t"], axis=1)
grouped_data_15.to_csv('DIScategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('DIScategoriesNew.csv', sep='/',  header=None)

end_time15 = datetime.now()

duration15=end_time15-start_time15
print(duration15)



#Importing the dataset


start_time16 = datetime.now()

with fitz.open('SEC.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText()
        text=text.encode('ascii','ignore').decode()
text=text.replace("[^a-zA-z\s]","." )
text=text.replace(",","." )
text=text.replace("e.g.","." )
text=text.replace("- ","." )
text=text.replace(" -","." )
text=text.replace(" - ","." )
text=text.replace("*","." )
text=text.replace(":","." )
text=text.replace(";","." )
text=text.replace("(","." )
text=text.replace(")","." )
text=text.replace("+","." )
text=text.replace("' ","." )
text=text.split("." )
for j in range(len(text)-1):
    text[j]=text[j].replace("\n"," " )
    text[j]=text[j].replace("'s"," " )
    text[j]=text[j].replace("the","" )
    text[j]=text[j].replace("that","" )
    text[j]=text[j].upper()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('SECNew.csv', index=False, sep='/')
text= text['text'].values.tolist()

# Loop through each line of the file

grouped_data_16= pd.DataFrame( columns=range(10))

for i in range(0, len(text)):
    for key in keys_dict:
        if key in text[i]:
            keys_dict[key] = keys_dict[key] + 1
            Freq= pd.DataFrame(keys_dict.items(), columns=['key', 'freq'])
            final_SEC= pd.merge(dataset, Freq, on='key')
#Droping keys for which frequency==0
final= pd.DataFrame(index=range(len(final_SEC)),columns=range(3))
for j in range(len( final_SEC)):
    if final_SEC.iloc[j,2]!=0:
        final.iloc[j,0]=final_SEC.iloc[j,0] 
        final.iloc[j,1]=final_SEC.iloc[j,1]
        final.iloc[j,2]=final_SEC.iloc[j,2] 
final['key'] = final[0]
final['category'] = final[1]
final['freq'] = final[2]
            #Droping missing (nan) values
final=final.dropna()
            #Descriptive statistics 
            #Grouping and perform count over each group
column_names = [ "EconomicOperands", "Other",  "LogicalConnectors",
                "MathematicalOperators", "RegulatoryOperators"]
matrix = pd.DataFrame(columns = column_names)
matrix=matrix.T
matrix_s= final.groupby('category')['category'].count()
matrix_s=matrix_s.to_frame(name='count')
matrix_s=pd.concat([matrix, matrix_s], axis=1)
matrix_str=matrix_s.T
matrix_str= matrix_str.add_suffix('_s')
matrix_t= final.groupby('category')['freq'].sum()
matrix_t=matrix_t.to_frame(name='count')
matrix_t=pd.concat([matrix, matrix_t], axis=1)
matrix_ttr=matrix_t.T
matrix_ttr= matrix_ttr.add_suffix('_t')
final_matrix = pd.concat([matrix_str, matrix_ttr], axis=1)
grouped_data_16=final_matrix.iloc[0]
    #We refresh the count in the dictionary to loop over the next line 
keys_dict = keys.to_dict('records')
keys_dict = keys.set_index('key').T.to_dict('records')[0]
print(grouped_data_16)

grouped_data_16=pd.DataFrame(grouped_data_16)
grouped_data_16 = grouped_data_16.T
grouped_data_16=grouped_data_16.set_axis([  "EconomicOperands_s", "Other_s", 
                    "LogicalConnectors_s", "MathematicalOperators_s",  
                    "RegulatoryOperators_s",  "EconomicOperands_t", "Other_t",
                    "LogicalConnectors_t", "MathematicalOperators_t",  
                    "RegulatoryOperators_t"], axis=1)
grouped_data_16.to_csv('SECcategoriesNew.csv', index=False, sep='/')
datasetx = pd.read_csv('SECcategoriesNew.csv', sep='/',  header=None)

end_time16 = datetime.now()

duration16=end_time16-start_time16
print(duration16)

"""
Computing complexity measures given the formulas introduced in 
Colliard and Georg 2020

"""

grouped_data_16["section"]=["SEC"]
#Length 
grouped_data_16["length"] = grouped_data_16['EconomicOperands_t'] 
                        + grouped_data_16["LogicalConnectors_t"]
                        +grouped_data_16["MathematicalOperators_t"]
                        +grouped_data_16["RegulatoryOperators_t"]
#Cyclomatic 
grouped_data_16['cyclomatic'] = grouped_data_16['LogicalConnectors_t']
#Quantity 
grouped_data_16['quantity'] = grouped_data_16['RegulatoryOperators_t']
#Potential 
grouped_data_16['potential'] = 2+ grouped_data_16["EconomicOperands_s"]
#Diversity 
grouped_data_16['diversity'] = grouped_data_16["MathematicalOperators_s"]
                        +grouped_data_16["RegulatoryOperators_s"]
                        +grouped_data_16["LogicalConnectors_s"]
#Level 
grouped_data_16['level']= grouped_data_16['potential']/grouped_data_16['length']
grouped_data_16.to_csv('SECcategoriesNew.csv', index=False, sep='/') 


