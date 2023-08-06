import numpy as np
#import numpy.matlib
from sf import *

###################################################################################
def dspl(flg, **kwargs): 
#--------------------------
# Author: Alexander Efremov
# Date:   20.12.2009
#--------------------------
    par = kwargs['par']
    if flg == 1:
        ivi = par['ivi']
        x = kwargs['x']
        F = kwargs['F']
        itr = kwargs['itr']
        cnames = kwargs['args']['cnames']
        
        s = kwargs['s']
        spc = '   '
        if itr == 0 and not 'newtls' in par:
            print('---------- Newton-Raphson Method Log ------------')
            print('[Iter][  Step  ][Objective Function]', cnames[:, 0])
            print(itr, 'initial', s, F, x.T)
        else:
            print(itr, par['meth'], s, F, x.T)
    else:
        if flg == 2:
            x = kwargs['x']
            xx = kwargs['xx']
            F = kwargs['F']
            FF = kwargs['FF']
            g = kwargs['g']
            H = kwargs['H']
            itr = kwargs['itr']
            msg = kwargs['msg']
            par = kwargs['par']
            print(' ')
            if not len(FF)==0 :
                print('Last Change of F: ', F - FF[0])
                print(' ')
            print('Last Gradient')
            print(g)
            print(' ')
            if 'A' == msg:   print('Convergence criterion (FCONV = ', par['fcnv'], ') satisfied. /Initial model/')
            elif 'B' == msg: print('Stopping Rule (MaxIter = ', par['maxiter'], ') satisfied. /', itr, '/')
            elif 'C' == msg: print('Convergence criterion (FCONV = ', par['fcnv'], ') satisfied. /', np.abs(F - FF[0])/(np.abs(FF[0]) + 1e-6), '/')
            elif 'D' == msg: print('Convergence criterion (ABSFCONV = ', par['afcnv'], ') satisfied. /', np.abs(F - FF[0]), '/')
            elif 'E' == msg: print('Convergence criterion (XCONV = ', par['xcnv'], ') satisfied. /', (x - xx[:, 0]).T/x, '/')
            elif 'F' == msg: print('Convergence criterion (GCONV = ', par['gcnv'], ') satisfied. /', -g.T@H@g/(np.abs(F) + 1e-6), '/')
            elif 'G' == msg: print('Termination: reaching the uncretainty level...')
            elif 'H' == msg: print('Termination: Hessian is a zero matrix...')
            else:
                print('Termination is caused by unknown reason...')
            print('----------------------------------------------------------')
            print(np.transpose(np.array([' '])))
###################################################################################
def f_lgr(args = None): 
#---------------------------------------------
# Author: Alexander Efemov
# Date:   20.12.2009
# Course: Modelling and Processes Optimization
#---------------------------------------------
    # F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h-3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    mdl ={'pm': pm}
    if x.shape[1] == 0: x = c_(x)
    ym = lgr_apl(x, mdl)
    ym[ym > 1 - 1e-10] = 1 - 1e-10
    ym[ym < 1e-10] = 1e-10
    m = pm.shape[1]
    yy = np.matlib.repmat(y, 1, m)
    ww = np.matlib.repmat(w, 1, m)
    F = -sum(yy*np.log(ym)*ww + (1 - yy)*np.log(1 - ym)*ww)
    args['data'][:, -1] = ym.flatten()
    return F, args
###################################################################################
def g_lgr(args = None): 
#---------------------------------------------
# Author: Alexander Efemov
# Date:   20.12.2009
# Course: Modelling and Processes Optimization
#---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h-3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    g = -x.T@((y - ym)*w)
    return g
###################################################################################
def H_lgr(args = None): 
#---------------------------------------------
# Author: Alexander Efemov
# Date:   20.12.2009
# Course: Modelling and Processes Optimization
#---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h-3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    n = x.shape[1]
    H = (x*np.matlib.repmat(ym*(1 - ym)*w, 1, n)).T@x
    return H
###################################################################################
def lgr_apl(X, mdl):
    # logistic regression function
    pm = mdl['pm']
    if not isinstance(X, np.ndarray): X = np.array([[X]])
    if not isinstance(pm, np.ndarray): pm = np.array([[pm]])
    ym = 1/(1 + np.exp(-X@pm))
    return ym
###################################################################################
def optOmit(x, xx, F, FF, g, g_1, H, H_1, Hinv, Hinv_1, iterate, s, tmp, par): 
#---------------------------------------------
# Author: Alexander Efemov
# Date:   20.12.2009
# Course: Modelling and Processes Optimization
#---------------------------------------------
    msg = 0
    flg = 0
    if par['smeth'] == 'fprev2' or par['smeth'] == 'fprev3':
        if iterate == 1 and F > FF[0]:
            if F < tmp['F']:
                par['sc'] = s/2
                tmp['F'] = F
                tmp['x'] = x
                tmp['g'] = g
                tmp['H'] = H
                tmp['Hinv'] = Hinv
                x = c_(xx[:, 0])
                F = FF[0]
                g = g_1
                H = H_1
                Hinv = Hinv_1
            else:
                #          disp('The uncertainty level has been reached and the precision could not be increased. Note: it is assumed that the objective function is unimodal and in last direction two extrema are detected. The optimization is terminated.')
                if FF[0] < tmp['F']:
                    F = FF[0]
                    x = c_(xx[:, 0])
                    g = g_1
                    H = H_1
                    Hinv = Hinv_1
                else:
                    x = tmp['x']
                    F = tmp['F']
                    g = tmp['g']
                    H = tmp['H']
                    Hinv = tmp['Hinv']
                iterate = 0
                msg = 'G'
            flg = 1
        else:
            tmp['F'] = np.inf
            par.sc = []
    return x, F, g, H, Hinv, tmp, par, iterate, msg, flg
