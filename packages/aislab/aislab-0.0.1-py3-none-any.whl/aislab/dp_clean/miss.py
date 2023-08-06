"""
D A T A   C L E A N N I N G
-----------------------------------------
author: OPEN-MAT
Matlab version:
    Alexander Efremov
    26 Apr 2009
    course: Multivariable Control Systems
-----------------------------------------
"""
import numpy as np
import copy
from sf import *
from md_reg import *
##############################################################################
#def filna(x):
##############################################################################
#def filconst():
##############################################################################
#def filinterp():
##############################################################################
def def filmdl():
    m = x.shape[1]
    ix = np.argwhere(np.isnan(x))
    DV = 1 - np.isnan(x)
    nna = np.sum(np.isnan(x), axis=0)
    mx = np.nanmean(x, axis=0)
    iy = np.argsort(nna)
    for i in iy:
        if nna[i] == 0: continue
        yi = c_(x[:, i])
        xi = np.delete(x, i, axis=1)
        mxi = np.delete(mx, i)
        for j in range(m-1): xi[np.isnan(xi[:,j]),j] = mxi[j] # fill temporary na-s with mean
        iD = DV[:,i]==1
        iV = DV[:,i]==0
        mdl = lspm(xi[iD, :], c_(yi[iD, 0]), pm0=1)
        x[iV, i] = lspm_apl(xi[iV, :], c_(yi[iV, 0]), mdl).flatten()
    return x, ix

##############################################################################


