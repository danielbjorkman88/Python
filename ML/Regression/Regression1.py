# -*- coding: utf-8 -*-
"""
Created on Tue May  5 14:38:22 2020

@author: malyr
"""

import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import os
import maplotlib.pyplot as plt

path = r'C:\Users\malyr\OneDrive\Dokument\GitHub\Python\ML\Data'

os.chdir(path )

data = pd.read_csv("student-mat.csv", sep = ";")

data = data[["G1" , "G2", "G3", "studytime" , "failures", "absences"]]

predict = "G3"

x = np.array(data.drop([predict],1)) # Features
y = np.array(data[predict]) #labels

x_train , x_test, y_train , y_test = sklearn.model_selection.train_test_split(x,y, test_size = 0.1)

linear = linear_model.LinearRegression()

linear.fit(x_train , y_train)
acc = linear.score(x_test, y_test)
print(acc)

print("Coefficient: \n" , linear.coef_)
print("Intercept: \n", linear.intercept_)

predictions = linear.predict(x_test)


