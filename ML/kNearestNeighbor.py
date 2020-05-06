# -*- coding: utf-8 -*-
"""
Created on Wed May  6 12:18:34 2020

@author: malyr
"""

#k-nearest neighbor

import pandas as pd
import numpy as np
import sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn import linear_model , preprocessing
from sklearn.utils import shuffle
import os
import matplotlib.pyplot as plt
import pickle

path = r'C:\Users\malyr\OneDrive\Dokument\GitHub\Python\ML\Data'

os.chdir(path )

data = pd.read_csv("car.data")

le = preprocessing.LabelEncoder()
buying = le.fit_transform( list(data["buying"]))
maint = le.fit_transform( list(data["maint"]))
door = le.fit_transform( list(data["door"]))
persons = le.fit_transform( list(data["persons"]))
lug_boot = le.fit_transform( list(data["lug_boot"]))
safety = le.fit_transform( list(data["safety"]))
cls = le.fit_transform( list(data["class"]))

predict = "class"
labelNames = data.drop([predict],1).keys()
#processedData = np.zeros([data.shape[0], len(labelNames)])
#for i in range(len(labelNames)):
#    processedData[:,i] = le.fit_transform( list(data[labelNames[i]]))

x = list(zip(buying , maint , door, persons , lug_boot , safety))
y = list(cls)

x_train , x_test, y_train , y_test = sklearn.model_selection.train_test_split(x,y, test_size = 0.1)

model = KNeighborsClassifier(n_neighbors= 9)

model.fit(x_train, y_train)
acc = model.score(x_test , y_test)
print(acc)

predicted = model.predict(x_test)


names = ["unacc" , "acc" , "good", "vgood"]

for x in range(len(x_test)):
    print("Pridicted: " , names[predicted[x]], "Data: ", x_test[x], "Actual: ", names[y_test[x]])




#
#for dimension in range(x.shape[1]):
#    p = labelNames[dimension]
#    plt.figure()
#    
#    #plt.scatter(x_train[:,dimension], y_train, label = 'Training data')
#    #plt.scatter(x_test[:,dimension], y_test, label = 'Testing data')
#    plt.scatter(data[p], data[predict], label = "Data")
#    predictions = linear.predict(x_test)
#    plt.scatter(x_test[:,dimension], predictions, label = 'Predicted ' + predict)
#
#    plt.plot(xes , yes , label = 'Best fit', color = 'r')
#    
#    plt.xlabel(p)
#    plt.ylabel('Final Grade ' + predict)
#    plt.plot()
#    plt.grid(linewidth = 0.3)
#    plt.legend()
#    plt.show()












