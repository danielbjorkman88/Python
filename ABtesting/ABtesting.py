# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:04:33 2020

@author: malyr
"""

#AB-testing

import numpy as np
from scipy.stats import beta
import pandas as pd
import matplotlib.pyplot as plt


# Function:
# Beta(alpha = Sucesses, beta = Failures)

# Prior Beliefs
# Like odds, but Higher number -> Stronger belief
param_alpha = 8
param_beta = 42

# True sucess rate / click rate 
A_measured = 0.15
B_measured = 0.20


np.random.seed(42)


group_size = 1000
A_group , B_group = np.random.rand(2, group_size)

A_successes = sum(A_group < A_measured) # 15% Click rate
B_successes = sum(B_group < B_measured) # 20% Click rate

A_failures = group_size - A_successes
B_failures = group_size - B_successes

# A_posterior = prior + A's measured data
A_posterior = beta(A_successes + param_alpha, 
                   A_failures + param_beta)

# B_posterior = prior + B's measured data
B_posterior = beta(B_successes + param_alpha,
                   B_failures + param_beta)

plt.figure()

x = np.linspace(0.01, 0.99, 1000)
plt.plot(x, A_posterior.pdf(x), '-', lw=2, label='A variant. Mean = ' + str(A_posterior.expect()))
plt.plot(x, B_posterior.pdf(x), '-', lw=2, label='B variant. Mean = ' + str(B_posterior.expect()))
plt.legend()

plt.title('Posterior probabilities', fontsize = 14)
plt.show()



# Monte carlo simulation
n_trails = 100000

A_samples = pd.Series([A_posterior.rvs() \
                      for _ in range(n_trails)])

B_samples = pd.Series([B_posterior.rvs() \
                      for _ in range(n_trails)])

B_wins = sum(B_samples > A_samples)

B_wins_percent = B_wins / n_trails





