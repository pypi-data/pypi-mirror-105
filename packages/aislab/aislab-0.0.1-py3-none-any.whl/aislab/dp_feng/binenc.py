import numpy as np
from numpy.matlib import repmat
import copy

from sf import *

###################################################################################
def b2dv(bins, x, xtp):
    if xtp == 'nom' or xtp == 'ord':
        dv = np.zeros(x.shape,dtype=int)
        for k in range(len(bins['lb'])):
            if bins['type'] == 'Missing':           dv1 = np.isnan(x)
            elif bins['type'] == 'Other':           dv1 = np.zeros(x.size)
            elif bins['type'] == 'Special Value':   dv1 = x == bins['lb']
            else:                                   dv1 = x == bins['lb'][k]
            dv = dv + dv1
    else:
        if bins['type'] == 'Missing':               dv = np.isnan(x)
        elif bins['type'] == 'Other':               dv = np.full(x.shape, False)
        elif bins['type'] == 'Special Value':       dv = x == bins['lb']
        elif bins['lb'] == bins['rb']:              dv = x == bins['lb']
        else:                                       dv = (x >= bins['lb']) & (x < bins['rb'])
    dv = np.array(dv, dtype=bool)
    return dv
###################################################################################
def best_merge(bns, s):
    bns2 = copy.deepcopy(bns)
    md = len(s)
    i1 = 1
    i2 = 1
    j = 0
    for si in s:
        i2 += si
        if i2 - i1 > 1:
            for i3 in range(i1, i2-1): 
                bns2 = mrgbns(bns2, i1)
        j += 1
        i1 = i2
        i1 -= si - 1
        i2 -= si - 1
    return bns2
###################################################################################
def binMOS(bns, x, w, sv, xtp):
    ii = np.where(np.isnan(x))
    if not ii == 0:
        bns[len(bns)+1] = setbin(np.nan, w[0:len(ii[0]):1].tolist(), xtp, 'Missing')
    else:
        bns[len(bns)+1] = setbin(np.nan, [0], xtp, 'Missing')
        bns[len(bns)]['n'] = 0
    bns[len(bns)+1] = setbin([], [], xtp, 'Other')
    for j in range(len(sv)):
        ii = np.where(x == sv[j])
        if not ii == 0:
            bns[len(bns)+1] = setbin(sv[j], w[0:len(ii[0]):1].tolist(), xtp, 'Special Value')
        else:
            bns[len(bns)+1] = setbin(sv[j], [0], xtp, 'Special Value')
    return bns
###################################################################################
def stbnsy(bns, x, y, w, par):
    ytp = par['ytp']
    xtp = par['xtp']
    if 'yi' in par: yi = par['yi']
    else:           yi = []
    for h in range(1,len(bns)+1):
        dv = b2dv(bns[h], x, xtp)
        bns[h]['y'] = {}
        bns[h]['y2'] = {}
        bns[h]['nw'] = {} #!
        bns[h]['my'] = {}
        bns[h]['woe'] = {}
        bns[h] = binst(bns[h], dv[:,0], y, w, ytp, yi)
    return bns
###################################################################################
def bns2arr(bns):
    # r = len(bns[1]['y'])
    m = len(bns)
    Luy = 0
    for i in bns[1]['y']:
        Luy = Luy + len(bns[1]['y'][i])
    syy = np.zeros([m, Luy])
    syy2 = np.zeros([m, Luy])
    wy = np.zeros([1, Luy])
    nw = nans((m, 1))
    for i in range(len(bns)): nw[i] = bns[i+1]['nw']
    n = nans((m, 1))
    for i in range(len(bns)): n[i] = bns[i+1]['n']
    for i in range(m):
        k = []
        k2 = []
        for j in bns[i+1]['y']:
            k = np.append(k, bns[i+1]['y'][j])
            k2 = np.append(k2, bns[i+1]['y2'][j])
        syy[i] = k
        syy2[i] = k2
    j = [-1]
    wy = []
    for i in bns[1]['y']:
        luy = len(bns[1]['y'][i])
        # j = np.arange(j[len(j)-1] + 1 ,j[len(j)-1]+1+luy)
        wy = np.append(wy, repmat(1/luy, 1, luy))
    return n, nw, syy, syy2, wy
