# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 15:13:39 2021

@author: prane
"""
import numpy as np
import lightkurve as lk
import matplotlib.pyplot as plt

lc = lk.search_lightcurvefile('HD 90352', mission='TESS', sector=10).download().SAP_FLUX
lc = lc.remove_nans().remove_outliers(sigma=6)
mask = (lc.time > 1572)
lc = lc[mask]
time = lc.time
flux = lc.flux
m = lc.quality == 0
with lc.hdu as hdu:
    hdr = hdu[1].header

texp = hdr["FRAMETIM"] * hdr["NUM_FRM"]
texp /= 60.0 * 60.0 * 24.0

ref_time = 0.5 * (np.min(time) + np.max(time))
x = np.ascontiguousarray(time[m] - ref_time, dtype=np.float64)
y = np.ascontiguousarray(1e3 * (flux[m] - 1.0), dtype=np.float64)

plt.plot(x, y, ".k")
plt.xlabel("time [days]")
plt.ylabel("relative flux [ppt]")
_ = plt.xlim(x.min(), x.max())