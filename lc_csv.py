# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 10:32:56 2020

@author: prane

In this program we will figure out how to save a lightcurve as a csv file
"""
import lightkurve as lk

#download tpf and convert to lightcurve; remove outliers
tpf = lk.search_targetpixelfile('HD 90352', mission='TESS', sector=10).download(quality_bitmask='default')
mask = tpf.create_threshold_mask(threshold=25)
lc = tpf.to_lightcurve(aperture_mask=mask)
lc = lc.remove_nans().remove_outliers(sigma=6)
lc.scatter()

normal = lc.normalize()
normal.scatter()

#how to use lc.to_csv??
#lc.to_csv(path_or_buf="lc_csv.csv") #saved to C:/Users/prane
#how to save to designated directory?
#lc.to_csv(path_or_buf="C:\Users\prane\OneDrive\Desktop\Research\Programs\csv\lc_csv.csv")
#returns unicode error; can't read backslash?
#lc.to_csv(path_or_buf="C:/Users/prane/OneDrive/Desktop/Research/Programs/csv/lc_csv.csv")
#aHA! Forward slashes it is - curse you, 1980s computer codes!!
#It's so beautiful TTwTT ...I think I've used that before but I do what I want