###################################################################################
def binst(bins, dv, y, w, ytp, yi):
    wh = w[:,0][dv]
    if wh.any:
        bins['n'] = len(wh)
        bins['nw'] = float(sum(wh))
    else:
        bins['n'] = 0
        bins['nw'] = 0.
    b = {}
    b2 = {}
    for i in range(len(ytp)):
        yh = y[:,i][dv]
        if ytp[i] == 'nom' or ytp[i] == 'ord':
            if yi != []:
                yii = yi[i]
            else:
                yii = np.unique(y[~np.isnan(y[:,i]), i])
            c = []
            for j in range(len(yii)):
                jj = list(yh == yii[j])
                if jj != []:
                    c.append(sum(wh[jj]))
                else:
                    c.append(0)
            bins['y'][i+1] = c
            bins['y2'][i+1] = c
            bins['my'][i+1] = []
            bins['woe'][i+1] = []
        else:
            if len(dv) != 0:
#                yh = list(y[:, i][dv])
#                wh = w[:,0][dv]
                b[i+1] = [np.sum(wh*yh)]
                b2[i+1] = [sum(wh*yh*yh)]
            else:
                b[i+1] = [0]
                b2[i+1] = [0]
            bins['y'] = b
            bins['y2'] = b2
            bins['my'][i+1] = b[i+1][0]/max(bins['nw'], 1e-12)
            bins['woe'][i+1] = []
    return bins
###################################################################################
def cnd_gbi(gg, ngg, dGBInd, tolmindGBInd, Dind):
    GBI = gbi(gg, ngg)
    GBI1 = GBI + 200*(GBI < 0)
    dGBI = diff(GBI1)
    #sdGBI = np.sort(dGBI)
    cnd_GBI = np.min(abs(dGBI), axis=0) >= dGBInd - tolmindGBInd*Dind
    return cnd_GBI
###################################################################################
def cnd_trnd(ns, gg, nn, md, mt):
    if mt is not np.nan:
        my = gg/nn
        my[my<1e-3] = 1e-3
        dmy = diff(my)
        trnd = (np.sum(dmy > 0, axis=0) == md - 1)*1 - (np.sum(dmy < 0, axis=0) == md - 1)*1
        if mt == 0: cnd_TRND = abs(trnd) == 1
        else:       cnd_TRND = trnd == mt
    else:
        cnd_TRND = np.ones(ns, dtype = bool)
    return cnd_TRND
###################################################################################
# def enc():
#   encoding
#   - met = woe, mdep, ...
###################################################################################
def enc_int(x, order=None):
    if order is None: order = np.unique(x)
    i = 1
    xe = copy.deepcopy(x)
    for xi in order:
        xe[x.flatten()==xi,0] = i
        i += 1
    return xe
###################################################################################
def enc_apl(bns, x, par):
    xtp = par['xtp']
    met = par['met_enc']
    N = x.shape[0]
    if met == 'dv': m = len(bns)
    else:           m = 1
    xe = nans((N, m))
    for h in range(1,len(bns)+1):
        dv = b2dv(bns[h], x, xtp)
        if met == 'my':     xe[dv] = bns[h]['my'][1]
        elif  met == 'woe': xe[dv] = bns[h]['woe'][1]
        elif met == 'dv':   xe[:,h-1] = dv.flatten()
    return xe
###################################################################################
def inv_distr(DistrType, pval, df1, df2, x1, x2, tol):
    ITMAX = 100; EPS = 3.0e-7
    a = x1; b = x2; c = x2; d = 0; e = 0
    cnd = DistrType == 'Fisher'
    if cnd:
        fa = betai(df1, df2, a)[0] - pval
        fb = betai(df1, df2, b)[0] - pval
    else:
        fa = gamq(df2, a)[0] - pval
        fb = gamq(df2, b)[0] - pval
    if fa > 0 and fb > 0 or fa < 0 and fb < 0:
        print('Root must be bracketed in inverse_distr')
        return None
    fc = fb
    it_num = range(0, ITMAX)
    for i in it_num:
        if fb > 0 and fc > 0 or fb < 0 and fc < 0:
            c = a; fc = fa; e = b - a; d = e
        if abs(fc) < abs(fb):
            a = b;  b = c;  c = a;  fa = fb;  fb = fc;  fc = fa
        tol1 = 2*EPS*abs(b) + 0.5*tol
        xm = 0.5*(c - b)
        cnd1 = abs(b) < 1e-10
        if abs(xm) <= tol1 or fb == 0:
            return int(cnd)*(cnd1*1e10 + int(not cnd1)*(1/b - 1)*df1/df2) + int(not cnd)*2*b
        if abs(e) >= tol1 and abs(fa) > abs(fb):
            s = fb/fa
            if a == c:
                p = 2*xm*s
                q = 1 - s
            else:
                q = fa/fc;  r = fb/fc
                p = s*(2*xm*q*(q - r) - (b - a)*(r - 1))
                q = (q - 1)*(r - 1)*(s - 1)
            if p > 0:
                q = -q
            p = abs(p)
            min1 = 3*xm*q - abs(tol1*q)
            min2 = abs(e*q)
            cnd2 = min1 < min2
            if 2*p < (cnd2*min1 + int(not cnd2)*min2):
                e = d;  d = p/q
            else:
                d = xm; e = d
        else:
            d = xm; e = d
        a = b
        fa = fb
        if abs(d) > tol1:
            b = b + d
        else:
            prod = xm*tol1
            if prod == 0:
                sgn = 1
            else:
                sgn = np.sign(prod)
            b = b + sgn*abs(tol1)
        if cnd:
            fb = betai(df1, df2, b)[0] - pval
        else:
            fb = gamq(df2, b)[0] - pval
    cnd1 = abs(b) < 1e-10
    return cnd*(cnd1*1e10 + int(not cnd1)*(1/b - 1)*df1/df2) + int(not cnd)*2*b
