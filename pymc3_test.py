# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:17:23 2021

@author: prane
"""

import numpy as np

import matplotlib.pyplot as plt

 

np.random.seed(42)

 

true_m = 0.5

true_b = -1.3

true_logs = np.log(0.3)

 

x = np.sort(np.random.uniform(0, 5, 50))

y = true_b + true_m * x + np.exp(true_logs) * np.random.randn(len(x))

 

plt.plot(x, y, ".k")

plt.ylim(-2, 2)

plt.xlabel("x")

plt.ylabel("y")

 

import pymc3 as pm

 

with pm.Model() as model:

 

    # Define the priors on each parameter:

    m = pm.Uniform("m", lower=-5, upper=5)

    b = pm.Uniform("b", lower=-5, upper=5)

    logs = pm.Uniform("logs", lower=-5, upper=5)

 

    # Define the likelihood. A few comments:

    #  1. For mathematical operations like "exp", you can't use

    #     numpy. Instead, use the mathematical operations defined

    #     in "pm.math".

    #  2. To condition on data, you use the "observed" keyword

    #     argument to any distribution. In this case, we want to

    #     use the "Normal" distribution (look up the docs for

    #     this).

    pm.Normal("obs", mu=m * x + b, sd=pm.math.exp(logs), observed=y)

 

    # This is how you will sample the model. Take a look at the

    # docs to see that other parameters that are available.

    trace = pm.sample(draws=1000, tune=1000, chains=1, cores=1)
    #does not work with chains=2 but DOES work with chains=1

   

    

_ = pm.traceplot(trace, var_names=["m", "b", "logs"])

with model:

    pm.summary(trace, var_names=["m", "b", "logs"])

 

import corner  # https://corner.readthedocs.io

 

samples = pm.trace_to_dataframe(trace, varnames=["m", "b", "logs"])

_ = corner.corner(samples, truths=[true_m, true_b, true_logs])