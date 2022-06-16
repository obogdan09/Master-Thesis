#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 21:36:35 2022

@author: bogdanolena
"""

#Importing used libraries 

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn import tree
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
np.random.seed(500)


# PREPROCESSING THE DATA

classifier = pd.read_csv('keys.csv',  sep=';',  header=0,encoding = 'latin1')
testing = pd.read_csv('verificationSet.csv',  sep=';',  header=0)
multinomialData = pd.concat([classifier, testing], axis=0)
multinomialData=multinomialData.reset_index()
del multinomialData["index"]

key = multinomialData["key"]
y=multinomialData["category"]
for i in range(0, len(y)):
    if y[i]=="Attributes":
        y[i]="EconomicOperands"
    if y[i]=="FunctionWords":
        y[i]="Other"
    if y[i]=="LegalReferences":
        y[i]="Other"
y = pd.Categorical(y) #to create numerical categories 



print("We have {} unique classes".format(len(y.unique())))
#We have 5 unique classes





vectorizer=TfidfVectorizer(max_features=300)
X_testing = vectorizer.fit_transform(key) 
X_train=X_testing[:9099]
X_test=X_testing[9099:]
y_train=y[:9099]
y_test=y[9099:]

# Classifying using TFidVectorizer 

"-----Naive Bayes-----"

clf = MultinomialNB()
# Train the model using the training data
clf.fit(X_train, y_train)
# Predict the categories of the test data
predicted_categories = clf.predict(X_test)

#accuracy score

print("The accuracy is {}".format(
    accuracy_score(y_test, predicted_categories)*100), '%')
#The accuracy is 87.33108108108108  %

"-----SVM-----"




vectorizer=TfidfVectorizer(max_features=3000)
X_testing = vectorizer.fit_transform(key) 
X_train=X_testing[:9099]
X_test=X_testing[9099:]
y_train=y[:9099]
y_test=y[9099:]

# Classifier - Algorithm - SVM
# fit the training dataset on the classifier
SVM = svm.SVC(C=1, kernel='linear', degree=10, gamma="auto")
SVM.fit(X_train,y_train)
# predict the labels on validation dataset
predictions_SVM = SVM.predict(X_test)

matrix=confusion_matrix(y_test, predictions_SVM)
cm=pd.DataFrame(matrix,index=['EO', 'Other', 'LC', 'RO', 'MO'],
                columns=['EO', 'Other', 'LC', 'RO', 'MO'])
print(cm)

#accuracy score

print("The accuracy is {}",accuracy_score(predictions_SVM, y_test)*100, '%')
#The accuracy is 87.9222972972973 %%

import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(matrix.T, square=True, cmap="PiYG",  annot=True, fmt='d', 
            cbar=False, annot_kws={'size':16},
            xticklabels=['EO','Other', 'LC', 'RO', 'MO'],
            yticklabels=['EO','LR', 'Other', 'LC', 'RO', 'MO'], ax=ax)
plt.xlabel('true category')
plt.ylabel('predicted category');


"-----Decision Trees classifier-----"


clf = tree.DecisionTreeClassifier(criterion="entropy", max_depth=6)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

#accuracy score

print("The accuracy is {}",accuracy_score(y_test, y_pred)*100, '%')
#The accuracy is 86.2331081081081 %

"-----K Neighbors Classifier-----"


knn = KNeighborsClassifier(n_neighbors=100)
clf = knn.fit(X_train, y_train)
predicted = clf.predict(X_test)

#accuracy score

print('The accuracy is {}',np.mean(predicted == y_test)*100, '%')

#The accuracy is 83.5304054054054 %