###################################################################################
def mdep(syy, nw, wy, w=[]):
    nw[nw < 1e-6] = 1e-6
    if syy.ndim == 1: m = 1; [Luy] = syy.shape
    else:             [m, Luy] = syy.shape
    my = syy*(1/repmat(nw, 1, Luy));
    mmy = my.max(axis=0)
    if not isinstance(mmy, np.ndarray): mmy = np.array([[mmy]])
    mmy[mmy < 1e-6] = 1e-6 # !!! works for ytp = 'bin'
    if len(w) == 0: w = r_(wy/mmy)
    ww = repmat(w, m, 1)
    x = my*ww
    if not isinstance(w, np.ndarray): w = np.array([[w]])
    return x, w
###################################################################################
def minobs(bns, nd):
    i = 0
    while i < len(bns) - 1:
        i = i + 1
        if bns[i]['nw'] < nd:
            bns = mrgbns(bns, i)
            i = i - 1
    if len(bns) <= 1:
        return bns
    if bns[len(bns)]['nw'] < nd:
        bns = mrgbns(bns, len(bns) - 1)
    return bns
###################################################################################
def mrgbns(bns, i, j=np.nan):
    if np.isnan(j): j = i + 1
    if type(bns[i]['lb']) is list:
        if len(bns[i]['lb']) == 0:  bns[i]['lb'] = bns[j]['lb']
        else:                       bns[i]['lb'] = num2lst(np.unique(np.append(bns[i]['lb'], bns[j]['lb'])))
    elif isnum(bns[i]['lb']):       bns[i]['rb'] = bns[j]['rb']
    else: print('ERROR: Unknown type of x in mrgbns()...') # todo: make this error
    bns[i]['nw'] = bns[i]['nw'] + bns[j]['nw']
    bns[i]['n'] = bns[i]['n'] + bns[j]['n']
    if 'y' in bns[i].keys(): 
        for h in range(len(bns[i]['y'])): bns[i]['y'][h+1] = sumls(bns[i]['y'][h+1], bns[j]['y'][h+1])
        for h in range(len(bns[i]['y2'])): bns[i]['y2'][h+1] = sumls(bns[i]['y2'][h+1], bns[j]['y2'][h+1])
    cnd_i = bns[i]['type'] == 'Other' or bns[i]['type'] == 'Missing' or bns[i]['type'] == 'Special Value'
    cnd_i1 = bns[j]['type'] == 'Other' or bns[j]['type'] == 'Missing' or bns[j]['type'] == 'Special Value'
    if cnd_i and cnd_i1:  bns[i]['type'] = 'Mixed OMS'
    else:                 bns[i]['type'] = 'Normal'
    for k, l in zip(range(j,len(bns)), range(j+1,len(bns)+1)): bns[k] = bns[l]
    del bns[len(bns)]
    return bns
###################################################################################
def nabub(x, w, sv, xtp, ux):
    x = x[~np.isnan(x)]
    if not ux:   ux = np.unique(x)
    for i in sv: ux = list(filter(lambda a: a != i, ux))
    nu = len(ux)
    if nu == 0: bns = []
    cnt = 0
    bns = {}
    bns[nu] = setbin([0], [0], xtp, 'Normal')
    for i in range(nu):
        xi = ux[i]
        cnt = cnt + 1;
        bns[cnt] = setbin(xi, w[:len(x)][x == ux[i]], xtp, 'Normal')
    if cnt == 0: bns = {}
    return bns
###################################################################################
def passChi2(df, df_den, bm12, pt, ytp, ba):
    tol = 1e-3
    df2 = df/2
    df_den2 = df_den/2
    if ytp[0] == 'bin':
        if ba: apt = pt/bm12
        else:  apt = pt
        left = 0
        right = -4*df2*np.log(apt)
        dummy = 1;
        if apt < 1e-200: chi_pass = right
        else:            chi_pass = inv_distr('Chi2', apt, dummy, df2, left, right, tol)
    else:
        left = 0
        right = 1
        chi_pass = inv_distr('Fisher', pt, df_den2, df2, left, right, tol)
    return chi_pass
