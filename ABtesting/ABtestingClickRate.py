# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:04:33 2020

@author: Daniel Björkman
"""

#AB-testing

import numpy as np
from scipy.stats import beta
import pandas as pd
import matplotlib.pyplot as plt


# Function:
# Beta(alpha = Sucesses, beta = Failures)

estimated_sucess_rate = 16 # percent
confidence = 0.5 # Higher number -> Stronger belief

# Prior Beliefs
param_alpha = estimated_sucess_rate * confidence
param_beta = (100 - estimated_sucess_rate) * confidence

# True measured sucess rate / click rate 
A_measured = 0.15 # 15% Click rate
B_measured = 0.20 # 20% Click rate



# Simulating exposing customers to product
np.random.seed(42)
group_size = 1000
A_group , B_group = np.random.rand(2, group_size)

A_successes = sum(A_group < A_measured) 
B_successes = sum(B_group < B_measured) 

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

plt.ylabel('Density', fontsize = 18)
plt.xlabel('Sucess rate', fontsize = 18)
plt.title('Posterior probabilities', fontsize = 14)
plt.grid(linewidth = 0.3)
plt.show()



# Monte carlo simulation
n_trails = 100000
A_samples = pd.Series([A_posterior.rvs() \
                      for _ in range(n_trails)])

B_samples = pd.Series([B_posterior.rvs() \
                      for _ in range(n_trails)])

B_wins = sum(B_samples > A_samples)

B_wins_percent = B_wins / n_trails

if B_wins_percent > 0.95:
    print("B wins " + str(B_wins_percent) + " of the time")
    print("with a p-value of " + str(round(1- B_wins_percent,3)))

elif B_wins_percent < 0.05:
    print("A wins " + str(1- B_wins_percent) + " of the time")
    print("with a p-value of " + str(round(B_wins_percent,3)))
else:
    print("Results are not statistically significant")
    
    
B_relative = B_samples/A_samples

plt.figure()

B_relative.hist(label = "B/A", bins = 40)

plt.ylabel("Number of occurences", fontsize = 18)
plt.xlabel("B samples / A samples", fontsize = 18)
plt.grid(linewidth = 0.3)
plt.legend()
plt.title("Relative performence B/A")
plt.show()





