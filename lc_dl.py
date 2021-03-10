# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:05:12 2020

@author: prane
"""
import lightkurve as lk
#Today we will be using to_lightcurve() to turn tpfs into lcs
#using simple aperture photometry
#sap (oOOOOOH THAT's what that means!)will put an aperture on target
#and sum up flux of all contained pixels

#first lets download our lc from TESS
lc = lk.search_lightcurvefile('HD 90352', mission='TESS', sector=10).download().SAP_FLUX
#now let's make a lightcurve!
lc.plot()
#alternatively,
#lc.errorbar()
# (TTwTT) BEAUTIFULLLL

#clip weird dip at beginning of curve
mask = (lc.time > 1572)
masked_lc = lc[mask]
masked_lc.plot()

#If you wanna remove some outliers
clipped_lc = masked_lc.remove_outliers(sigma=6) #will look more into sigma

'''
#we can combine the flat and masked plots to see the difference

# First define the `matplotlib.pyplot.axes`
ax = flat_lc.scatter()

# Pass that axis to the next plot
clipped_lc.scatter(ax=ax, label='masked')

#...(u^u) Neat.
#BTW, you can use "scatter" instead of "plot" if you want, because scatter plots are handy.
'''

'''
#adding errorbars to a scatter plot
ax = clipped_lc.scatter(s=0.1)
clipped_lc.errorbar(ax=ax, alpha=0.2);  # alpha determines the transparency
'''

folded_lc = clipped_lc.fold(period=3.2881, t0=1586) #arbitrary epoch based on plot
folded_lc.errorbar()

#Binning the data may help. It reduces the number of points and their uncertainty.
binned_lc = folded_lc.bin(binsize=10)  # Average 10 points per bin
binned_lc.errorbar()
#Getting somewhere...
'''
lcinterpol = folded_lc.normalize(unit='ppm').remove_nans().remove_outliers().fill_gaps()
lcinterpol.errorbar()

lcbinterpol = binned_lc.normalize(unit='ppm').remove_nans().remove_outliers().fill_gaps()
lcbinterpol.errorbar()
'''