###################################################################################
def permints(n, m, init=True):
    s = np.array([])
    p = n - m + 1
    if m == 2:
        bng = np.arange(0, p).reshape((p, 1))
        bng_new = np.arange(p-1, -1, -1).reshape((p,1))
        s = np.hstack((bng, bng_new))
    if m > 2:
        i_iter = np.arange(0, p)
        for i in i_iter:
            bng  = permints(m-1+i, m-1, False)
            bng_new = np.tile(p-1-i, bng.shape[0]).reshape((bng.shape[0],1))
            if s.shape[0] == 0: s = np.hstack((bng, bng_new))
            else:               s = np.vstack((s, np.hstack((bng, bng_new))))
    if init and s.shape[0] != 0: s += 1
    return s
###################################################################################
def reduce_bns1(bns, xtp, g, b, nw, gd, bd):
    order_nom = lambda g, nw: g / max(1, nw)
    cnd_mrg = lambda g, b, nw, gd, bd, p1: g < gd and g*p1 < 1 or b < bd and b*p1 < 1 # merge condition 
    bng = copy.deepcopy(bns)
    if xtp == 'nom':
        bns = sort_bins(config, bns, order_nom, BUS_groups)
    try:
        pg = b.sum()/nw.sum()
        p1 = min([pg, 1 - pg])
    except: print('Error: Binning stats are wrong...') # todo: make it real error
    keep_bin = 1
    while keep_bin < len(bns)-1:
        gi = bns[keep_bin]['y'][1][0]
        nwi = bns[keep_bin]['nw']
        bi = nwi - gi
        drop_bin = keep_bin + 1
        bin_type_drop = bns[drop_bin]['type']
        if bin_type_drop == 'Missing':
            drop_bin = keep_bin - 1
            bin_type_drop = bng[drop_bin]['type']
        if bin_type_drop != 'Missing' and cnd_mrg(gi, bi, nwi, gd, bd, p1):
            if keep_bin < drop_bin: bns = mrgbns(bns, keep_bin, drop_bin)
            else:                   bns = mrgbns(bns, drop_bin, keep_bin)
        else:
            keep_bin += 1
    return bng
###################################################################################
def reduce_bns2(bns, ytp, md, mar):
    lpm = np.log(1e4)
    kk = np.arange(md + 2, 1e5 + 1)
    kkk = ((kk - 1)*np.log(kk - 1) - (kk - md)*np.log(kk - md) - (md - 1)*np.log(md - 1))[::-1]
    ind = np.arange(len(kkk))[::-1]
    mmax = ind[kkk < lpm].max() + md + 2 + 1

    m = len(bns)
    s = np.ones((m, 1))
    while m > mmax:
        if ytp[0] == 'bin':
            [__, nw, sy, __, __] = bns2arr(bns)
            y1 = sy[:-1]
            y2 = sy[1:]
            n1 = nw[:-1]
            n2 = nw[1:]

            cnd = list((n1 == 0) & (n2 == 0))
            if any(cnd):
                cnt_max = cnd.index(True)
            else:
                dC = (y1 + y2)**2/(n1 + n2) - y1**2/n1 - y2**2/n2
                dC[dC > 0] = 0
                cnd = n1 + n2 <= mar
                isc = np.arange(1, len(cnd) + 1)[cnd.flatten()]
                __, idCm = max1(dC[cnd])
                cnt_max = isc[idCm]
        else: # if ytp != 'bin'
            print('Error, dependant is not binary!')
#            m_1 = m - 1
#            dCritm = -1.0000e+10
#            G2 = g2.sum(); Nw = nw.sum()
#            sums = (g**2/nw).sum()
#            a = g.sum()**2/Nw**2
#            b = (Nw**2 - m_1 + 1)/m_1*G2/(G2 + a - sums)
#            dC = (y1 + y2)**2/(n1 + n2) - y1**2/n1 - y2**2/n2 # after merge - before merge
#            dCrit = (Nw - m_1)/(m_1 - 1)*G2/(G2 + a - sums - dC) - b
#            cnd = (dCrit > dCritm) & (n1 + n2 <= config['parameters']['cc_mar'])
#            if cnd.any():
#                isc = np.arange(len(cnd))[cnd]
#                idCm = np.argmax(dC[cnd])
#                cnt_max = isc[idCm]
#            else:
#                cnt_max = np.argmin(abs(dC))
#                if cnt_max == len(nw) - 1:
#                    cnt_max -= 1
        bns = mrgbns(bns, cnt_max)
        s[cnt_max-1] += s[cnt_max]
        s = np.delete(s, cnt_max)
        m = len(bns)
    [__, nw, sy, __, __] = bns2arr(bns)
    s = np.array(s, dtype = int)
    return bns, s, sy, nw
