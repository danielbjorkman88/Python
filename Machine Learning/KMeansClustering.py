# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:12:04 2020

@author: malyr
"""

#K-Means Clustering

import numpy as np
import sklearn
from sklearn.preprocessing import scale
from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from sklearn import metrics

digits = load_digits()
data = scale(digits.data) # Scales digit values to between -1 and 1
y = digits.target

k = len(np.unique(y))

samples, featurs = data.shape
 

def bench_k_means(estimator, name, data):
    estimator.fit(data)
    print('%-9s\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, estimator.inertia_,
             metrics.homogeneity_score(y, estimator.labels_),
             metrics.completeness_score(y, estimator.labels_),
             metrics.v_measure_score(y, estimator.labels_),
             metrics.adjusted_rand_score(y, estimator.labels_),
             metrics.adjusted_mutual_info_score(y,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean')))
    
clf = KMeans(n_clusters = k, init ='random' , n_init = 10)
bench_k_means(clf, "1", data)
  
    



