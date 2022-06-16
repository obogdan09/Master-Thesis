#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:56:42 2022

@author: bogdanolena
"""

#Importing used libraries 

import gensim
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
import tensorflow_hub as hub
import tensorflow as tf
from tensorflow.keras.layers import Input, Lambda, Bidirectional, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras import layers 
from keras import backend as K
#Calculate confusion matrix
from sklearn.metrics import confusion_matrix
from functools import reduce
import operator


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
y = pd.Categorical(y)

print (y.unique())

#Loading the dataset for Word2Vec to be trained on 
#This dataset contains all four Basel Accords

dataset = pd.read_csv('datasetNew.csv', header=0)
X=[]
for i in range(0, len(dataset)):
    X.append(dataset.iloc[i][1])
del dataset["Unnamed: 0"]
print(X)


#Traing our Word2Vec Model

model = gensim.models.Word2Vec(X, vector_size=115,window=5,min_count=1)
np.random.seed(500) 


def get_vect(word, model):
    try:
        return model.wv[word]
    except KeyError:
        return np.zeros((model.vector_size,))

def sum_vectors(phrase, model):
    return sum(get_vect(w, model) for w in phrase)

def word2vec_features(X, model):
    feats = np.vstack([sum_vectors(p, model) for p in X])
    return feats




#For Logistic Regression, SVM and Regression tree classifier we need the input 
#set to be already transformed using our Word2Vec. 

key_feat= word2vec_features(key, model)
wv_train_feat=key_feat[:9099]
wv_test_feat=key_feat[9099:]
y_train=y[:9099]
y_test=y[9099:]

key_train=key[:9099]
key_test=key[9099:]



"------Logistic regression-----" 




clfwv = LogisticRegression(solver='lbfgs', max_iter=1000, verbose=5)
clfwv.fit(wv_train_feat, y_train)
y_predicted= clfwv.predict(wv_test_feat)
y_predicted= pd.Categorical(y_predicted)
print("The accuracy is ",clfwv.score(wv_test_feat, y_test)*100, "%")
matrix=confusion_matrix(y_test, y_predicted)
cm=pd.DataFrame(matrix,index=['EO', 'Other', 'LC', 'RO', 'MO'],
                columns=['EO', 'Other', 'LC', 'RO', 'MO'])
print(cm)

#The accuracy is 79.8141891891892 %


"------Decision Tree classifier-----" 


clf = tree.DecisionTreeClassifier(criterion="entropy", max_depth=6)
clf.fit(wv_train_feat, y_train)
clf.score(wv_train_feat, y_train)
#Predict the response for test dataset
y_pred = clf.predict(wv_test_feat)
print("The accuracy is ",metrics.accuracy_score(y_test, y_pred)*100, "%")

#The accuracy is  80.4054054054054 %


"------K Neighbors Classifier-----" 



knn = KNeighborsClassifier(n_neighbors=100)
knn = knn.fit(wv_train_feat, y_train)
predicted = knn.predict(wv_test_feat)
print('The accuracy is ',np.mean(predicted == y_test)*100, '%')

#The accuracy is 80.91216216216216%

"------SVM-----" 



# fit the training dataset on the classifier
SVM = svm.SVC(C=1, kernel='linear', degree=10, gamma='auto')
SVM.fit(wv_train_feat, y_train)
# predict the labels on validation dataset
predictions_SVM = SVM.predict(wv_test_feat)
# Use accuracy_score function to get the accuracy
print("The accuracy is ",accuracy_score(predictions_SVM, y_test)*100, "%")
matrix=confusion_matrix(y_test, predictions_SVM)
cm=pd.DataFrame(matrix,index=['EO', 'Other', 'LC', 'RO', 'MO'],
                columns=['EO', 'Other', 'LC', 'RO', 'MO'])
print(cm)

#The accuracy is 81.58783783783784 %

"""
        EO  Other  LC   RO  MO
EO     817      0   0   27   0
Other   35      0   0    5   0
LC      24      0   0    0   0
RO      98      0   0  154   0
MO      24      0   0    0   0

"""
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(matrix.T, square=True, cmap="PiYG",  annot=True, fmt='d', 
            cbar=False, annot_kws={'size':16},
            xticklabels=['EO','Other', 'LC', 'RO', 'MO'],
            yticklabels=['EO','LR', 'Other', 'LC', 'RO', 'MO'], ax=ax)
plt.xlabel('true category')
plt.ylabel('predicted category');



"------Feed-forward networks using pre-trained ELMO model-----" 


#Importing ELMo model:


tf.compat.v1.disable_eager_execution()
elmo = hub.Module("https://tfhub.dev/google/elmo/3", trainable=True)



def ELMoEmbedding(input_text):
    return elmo(tf.reshape(tf.cast(input_text, tf.string), [-1]), 
                signature="default", as_dict=True)["elmo"]
def build_model():
    input_layer = Input(shape=(1,), dtype="string", name="Input_layer")
    embedding_layer = Lambda(ELMoEmbedding, output_shape=(500, ), 
                             name="Elmo_Embedding")(input_layer)
    BiLSTM = Bidirectional(layers.LSTM(500, return_sequences= False, 
        recurrent_dropout=0.2, dropout=0.2), name="BiLSTM")(embedding_layer)
    Dense_layer_1 = Dense(450, activation='relu')(BiLSTM)
    Dropout_layer_1 = Dropout(0.5)(Dense_layer_1)
    Dense_layer_2 = Dense(350, activation='relu')(Dropout_layer_1)
    Dropout_layer_2 = Dropout(0.5)(Dense_layer_2)
    output_layer = Dense(1, activation='sigmoid')(Dropout_layer_2)
    model = Model(inputs=[input_layer], outputs=output_layer, 
                  name="BiLSTM with ELMo Embeddings")
    model.summary()
    model.compile(loss='binary_crossentropy',optimizer='adam',
                  metrics=['accuracy'])
    return model
elmo_BiDirectional_model = build_model()


tf.compat.v1.disable_eager_execution()

tf.compat.v1.experimental.output_all_intermediates(True)

init = tf.compat.v1.global_variables_initializer()

with tf.compat.v1.Session() as sess:
    sess.run(init)
    model_elmo = elmo_BiDirectional_model.fit(key_train, y_train, epochs=1, 
                                              batch_size=64)
    train_prediction = elmo_BiDirectional_model.predict(key_train)
    test_prediction =  elmo_BiDirectional_model.predict(key_test)
from sklearn.metrics import accuracy_score

print("The accuracy is:",accuracy_score(y_test,test_prediction), "%")

#The accuracy is 71.28378378378378 %