###################################################################################
def sbng(bns, par):
    bns1 = copy.deepcopy(bns)
    del bns
    bns = bns1
    xtp = par['xtp']
    ytp = par['ytp']
    met = par['met']
    skip_mos = par['skip_mos']
    k = 1
    bns_1 = {}
    for i in range(len(bns), 0, -1):
        try:
            if 'Missing' in bns[i]['type'] and 'm' in skip_mos:
                bns_1[k] = bns[i]
                k = k + 1
                bns = {key:val for key, val in bns.items() if key != i}
        except: 
            pass
        try:
            if 'Other' in bns[i]['type'] and 'o' in skip_mos:
                bns_1[k] = bns[i]
                k = k + 1
                bns = {key:val for key, val in bns.items() if key != i}
        except: 
            pass
        try:
            if 'Special Value' in bns[i]['type'] and 'sv' in skip_mos:
                bns_1[k] = bns[i]
                k = k + 1
                bns = {key:val for key, val in bns.items() if key != i}
        except: 
            pass
        
    if 'nom' in xtp:
        [n, nw, syy, syy2, wy] = bns2arr(bns)
        [x, w] = mdep(syy, nw, wy)
        ix = (x @ w.T).argsort(axis=0) + 1
        bins = {}
        for i in range(len(ix)): bins[i+1] = bns[ix.flatten()[i]]
        bns = bins
        xtp = 'ord'
    
    if met == 'hclust':
        md = par['md']
        met_dist = par['met_dist']
        [bns, D] = spih_sb_hclust(bns, xtp, md, met_dist)
    elif met == 'co1y':
        md = par['md']
        gd = par['nmin_uy'][0]
        bd = par['nmin_uy'][1]
        mar = par['mar']
        skip_mos = par['skip_mos']
        pt = par['pt']
        ba = par['ba']
        maxprm = par['maxprm']
        dGBInd = par['dGBInd']
        tolmindGBInd = par['tolmindGBInd']
        mt = par['mt']
        minB = par['minB']
        tolminB = par['tolminB']
        [bns, D] = spih_sb_co1y(bns, xtp, ytp, md, gd, bd, mar, pt, ba, dGBInd, tolmindGBInd, mt, minB, tolminB)

    if bns is None: return bns, D
    else:
        for i in range(len(bns_1)): bns[len(bns)+1] = bns_1[i+1]

    return bns, D
###################################################################################
def setbin(x, w, xtp, btp):
    bn={}
    if 'num' in xtp:
        if np.any(np.isnan(x)):
            bn['lb'] = [np.nan]
            bn['rb'] = [np.nan]
        else: 
            if (isinstance(x, np.ndarray) or isinstance(x, list)) and len(x) == 0:
                bn['lb'] = []
                bn['rb'] = []
            else:
                bn['lb'] = np.min(x)
                bn['rb'] = np.max(x)
    else:
        if ~np.any(np.isnan(x)):
            bn['lb'] = np.transpose(np.unique(x)[:,None])
            bn['lb'] = bn['lb'][0].tolist()
        else:
            bn['lb'] = [np.nan]
        bn['rb'] = []
    bn['nw'] = np.sum(w)
    bn['n'] = len(w)
    bn['type'] = btp
    if bn['n'] == 1 and not bn['lb']:
        bn['n'] = 0
    return bn
###################################################################################
def sort_bins(vname, config, unordered_bins, bin_order_function):

    sorting_criteria = []
    ranking_criteria = []
    for bn in unordered_bins:

        if bn[-1]['type'] != 'missing':
            sorting_criteria.append( bin_order_function(bn[-1]['statistics']) )
        elif bn[-1]['type'] == 'missing' and unordered_bins[-1][-1]['statistics']['number_of_records'] >= config['parameters']['fc_mir']:
            pass
        else:
            # Do not use the missings not statistically significant number of NaNs 
            if 'Use_NA' in config['variables'][vname]:
                config['variables'][vname].pop('Use_NA')

    sorting_order = np.argsort(sorting_criteria)

    ordered_bins = []
    for s in sorting_order:
        ordered_bins.append(unordered_bins[s])
    ordered_bins.append(unordered_bins[-1])

    return ordered_bins
