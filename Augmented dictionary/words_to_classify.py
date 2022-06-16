#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:10:23 2022

@author: bogdanolena
"""


# Importing the libraries
import numpy as np
import pandas as pd
import fitz  # this is pymupdf, to import the text
from datetime import datetime #to measure the time the program takes to execute 
# Importing the datasets





with fitz.open('basel_.I.pdf') as doc:
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
    text[j]=text[j].lower()

text = pd.DataFrame(text, columns = ['text'])
text.to_csv('Basel_1_text.csv', index=False, sep='/')

 

with fitz.open("basel_.II.pdf") as doc:
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
    text[j]=text[j].lower()
text = pd.DataFrame(text, columns = ['text'])
text.to_csv('Basel_2_text.csv', index=False, sep='/')





with fitz.open("basel_.III.pdf") as doc:
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
    text[j]=text[j].lower()
text = pd.DataFrame(text, columns = ['text'])
text.to_csv('Basel_3_text.csv', index=False, sep='/')




#For the moment, I will not work with Basel IV as there are a lot of formulas which are 
#difficult to render in python and they are also a dimension of complexity 

with fitz.open("Basel_3.5.pdf") as doc:
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
    text[j]=text[j].lower()
text = pd.DataFrame(text, columns = ['text'])
text.to_csv('Basel_3.5_text.csv', index=False, sep='/', encoding='utf-8', errors='strict')




    
    
dataset1 = pd.read_csv('Basel_1_text.csv',  sep='/',  header=0,encoding = 'latin1')
dataset2 = pd.read_csv('Basel_2_text.csv', sep='/',  header=0, encoding = 'latin1')
dataset3 = pd.read_csv('Basel_3_text.csv',  sep='/',  header=0, encoding = 'latin1')
dataset4 = pd.read_csv('Basel_3.5_text.csv',  sep='/',  header=0, encoding = 'latin1')
dataset = pd.concat([dataset1, dataset2, dataset3, dataset4])
dataset.to_csv('BaselTotal.csv')
#I need to get rid of NaN values. 

datasetNew=[]
for i in range(0, len(dataset)):
     if pd.isnull(dataset["text"].iloc[i] ) == False:
         datasetNew.append(dataset["text"].iloc[i])
dataset=pd.DataFrame(datasetNew, columns=['text'])

X = dataset.loc[:,["text"] ].values

#Tranforming a ndarray of objects into the list 

X=X.tolist()
for i in range(0, len(X)):
    mystring= ' '
    for x in X[i]:
        if type(x) != float:
            mystring += x.upper()
    X[i]=mystring
    X[i]=X[i].split()

#Eliminating the objects in X that are repeated 
s = []
for i in X:
    if i not in s:
        s.append(i)
    
X=s

#Save the dataset for further use 

x = pd.Series(X)
x.to_csv('datasetNew.csv')


#Extracting the words/concepts which are not classified in the dictionary 

#------Words to classify


#In this first step, I eliminate all Logical connectors and Function words from the analysis
#as I may need them to re-contruct n-grams in the expanded dictionary 
#for example, there may be the case where the word 'to' belongs to an
#expression of words, for instance 'with regards to' or 'with reference to'
classifier_complete = pd.read_csv('keys.csv',  sep=';',  header=0, encoding = 'latin1')
listOfClass=[]
for i in range(0, len(classifier_complete)):
    if classifier_complete['category'][i] != 'LogicalConnectors':
        if classifier_complete['category'][i] != 'FunctionWords':
            listOfClass.append(classifier_complete['key'][i])

listOfClassComplete=[]
for i in range(0, len(classifier_complete)):
    listOfClassComplete.append(classifier_complete['key'][i])



#len(listOfClass)=8,647

#First, to find all n-grams present in the Colliard and Georg 2020 dictionary

#5grams 


NotClassified=[] 
for i in range(0, len(X)):
    if len(X[i])<5:
        for j in range(0, len(X[i])):
            NotClassified.append(X[i][j])
    else: 
        for j in range(0, len(X[i])-5):

            if j<len(X[i])-5:
                if X[i][j] + ' ' + X[i][j+1] + ' ' + X[i][j+2] + ' ' + X[i][j+3] + ' ' + X[i][j+4] not in listOfClass:
                    NotClassified.append( X[i][j])
                    j+=1
            if j<len(X[i])-5:
                if X[i][j] + ' ' + X[i][j+1] + ' ' + X[i][j+2] + ' ' + X[i][j+3] + ' ' + X[i][j+4]  in listOfClass:
                    j+=5
                    
            if j ==len(X[i])-5:
                if X[i][j] + ' ' + X[i][j+1] + ' ' + X[i][j+2] + ' ' + X[i][j+3]+ ' ' + X[i][j+4]  not in listOfClass:
                    NotClassified.append( X[i][j])
                    NotClassified.append( X[i][j+1])
                    NotClassified.append( X[i][j+2])
                    NotClassified.append( X[i][j+3])
                    NotClassified.append( X[i][j+4])
            if j>len(X[i])-5:
                k=len(X[i])-j
                if k==1:
                    NotClassified.append( X[i][j])
                if k==2:
                    NotClassified.append( X[i][j])
                    NotClassified.append( X[i][j+1])
                if k==3:
                    NotClassified.append( X[i][j])
                    NotClassified.append( X[i][j+1])
                    NotClassified.append( X[i][j+2])
                if k==4:
                    NotClassified.append( X[i][j])
                    NotClassified.append( X[i][j+1])
                    NotClassified.append( X[i][j+2])
                    NotClassified.append( X[i][j+3])

                
#len(NotClassified)=415,969
 
#4grams

NotClassified2=[]

for i in range(0, len(NotClassified)-4):
    if i<len(NotClassified)-4:
        if NotClassified[i] + ' ' + NotClassified[i+1] + ' ' + NotClassified[i+2]+ ' ' + NotClassified[i+3] not in listOfClass:
            NotClassified2.append( NotClassified[i])
            i+=1
        if NotClassified[i] + ' ' + NotClassified[i+1] + ' ' + NotClassified[i+2]+ ' ' + NotClassified[i+3] in listOfClass:
            i+=4
    if i ==len(NotClassified)-4:
        if NotClassified[i] + ' ' + NotClassified[i+1] + ' ' + NotClassified[i+2]+ ' ' + NotClassified[i+3] not in listOfClass:
            NotClassified2.append( NotClassified[i])
            NotClassified2.append( NotClassified[i+1])
            NotClassified2.append( NotClassified[i+2])
            NotClassified2.append( NotClassified[i+3])
    if i>len(NotClassified)-4:
        k=len(NotClassified)-i
        if k==1:
            NotClassified2.append( NotClassified[i])
        if k==2:
            NotClassified2.append( NotClassified[i])
            NotClassified2.append( NotClassified[i+1])
        if k==3:
            NotClassified2.append( NotClassified[i])
            NotClassified2.append( NotClassified[i+1])
            NotClassified2.append( NotClassified[i+2])
            print(i)
            print(k)
                


##len(NotClassified2)=415,944

#3grams 



NotClassified3=[]

for i in range(0, len(NotClassified2)-3):
    if i<len(NotClassified2)-3:
        if NotClassified2[i] + ' ' + NotClassified2[i+1] + ' ' + NotClassified2[i+2] not in listOfClass:
            NotClassified3.append( NotClassified2[i])
            i+=1
        if NotClassified2[i] + ' ' + NotClassified2[i+1] + ' ' + NotClassified2[i+2] in listOfClass:
            i+=3
    if i ==len(NotClassified2)-3:
        if NotClassified2[i] + ' ' + NotClassified2[i+1] + ' ' + NotClassified2[i+2] not in listOfClass:
            NotClassified3.append( NotClassified2[i])
            NotClassified3.append( NotClassified2[i+1])
            NotClassified3.append( NotClassified2[i+2])
    if i>len(NotClassified2)-3:
        k=len(NotClassified2)-i
        if k==1:
            NotClassified3.append( NotClassified2[i])
        if k==2:
            NotClassified3.append( NotClassified2[i])
            NotClassified3.append( NotClassified2[i+1])
            print(i)
            print(k)
            
##len(NotClassified3)=415,798
                


#2grams 


NotClassified4=[]

for i in range(0, len(NotClassified3)-2):
    if i<len(NotClassified3)-2:
        if NotClassified3[i] + ' ' + NotClassified3[i+1] not in listOfClass:
            NotClassified4.append( NotClassified3[i])
            i+=1
        if NotClassified3[i] + ' ' + NotClassified3[i+1] in listOfClass:
            i+=2
    if i ==len(NotClassified3)-2:
        if NotClassified3[i] + ' ' + NotClassified3[i+1] not in listOfClass:
            NotClassified4.append( NotClassified3[i])
            NotClassified4.append( NotClassified3[i+1])
    if i>len(NotClassified3)-3:
        k=len(NotClassified3)-i
        if k==1:
            NotClassified4.append( NotClassified3[i])
            

#len(NotClassified4)=408,270

#1gram

NotClassified5=[]

for i in range(0, len(NotClassified4)):
    if NotClassified4[i] not in listOfClass:
        NotClassified5.append(NotClassified4[i])
        
#len(NotClassified5)=209,552


#Thus, we have 209,552 words that have to be classified, given that an 
#important proportion may still be logical connectors or function words 

#We can determine how many words were not classified (excluding logical connectors and function words)
#This is not useful in terms of analysis but will provide with more exact number of not classified terms


NotClassifiedNoLogic=[]

listOfClassComplete=[]
for i in range(0, len(classifier_complete)):
    listOfClassComplete.append(classifier_complete['key'][i])
for i in range(0, len(NotClassified5)):
    if NotClassified5[i] not in listOfClassComplete:
        NotClassifiedNoLogic.append(NotClassified5[i])
        

#len(NotClassifiedNoLogic)=53,749


#See the first 10 terms: 
    
print(NotClassifiedNoLogic[:10])

#['BASLE', '1987', 'CONVERGENCE', 'DECEMBER', 'CONVERGENCE', 'BASLE', 'JULY', '1988', 'CONSULTATIVE', 'CONTENTS']





#------------
To detect duplicates 

s = []
for i in NotClassifiedNoLogic:
    if i not in s:
        s.append(i)

NotClassifiedNoLogic=s

#len(NotClassifiedNoLogic)=6,809
#------------
NotClassifiedNoLogic = [s.replace('"', '') for s in NotClassifiedNoLogic]
NotClassifiedNoLogic = [s.replace('?', '') for s in NotClassifiedNoLogic]
NotClassifiedNoLogic = [s.replace('[', '') for s in NotClassifiedNoLogic]
NotClassifiedNoLogic = [s.replace(']', '') for s in NotClassifiedNoLogic]
NotClassifiedNoLogic = [s.replace('/', ' ') for s in NotClassifiedNoLogic]
NotClassifiedNoLogic = [s.replace('--', ' ') for s in NotClassifiedNoLogic]


#Save the dataset for further use 

NotClassifiedNoLogic = pd.Series(NotClassifiedNoLogic)
NotClassifiedNoLogic.to_csv('notClassified.csv')