###################################################################################
def stepPar(s, F, FF, g, g_1, iter, flg, par): 
# Stepsize Determination
#---------------------------------------------
# Author: Alexander Efemov
# Date:   20.12.2009
# Course: Modelling and Processes Optimization
#---------------------------------------------
    if not len(par['sc']) == 0:
        s = par['sc']
    elif par['smeth'] == 'fprev2' or par['smeth'] == 'fprev3':
        su = par['su']
        p_decr = par['p_decr']
        p_incr = par['p_incr']
        #    smax = par['s_max']
        nn = len(FF)
        FF[np.arange(nn, 4)] = NaN
        c[0] = FF(1) < FF(2)
        c[1] = FF(0) < FF(1)
        c[2] = F < FF(0)
        if (iter == 1 or iter == 2) and c(3) == 0:
            s1 = p_decr*s
        elif iter > 1 and par['smeth'] == 'fprev2':
            if np.all(c(3) == 1): s1 = p_incr*s
            else:                 s1 = p_decr*s
        elif iter > 2 and par['smeth'] == 'fprev3':
            if   np.all(c == np.array([1,1,1])): s1 = p_incr*s
            elif np.all(c == np.array([1,1,0])): s1 = p_decr*s
            elif np.all(c == np.array([1,0,1])): s1 = s
            elif np.all(c == np.array([1,0,0])): s1 = p_decr*s
            elif np.all(c == np.array([0,1,1])): s1 = s
            elif np.all(c == np.array([0,1,0])): s1 = p_decr*s
            elif np.all(c == np.array([0,0,1])): s1 = s
            elif np.all(c == np.array([0,0,0])): s1 = p_decr*s
        else:
            s1 = s
        s = min([s1, su*np.abs(p_incr - 1)/5 + s])
        if s > su:   s = su
        if flg == 1: s = s / 2
    elif par['smeth'] == 'gang':
            su = par['su']
            if iter < 1: 
                s = 1
            else:
                norm2g = np.sqrt(g.T@g)
                norm2g_1 = np.sqrt(g_1.T@g_1)
                s = 1e-10 + (pi - np.arccos(min(1, g_1.T@g/max(norm2g_1*norm2g, 1e-06))))/pi*(su - 1e-10)
    elif par['meth'] == 'none':
        s = 1
    return s
###################################################################################
def stopcrt(x=None, F=None, xx=None, FF=None, g=None, H=None, itr=None, par=None):
# Stopping Criteria
# Contains a set of convergence criteria for NR, NRLS, NRPI, SD, etc.
#---------------------------------------------
# Author: Alexander Efemov
# Date:   20.12.2009
# Course: Modelling and Processes Optimization
#---------------------------------------------
    if FF is None:                              F_1 = None
    elif isinstance(FF, (int, float)):          F_1 = FF
    else:                                       F_1 = FF[0, 0]
    if isinstance(xx, list) and len(xx) == 0:   x_1 = None
    elif isinstance(xx, (int, float)):          x_1 = xx
    else:                                       x_1 = xx[:, 0]
    iterate = 1
    msg = '0'
    if 'maxiter' in par:
        maxiter = par['maxiter']
        if itr >= maxiter:
            iterate = 0
            msg = 'B'
            return iterate, msg
    if 'fcnv' in par and not F_1 is None:
        fcnv = par['fcnv']
        if np.abs(F - F_1)/min(np.array([1e12, np.abs(F_1) + 1e-6])) < fcnv:
            iterate = 0
            msg = 'C'
            return iterate, msg
    if 'afcnv' in par and not F_1 is None:
        afcnv = par['afcnv']
        if np.abs(F - F_1) < afcnv:
            iterate = 0
            msg = 'D'
            return iterate, msg
    if 'xcnv' in par and not x_1 is None:
        x_1 = c_(x_1)
        d = nans(x.shape)
        xcnv = par['xcnv']
        ind1 = np.argwhere(np.abs(x_1) < 0.01)
        ind2 = np.argwhere(np.abs(x_1) >= 0.01)
        d[ind1, 0] = x[ind1, 0] - x_1[ind1, 0]
        d[ind2, 0] = (x[ind2, 0] - x_1[ind2, 0])/x_1[ind2, 0]
        if np.all(np.abs(d) <= xcnv):
            iterate = 0
            msg = 'E'
            return iterate, msg
    if 'gcnv' in par:
        gcnv = par['gcnv']
        if g.T@H@g/(np.abs(F) + 1e-6) < gcnv:
            iterate = 0
            msg = 'F'
            return iterate, msg
    return iterate, msg
###################################################################################