###################################################################################
def spih(bns, xtp, md, nd, met):
    Nw = 0
    for k in bns:
        Nw = Nw + bns[k]['nw'] 
    m = len(bns)
    Nd = Nw/md
    i = 0
    iold = 1
    s = 0
    while m >= i + 2:
        s = s + 1
        i = i + 1
        if xtp == 'num' or xtp == 'ord':
            ni2 = bns[i]['nw'] + bns[i + 1]['nw']
            if ni2 <= Nd or bns[i]['nw'] <= nd:
                bns = mrgbns(bns, i)
                i = i - 1
            else:
                d_aft = ni2 - Nd
                d_bef = Nd - bns[i]['nw']
                if d_bef > d_aft:
                    bns = mrgbns(bns, i)
        else:
            c = []
            for k in range(len(bns) - i): c.append(bns[i+k+1]['nw'])
            ni2 = bns[i]['nw'] + c
            imrg = find((ni2 <= Nd) | (bns[i]['nw'] <= nd)) + i + 1
            if any(imrg):
                leng = len(imrg)
                jj = range(0, leng)
                r = rand(l=0, h=leng-1, tp='int', seed=s)
                bns = mrgbns(bns, i, imrg[jj[r[0,0]]])
                i = i - 1
            else:
                r = rand(l=0, h=len(ni2)-1, tp='int', seed=s)
                d_aft = ni2[r] - Nd
                d_bef = Nd - bns[i]['nw']
                if d_bef > d_aft:
                    bns = mrgbns(bns, i, r[0,0] + 1)
        m = len(bns)
        if met == 'enr' and iold < i:
            sm = 0
            for k in range(1,i+1): sm = sm + bns[k]['nw'] 
            iold = i
            if md == i and m <= md: break
    
    while m > md:
        if xtp == 'num' or xtp == 'ord':
            ni2 = []
            for k, l in zip(range(1,len(bns)), range(2,len(bns)+1)):
                ni2.append([bns[k]['nw'] + bns[l]['nw']])
            i = np.argmin(ni2) + 1
            bns = mrgbns(bns, i)
        else:
            c = []
            for k in range(len(bns)): c.append(bns[k+1]['nw'])
            ni2 = np.kron(np.ones((m,1)), c) + np.kron(np.ones((m,1)), c).T
            np.fill_diagonal(ni2, float('inf'))
            ij = np.argmin(ni2) + 1
            [i, j] = ind2sub(np.array([m, m]), ij)
            bns = mrgbns(bns, min(np.array([i, j])), max(np.array([i, j])))
        m = len(bns)
    if bns[len(bns)]['nw'] < nd:
        if xtp == 'num' or xtp == 'ord':
            bns = mrgbns(bns, m - 1)
        else:
            c = []
            for k in range(len(bns)): c.append(bns[k]['nw'])
            ni2 = bns[len(bns)]['nw'] + c
            i = np.argmin(ni2) + 1
            bns = mrgbns(bns, i, m)
    return bns
###################################################################################
def spih_erv(x, w, xtp, md, sv):
    ir = [np.isnan(x)]
    for k in range(len(sv)):
        for l in range(len(ir[0])):
            ir[0][l] = ir[0][l] or x[l] == sv[k]
    x = x[~ir[0]]
    xmin = min(x)
    xmax = max(x)
    s = (xmax - xmin)/md
    b = np.arange(xmin,xmax+s,s)
    b = np.round(b,4)
    lb = b[0:len(b)-1]
    rb = b[1:len(b)-1]
    rb = np.append(rb,float('inf'))
    bns = {}
    for k in range(int(md)):
        bns[k+1] = setbin([], [], xtp, 'Normal')
    for k in range(int(md)):
        ii = []
        for l in range(len(x)):
            ii.append(x[l] >= lb[k] and x[l] < rb[k])
        bns[k+1] = setbin(x[ii].tolist(), w[0:len(ii):1][ii].tolist(), xtp, 'Normal')
        bns[k+1]['lb'] = [lb[k]]
        bns[k+1]['rb'] = [rb[k]]
    return bns
###################################################################################
def spih_sb_co1y(bns, xtp, ytp, md, gd, bd, mar, pt, ba, dGBInd, tolmindGBInd, mt, minB, tolminB):
    [n, nw, syy, syy2, wy] = bns2arr(bns)
    number_of_records = nw
    g = syy
    b = nw - syy
    if len(ytp) == 1 and ytp[0] == 'bin':
        Dind = dind(g, b)
        bns = reduce_bns1(bns, xtp, g, b, nw, gd, bd)
    else:
        pass # Not implemented for non-binary dependant

    bin_set_quality = {}
    bin_selection_stack = {}
    gbi_delta = {}
    mm = range(2, min([len(bns), md]) + 1) # number of bins to try
    viable_binnings = []
    binning_quality = []
    fb_to_rfb_steps = {}
    gbi_delta_of_viable_binnings = []
    bin_set_quality = None
    bin_selection_stack = None
    gbi_delta = None

