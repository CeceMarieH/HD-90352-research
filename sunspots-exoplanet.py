# -*- coding: utf-8 -*-
"""

Created on Fri Jul 17 11:08:00 2020

sunspots.py reads a file and plots the quantities

@author: RPO

"""
import lightkurve as lk

import matplotlib.pyplot as plt

import numpy as np

 

# number of running average data points

r = int(input("Number of running average data points: "))      

 

# Read Data File


# Note two coloms of data, one column for

# time (TJD) and the other for SAP flux.

#

#data = np.loadtxt("C:/Users/prane/Desktop/Research/Old data/Programs/lc1.txt", float, skiprows = 1)      # "a" is now a 2x2 array

tpf = lk.search_targetpixelfile('HD 90352', mission='TESS', sector=10).download(quality_bitmask='default')
mask = tpf.create_threshold_mask(threshold=25)
lc = tpf.to_lightcurve(aperture_mask=mask)
lc = lc.remove_nans().remove_outliers(sigma=6)#.bin(binsize=3)
mask = (lc.time > 1590)
lc = lc[mask]
lc = lc.fold(period = 3.2881, t0 = 1586)

# slice data to obtain time and flux arrays

time, flux = lc.time, lc.flux

N = len(flux)                                 # N: length of arrays



# plot raw values

plt.plot(time,flux, "y") 

 

# Calculate running average starting from the 6th data point

# and averaging from 5 previous points to the 5 following points,

# 11 points total. The size of the array for the running average

# will be smaller by 2*r.

 

runAvg = np.zeros( N - 2*r, float)

for k in range(len(runAvg)):

#    runAvg[k] = np.average(flux[ k: k + 2*r + 1 ])

    for m in range(-r, r+1):

        runAvg[k] = flux[k+m+r] + runAvg[k]

    runAvg[k] = runAvg[k]/(2*r+1)


#save averages as text file
avg = np.zeros((len(runAvg),2), float)
avg[:,0], avg[:,1] = time[r:N-r], runAvg

raw = np.zeros((N,2), float)
raw[:,0], raw[:,1] = time, flux

np.savetxt("C:/Users/prane/Desktop/Research/Programs/lc_avg_r"+str(r)+".csv", avg, delimiter=",", header = "PHASE,FLUX")
#np.savetxt("C:/Users/prane/Desktop/Research/Programs/lc_raw.csv", raw, delimiter=",", header = "PHASE,FLUX")


# plot running value results on same graph

plt.plot(time[r:N-r], runAvg, "r")

plt.show()

# Setup figure

#

plt.title("HD 90352")

plt.xlim(np.min(time), np.max(time))

plt.xlabel("Time (JD)")

plt.ylabel("SAP Flux")

#plt.savefig("sunspots.png")

plt.show()