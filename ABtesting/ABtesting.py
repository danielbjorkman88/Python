# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:04:33 2020

@author: malyr
"""

#AB-testing

import numpy as np
from scipy.stats import beta
import pandas as pd



np.random.seed(42)


group_size = 1000
A_group , B_group = np.random.rand(2, group_size)

A_successes = sum(A_group < 0.15) # 15% Click rate
B_successes = sum(B_group < 0.20) # 20% Click rate

A_failures = group_size - A_successes
B_failures = group_size - B_successes

A_posterior = beta(A_successes + 8,
                   A_failures + 42)

B_posterior = beta(B_successes + 8,
                   B_failures + 42)



# Monte carlo simulation
n_trails = 100000

A_samples = pd.Series([A_posterior.rvs() \
                      for _ in range(n_trails)])

B_samples = pd.Series([B_posterior.rvs() \
                      for _ in range(n_trails)])

B_wins = sum(B_samples > A_samples)

B_wins_percent = B_wins / n_trails