#    loop_time = time.time()
    crit_b = nans((md - 1,))
    bns_b = [None]*(md - 1)
    br = 0
    for md in mm:
        bns1 = copy.deepcopy(bns)
        bns1, s1, g, nw = reduce_bns2(bns1, ytp, md, mar)
        m = len(bns1)
        if ba: pass # [bm1, bm2] = bonfadj(mp, k, md, xtp)
        else:  bm1 = bm2 = 1
        Nw = sum(nw)
        df = md - 1
        df_den = Nw - md
        Chi2pass = passChi2(df, df_den, bm1*bm2, pt, ytp, ba)
        s2 = permints(m, md) # s2 - set of all merges to be investigated
        if s2.shape[0] != 0:
            gg, nn = stbngs(s2, g, nw)
            ngg = nn - gg
            if ytp[0] == 'bin':
                Chi2 = chi2(gg, ngg)
            else:
                sys.exit('ERROR: Supervised binning for non-binary dependants is not implemented...')
                # note: Chi2 -> Crit = fratio(gi, gi2, nwi, md, ssy, ytp)
            if ytp[0] == 'bin': cnd_GBI = cnd_gbi(gg, ngg, dGBInd, tolmindGBInd, Dind)
            else:               pass # not implemented

            cnd_TRND = cnd_trnd(s2.shape[0], gg, nn, md, mt)
            cnd_pt = Chi2 >= Chi2pass
            cnd_minB = np.min(ngg, axis=0) >= minB - tolminB*Dind
            cnd_mar = np.max(nn, axis=0) <= mar
            cnd = cnd_GBI & cnd_TRND & cnd_pt & cnd_minB & cnd_mar
            if cnd.any():
                ib = np.arange(len(cnd))[cnd.flatten()]
                crit_b[br], ic = max1(Chi2[cnd.flatten()])
                ind = ib[ic]
                bns_b[br] = best_merge(bns1, s2[ind,])
            else:
                crit_b[br] = np.nan
                bns_b[br] = None
        else:
            crit_b[br] = np.nan
            bns_b[br] = None
        br += 1
    if np.any(np.isnan(crit_b) == False):
        crit_b, ind = max1(crit_b, naskip=True)
        bns_b = bns_b[ind]
    else: 
        bns_b = None
        crit_b = np.nan
#    print('sb: ', round((time.time() - loop_time), 3), 'sec')
    return bns_b, crit_b
###################################################################################
def spih_sb_hclust(bns, xtp, md, met_dist):
    m = len(bns)
    [n, nw, syy, __, wy]  = bns2arr(bns)
    [x, w] = mdep(syy, nw, wy)
    [D, ind] = dist1(x, w, met_dist, xtp)
    ind1 = num2lst(np.arange(m))
    
    interate = md < m
    x1 = x
    while interate:
        if D.size == 0: ii = [];
        ii = np.argmin(D)
        ind1[min(ind[ii, :])] = [ind1[i] for i in ind[ii, :]]
        del ind1[max(ind[ii, :])]
        bns = mrgbns(bns, min(ind[ii, :])+1)
        ia = min(ind[ii, :])
        syy[ia, :] = sum(syy[ind[ii, :], :])
        nw[ia] = sum(nw[ind[ii, :]])
        syy = np.delete(syy, max(ind[ii, :]), axis=0)
        nw = np.delete(nw, max(ind[ii, :]), axis=0)
        if syy[ia, :].ndim == 1: [xnew] = mdep(syy[ia, :], nw[ia], wy, w=w)[0]
        else:                    [xnew] = mdep(np.sum(syy[ia, :],1), np.sum(nw[ia]), wy, w)[0]
        x1[ia, :] = xnew
        x1 = np.delete(x1, max(ind[ii, :]), axis=0)
        if ii > 0:     [D[ii - 1]] = dist1(x1[[ia,ia - 1], :], w, met_dist, xtp)[0]
        if ii < m - 2: [D[ii + 1]] = dist1(x1[[ia,ia + 1], :], w, met_dist, xtp)[0]
        D = np.delete(D, ii, axis=0)
        m = m - 1
        if m == md: interate = 0
    return bns, D
###################################################################################
def stbng(met, bns, par, x=np.empty((0,0)), y=np.empty((0,0)), w=np.empty((0,0))):
    if bns is None: return None, None
    if met == 'ub': bns = stbnsy(bns, x, y, w, par)
    ytp = par['ytp']
   
    st = {}
    if bns == {}: s = []; return st
    r = len(ytp)
    m = len(bns)
    Nw = 0
    for i in range(1, m+1): Nw = Nw + bns[i]['nw']
