# -*- coding: utf-8 -*-
"""
Created on Tue May  5 14:38:22 2020

@author: malyr
"""

import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
#from sklearn.utils import shuffle
import os
import matplotlib.pyplot as plt
import pickle

path = r'C:\Users\malyr\OneDrive\Dokument\GitHub\Python\ML\Data'

os.chdir(path )

data = pd.read_csv("student-mat.csv", sep = ";")

data = data[["G1" , "G2", "G3"]] #, "studytime" , "failures", "absences"]]

predict = "G3"

x = np.array(data.drop([predict],1)) # Features
y = np.array(data[predict]) #labels

  
best = 0
for _ in range(30):
    x_train , x_test, y_train , y_test = sklearn.model_selection.train_test_split(x,y, test_size = 0.1)
    
    linear = linear_model.LinearRegression()
    
    linear.fit(x_train , y_train)
    acc = linear.score(x_test, y_test)
    print(acc)
    
    if acc > best:
        with open("studentGradePredictor.pickle","wb") as f:
            pickle.dump(linear, f)

pickle_in = open("studentGradePredictor.pickle", "rb")
linear = pickle.load(pickle_in)

print("Coefficients: \n" , linear.coef_)
print("Intercept: \n", linear.intercept_)

predictions = linear.predict(x_test)






for dimension in range(x.shape[1]):
    #dimension = 1
    p = data.drop([predict],1).keys()[dimension]
    plt.figure()
    
    #plt.scatter(x_train[:,dimension], y_train, label = 'Training data')
    #plt.scatter(x_test[:,dimension], y_test, label = 'Testing data')
    plt.scatter(data[p], data[predict], label = "Data")
    plt.scatter(x_test[:,dimension], predictions, label = 'Predicted ' + predict)
    
    linelength = 20
    xes = [0,linelength]
    yes = [linear.intercept_, linelength*linear.coef_[1] + linear.intercept_ ]
    plt.plot(xes , yes , label = 'Best fit')
    
    plt.xlabel(p)
    plt.ylabel('Final Grade ' + predict)
    plt.plot()
    plt.grid(linewidth = 0.3)
    plt.legend()
    plt.show()


