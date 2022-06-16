#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 14:36:28 2022

@author: bogdanolena

This document  creates an augmented dataset for the training of the encoding model
"""


from functools import reduce
import operator

with open("BaselFramework.txt") as file: 
    lines=file.read().splitlines()
    print(lines)
lines = list(filter(None, lines))



for i in range(0, len(lines)):
    listNew=[]
    lines[i]= list(lines[i].split(" "))
    lines[i] = list(filter(None, lines[i]))
    listNew.append(lines[i])
    lines[i] =listNew
    
    

for i in range(0, len(lines)):
    listNew=[]
    out = reduce(operator.concat, lines[i])
    for k in range(0, len(out)):
        if type(out[k]) !=str:
            out[k] =str(out[k])
        out[k]=out[k].upper()
    lines[i]=out



augment_data = X + lines
X=augment_data