#    for i in range(1,len(bns)+1): print(bns[i]['nw'])
    for i in range(r):
        ytpi = ytp[i]
        nw = []
        for j in range(1, m+1): nw.append(bns[j]['nw'])
        nw = np.array(nw)
        nw = nw.reshape(nw.shape[0], 1)
        n = []
        for j in range(1, m+1): n.append(bns[j]['n'])
        sy = []
        sy2 = []
        for h in range(m):
            a = []
            a2 = []
            for k in bns[h+1]['y'][i+1]:  a.append(k)
            for k in bns[h+1]['y2'][i+1]: a2.append(k)
            sy.append(a)
            sy2.append(a2)
        sy = np.array(sy)
        sy2 = np.array(sy2)
        Sy = sy.sum(axis=0)
        s = {}
        if ytpi == 'bin': 
            s['sy'] = sy
            syb = np.array(nw - sy)
            s['syb'] = syb
            s['pnw'] = nw/Nw*100
            s['py0'] = np.dot(sy, np.linalg.pinv(Sy[np.newaxis]))*100
            s['py1'] = np.dot(syb, np.linalg.pinv([Nw - Sy]))*100
            s['cp0'] = np.cumsum(s['py0'])
            s['cp1'] = np.cumsum(s['py1'])
            nw1 = nw
            nw1[nw<1e-12] = 1e-12
            s['my0'] = np.array(syb/nw1)
            s['my1'] = np.array(sy/nw1)
            s['gbind'] = gbi(sy, syb)
            syb1 = syb
            syb1[syb<1e-12] = 1e-12

            s['odds'] = sy/syb
            s['Gini'] = gini(sy, syb)
            #s['WoE'] = woe(sy, syb)
            s['KS'] = ks(sy, syb)
            s['Vin'] = vinf(sy, syb) 
            s['D'] = dind(sy, syb)
            if m == 2: s['twoing'] = twng(sy, syb)
            s['Chi2'] = chi2(sy, syb)
        elif ytpi == 'num':
            s['sy'] = sy
            s['pnw'] = nw/Nw*100
            s['Frat'] = frat(sy, sy2, nw)
        else:
            s = []
        st[i] = s
        # for i in range(m): 
        #     if 'WoE' in s:  bns[i+1]['woe'] = s['WoE'][i]
        #     else:           bns[i+1]['woe'] = None
        #     if 'my' in s:   bns[i+1]['my'] = s['my1'][i]
        #     else:           bns[i+1]['my'] = None

    return st, bns
###################################################################################
def stbngs(s, sy, nw):
    Np, md = s.shape
    SY = nans((md, Np))
    NW = nans((md, Np))
    for i in range(0, Np):
        i1 = 0
        i2 = 0
        j = 0
        for si in s[i]:
            i2 += si
            if i2 - i1 == 1:
                SY[j, i] = sy[i1, 0]
                NW[j, i] = nw[i1, 0]
            else:
                SY[j, i] = sy[i1:i2, 0].sum(0)
                NW[j, i] = nw[i1:i2, 0].sum(0)
            j += 1
            i1 = i2
    return SY, NW
###################################################################################
def ubng(x, w, par):
    sv = par['sv']
    xtp = par['xtp']
    if 'xi_order' in locals(): xi_order = par['xi_order']
    else:                      xi_order = []
    met = par['met']
    if 'md' in par and met == 'enr' or met == 'erv': md = par['md']
    if 'pd' in par and met == 'epp':                 md = 100/par['pd']
    nmin = par['nmin']
    N = len(x)
    if met == 'enr' or met == 'epp' or met == 'svc':
        bns = nabub(x, w, sv, xtp, xi_order)
        if not met == 'svc':
            if len(bns) > md: bns = spih(bns, xtp, md, nmin, met)
            bns = minobs(bns, nmin)
    elif met == 'erv':
        if xtp == 'nom':
            bns = {}
            raise SystemExit('Binning method "Equal Ranges of Values" is not applicable for Nominal variables...')
        bns = spih_erv(x, w, xtp, md, sv)
    else:
        raise SystemExit('Unknown binning method...')
    flg = 0
    if len(bns) <= 1: flg = 1
    if not flg and xtp == 'num':
        for k in range(1,len(bns)): bns[k]['rb'] = bns[k+1]['lb']
        bns[1]['lb'] = -np.inf
        bns[len(bns)]['rb'] = np.inf
    if 'bns' in locals() and not bns == 0: bns = binMOS(bns, x, w, sv, xtp)
    else:                                  bns = {}
    return bns
###################################################################################
