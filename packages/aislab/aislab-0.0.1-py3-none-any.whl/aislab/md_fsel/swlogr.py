import numpy as np
import pandas as pd
from op_nlopt import *
from sf import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

###################################################################################
def bElimin(model, step, x, y, w, st0, par): 
    # Backward Elimination Step
    if par['met'] == 'FR': return model, step, st0, par
    Nw, z, met, cnames, s_min, SLE, SLS, iterate, nbm_crit, pInv, ivi, ivo, n1, n2 = parin(st0, model[-1], par)
    ivi0 = ivi
    if met == 'FR': return model, step, st0, par
    # ----- Find next best model -----
    if ivi.shape[0] > 1:
        p_Fpi, ind = nextmdl('BE2', model[-1])
        
#    if length(model) == 6,  # simulate insignificant factor
#       p_Fpi = 0.4; ind = 3;
#    end

        if p_Fpi > SLS:
            ivi = ivi0[np.hstack((np.arange(0, ind), np.arange(ind+1, len(ivi))))]
            ivo = np.vstack((ivo, ivi0[ind]))
            model1 = mdl(x[:, ivi[:, 0] - 1], y, w, ivi, n2 - 1, st0, par)
            ym = lgr_apl(x[:, ivi[:, 0] - 1], model1)
            st_ext = stmdl('FS1', x, y, ym, w, st0, model1, n2 - 1, ivi, ivo, pInv)
            model = model + [htmdl('BE1', [], 'BE', n2 - 1, ivi, ivo, cnames, ivi0[ind], model1['pm'], st_ext)]
            visualz(model, par)
            for i in np.arange(0, len(model) - 1):
                if len(model[i]['ivi'][:, 0]) == len(model[-1]['ivi'][:, 0]) and all(model[i]['ivi'] == model[-1]['ivi']): iterate = 0
            step = 'BE'
        else:
            if met == 'BR' or step== 'FE_STOP': iterate = 0
            step = 'BE_STOP'
    else:
        if met == 'BR' or step == 'FE_STOP': iterate = 0
        step = 'BE_STOP'
    
    par['iterate'] = iterate
    return model, step, st0, par
###################################################################################
def firstmdl(x, y, w, st0, par): 
    pInv = {}
    pInv['met'] = par['invmet']
    pInv['type'] = par['invtype']
    pInv['smin'] = par['inv.smin']
    if par['mtp'] == 'full':
        z = st0['z']
        ivi = c_(np.arange(1, z + 1))
        ivo = c_(np.array([])).astype(int)
        n2 = ivi.shape[0]
        model = mdl(x, y, w, ivi, n2, st0, par)
        ym = lgr_apl(x, model)
        st_ext = stmdl('BE1', x, y, ym, w, st0, model, n2, ivi, ivo, pInv)
        model = [htmdl('BE1', [], 'BE', n2 ,ivi ,ivo, par['cnames'], [], model['pm'], st_ext)]
    else:
        if par['mtp'] == 'empty':
            z = st0['z']
            ivi = c_(np.array([1]))
            ivo = c_(np.arange(2, z + 1))
            n2 = ivi.shape[0]
            modelInt = {}
            modelInt['st'] = st0['modelInt']
            modelInt['pm'] = st0['modelInt']['pm']
            st_ext = stmdl('FS1', x, y, st0['modelInt']['ovr']['ym0'], w, st0, modelInt, n2, ivi, ivo, pInv);
            pm = st0['modelInt']['pm']
            model = [htmdl('FS1', [], 'FS', n2, ivi, ivo, par['cnames'], [], pm, st_ext)]
        else:
            if par['mtp'] == 'init':
                z = st0['z']
                ivi = par['ivi']
                ivo = c_(np.setxor1d(c_(np.arange(1, z + 1)), ivi))
                n2 = ivi.shape[0]
                model = mdl(x[:, ivi[:, 0] - 1], y, w, ivi, n2, st0, par)
                ym = lgr_apl(x[:, ivi[:, 0] - 1], model)
                st_ext = stmdl('BE1', x, y, ym, w, st0, model, n2, ivi, ivo, pInv)
                model = [htmdl('BE1', [], 'BE', n2, ivi, ivo, par['cnames'], [], model['pm'], st_ext)]
            else:
                raise Exception('First model type is not defined...')
    
    step = 'START'
    return model, step, st0, par
###################################################################################
def fSelect(model, step, x, y, w, st0, par): 
    # Forward Selection Step
    if par['met'] == 'BR' or step == 'BE': return model, step, st0, par
    Nw, z, met, cnames, s_min, SLE, SLS, iterate, nbm_crit, pInv, ivi, ivo, n1, n2 = parin(st0, model[-1], par)    
    # ----- Find next best model -----
    if not len(ivo) == 0:
        minPvalSne, ind = nextmdl('FS2', model[-1])
        if minPvalSne <= SLE:
            ivi0 = np.hstack((np.matlib.repmat(ivi[:, 0], z - n2, 1), ivo))
            ivi = c_(ivi0[ind, :])
            ivo = np.delete(ivo, ind, 0)
            model1 = mdl(x[:, ivi[:, 0] - 1], y, w, ivi, n2 + 1, st0, par)
            ym = lgr_apl(x[:, ivi[:, 0] - 1], model1)
            st_ext = stmdl('FS1', x, y, ym, w, st0, model1, n2 + 1, ivi, ivo, pInv)
            model = model + [htmdl('FS1' , [], 'FS', n2 + 1, ivi, ivo, par['cnames'], ivi[-1], model1['pm'], st_ext)]
            visualz(model, par)
            for i in np.arange(0, len(model) - 1):
                if len(model[i]['ivi'][:, 0]) == len(model[-1]['ivi'][:, 0]) and all(model[i]['ivi'] == model[-1]['ivi']): iterate = 0
            step = 'FS'
        else:
            if met == 'FR' or step == 'BE_STOP': iterate = 0
            step = 'FE_STOP'
    else:
        if met == 'FR' or step == 'BE_STOP': iterate = 0
        step = 'FE_STOP'
    
    par['iterate'] = iterate
    return model, step, st0, par
###################################################################################
def htmdl(mode, model, FB, n2, ivi, ivo, cnames, ind2, pm, st): 
    if len(model) == 0: model = {}; model
    if not 'st' in model:  model['st'] = {}
    if not 'in' in model['st']:  model['st']['in'] = {}
    if not 'out' in model['st']: model['st']['out'] = {}
    if not 'ovr' in model['st']: model['st']['ovr'] = {}
    if len(ind2) > 0: ind2 = ind2 - 1
    # Model history
    if mode == 'FS1' or mode =='BE1':
        if ivi.shape[0] == 0: model['cname_i'] = c_(np.array(['']))
        else:                 model['cname_i'] = np.array(cnames)[ivi - 1]
        if ivo.shape[0] == 0: model['cname_o'] = c_(np.array(['']))
        else:                 model['cname_o'] = np.array(cnames)[ivo - 1]
        model['FB'] = FB
        model['n'] = n2
        model['xio'] = np.array(cnames)[ind2]
        model['pm']= pm
        model['ivi'] = ivi
        model['ivo'] = ivo
        model['st']['in'] = st['in']
        model['st']['out'] = st['out']
        model['st']['ovr'] = st['ovr']
    elif mode == 'FS2':
        model['st']['out'] = st
    elif mode == 'BE2':
        model['st']['in'] = st
    
    return model
###################################################################################
def mdl(x, y, w, ivi, n2, st0, par):
    # Initial model parameters
    lambda_ = st0['modelInt']['pm']
    if par['metpminit'] == 'zero':   pm = np.vstack((c_([lambda_]), np.zeros((n2 - 1,1))))
    elif par['metpminit'] == 'prev': pm = par['pm0']
    elif par['metpminit'] == 'fapp':
        model0 = lspm(x, (y - 0.5)*2*lambda_)
        pm = model0['Pm']
    # Arguments for func, grad, hes calculation
    if len(x.shape) == 1: x = c_(x)
    args = {}
    args['data'] = np.hstack((x, y, w, np.zeros((st0['N'], 1))))
    if np.size(ivi) == 1: args['cnames'] = c_(np.array([par['cnames'][ivi - 1]]))
    else:                 args['cnames'] = c_(np.array(par['cnames'])[ivi - 1])
    args['x'] = pm
#    func = par['func
#    grad = par['grad
#    hes = par['hes
    func = 1
    grad = 1
    hes = 1
    pm, F, g, H, Hinv, __ = newton(pm, func, grad, hes, args, par)
    # # Denormalization
    # pm = denormPar(dset, pmn);
    
    model = {'pm': pm, 
             'st': {'ovr': {'F': F, 
                            'g': g, 
                            'H': H, 
                            'Hinv': Hinv}
                    } 
              }
    return model
###################################################################################
def nextmdl(mode, model): 
#    model = model[-1]
    if mode == 'FS2':
        pvalSne = model['st']['out']['p_valSne']
        minPvalSne, ind = min1(pvalSne)
    else:
        if mode=='BE2':
            p_valW = model['st']['in']['p_valW']
            # p_valW[0] = 0 # !!!!!!!!!!!!!!!!!!!
            minPvalSne, ind = max1(p_valW)
    return minPvalSne, ind
###################################################################################
def parin(st0, model, par):
    Nw = st0['Nw']
    z = st0['z']
    met = par['met']
    cnames = par['cnames']
    s_min = par['smin']
    SLE = par['SLE']
    SLS = par['SLS']
    iterate = par['iterate']
    nbm_crit = par['nbm_crit']
    pInv = {}
    pInv['met'] = par['invmet']
    pInv['type'] = par['invtype']
    pInv['smin'] = par['smin']
    ivi = model['ivi']
    ivo = model['ivo']
    n1 = len(ivi) - 1
    n2 = n1 + 1;
    return Nw, z, met, cnames, s_min, SLE, SLS, iterate, nbm_crit, pInv, ivi, ivo, n1, n2

###################################################################################
def scrChiSq(x, y, ym0, ym, w, st0, model, mode, ivi, ivo, pInv): 
# Score Chi-Square statistics for group-wise selection/elimination
#--------------------------
# Author: Alexander Efremov
# Date:   20.12.2009
#--------------------------
    z = st0['z']
    n1 = len(ivi)
    g = model['st']['ovr']['g']
    Hinv = model['st']['ovr']['Hinv']
    n = x.shape[1]
    if mode == 'resid':
        Fish = (x*ym*(1 - ym)*w).T@x
        g = x.T@((y - ym)*w)
        invFish = nsinv(Fish, pInv['smin'])
        S = g.T@invFish@g
    elif mode=='globNul':
        ni = len(ivi)
        xin = x[:, ivi[:, 0] - 1]
        F11 = (xin*ym0*(1 - ym0)*w).T@xin
        g11 = xin.T@((y - ym0)*w)
        S = g11.T@nsinv(F11, pInv['smin'])@g11
    elif mode == 'freg':
        nci = ivi.shape[0]
        nco = ivo.shape[0]
        if nci == 0:
            S = np.nan
            return S
        gin = -g
        if nco == 0:
            S = c_(np.array([]))
            return S
        S = nans((nco, 1))
        fi = np.hstack((np.matlib.repmat(ivi.T - 1, z - n1, 1), ivo - 1))
        for i in np.arange(0, nco):
            xout = x[:, int(ivo[i, 0] - 1)]
            gout = xout.T@((y - ym)*w)
            Hi = -(x[:, fi[i, :]]*ym*(1 - ym)*w).T@x[:,fi[i, :]]
            g = np.vstack((gin, gout))
            S[i, 0] = (g.T@(-inv2(Hi, Hinv, pInv))@g)[0, 0]
    return S
###################################################################################
def swlogr(x, y, w, par): 
    N = x.shape[0]
    if par['pm0'] == 1:
        x = np.hstack((np.ones((N, 1)), x))
        par['cnames'] = ['intercept'] + par['cnames']
        par['ivi'] = np.vstack((1, par['ivi'] + 1))
    par['iterate'] = 1
    st0 = stats(x, y, w, par)
    model, step, st0, par = firstmdl(x, y, w, st0, par)
    while par['iterate']:
        model, step, st0, par = bElimin(model, step, x, y, w, st0, par)
        model, step, st0, par = fSelect(model, step, x, y, w, st0, par)
    return model
###################################################################################
def stats(x, y, w, par):
    pInv = {'met': par['invmet'], 
            'type': par['invtype'], 
            'smin': par['inv.smin']}
    N, z = x.shape
    Nw = sum(w)
    my = y.T@w/Nw
    st0 = {'N': N, 
           'Nw': Nw, 
            'z': z, 
            'my': my, 
            'modelInt': {'pm': np.log(my/(1 - my))}}
    modelInt = mdl(x[:, 0], y, w, 1, 1, st0, par)
    modelInt['FB'] = 'FS'
    modelInt['xio'] = 'intercept'
    modelInt['cname_i'] = c_(np.array(['intercept']))
    modelInt['cname_o'] = c_(np.array(par['cnames'][1:z]))
    ym0 = lgr_apl(x[0, 0], modelInt)
    
    st0['modelInt']['ovr'] = modelInt['st']['ovr']
    st0['modelInt']['ovr']['ym0'] = ym0
    st0['modelInt']['pm'] = modelInt['pm']
    st_ext = stmdl('BE1', x, y, ym0, w, st0, modelInt, 1, 1, c_(np.arange(2,z+1)), pInv)
    st0['modelInt'] = st_ext
    st0['modelInt']['ovr']['ym0'] = ym0
    st0['modelInt']['pm'] = modelInt['pm']
    modelInt['st'] = st_ext
    visualz([modelInt], par)
    return st0
###################################################################################
def stmdl(FB, x, y, ym, w, st0, model, n2, ivi, ivo, pInv): 
    N = st0['N']
    Nw = st0['Nw']
    z = st0['z']
    if not isinstance(ivi, np.ndarray): ivi = np.array([[ivi]])

    ym0 = np.matlib.repmat(st0['modelInt']['ovr']['ym0'], N, 1)
    if len(ym) == 1: ym = np.matlib.repmat(ym, N, 1)
    ivi0 = np.hstack((np.matlib.repmat(ivi.T, z-n2, 1), ivo))
    L0 = -st0['modelInt']['ovr']['F']
    L = - model['st']['ovr']['F']
    Hinv = model['st']['ovr']['Hinv']
    pm = model['pm']
    n = n2
    
    # Overall Stats & Model Measures /AIC, SC, Rg2, Rg2n, Rg2adj/
    st = {}; st['ovr'] = {}; st['in'] = {}; st['out'] = {}; st['globNul'] = {}
    st['ovr']['N'] = N
    st['ovr']['Nw'] = Nw
    st['ovr']['F'] = model['st']['ovr']['F']
    st['ovr']['g'] = model['st']['ovr']['g']
    st['ovr']['H'] = model['st']['ovr']['H']
    st['ovr']['Hinv'] = model['st']['ovr']['Hinv']
    st['ovr']['AIC'] = - 2 * L + 2 * n
    st['ovr']['BIC'] = - 2 * L + (n + 0) * np.log(N)
    st['ovr']['Rg2'] = 1 - np.exp(2 * (L0 - L) / (N - 1))
    st['ovr']['Rg2n'] = 1 - np.exp(2 * (L0 - L) / (Nw - 1))
    st['ovr']['Rg2adj'] = st['ovr']['Rg2'] / (1 - np.exp(2 * L0 / (N - 1)))
    st['ovr']['Rg2adjn'] = st['ovr']['Rg2n'] / (1 - np.exp(2 * L0 / (Nw - 1)))
    # Individual Estimate Measures /stdpe, W, Psi, PsiL, PsiU/
    FishInv = Hinv
    stde = c_(np.sqrt(np.diag(FishInv)))
    st['in']['W'] = (pm/stde) ** 2
    v = np.ones(st['in']['W'].shape)
    st['in']['p_valW'] = gamq(v/2, st['in']['W'][:, 0]/2)
    st['in']['Psi'] = np.exp(pm)
    st['in']['PsiL'] = np.exp(pm - 1.96 * stde)
    st['in']['PsiU'] = np.exp(pm + 1.96 * stde)
    
    st['in']['stdpe'] = stde
    if n > 0 and FB != 'full' or FB != 'BR':
        # - Residual Score Chi-Square Test
        st['ovr']['Sr'] = scrChiSq(x, y, ym0, ym, w, st0, model, 'resid', ivi, ivo, pInv)
        v = np.array([x.shape[1] - n])
        st['ovr']['p_valSr'] = gamq(v/2, st['ovr']['Sr']/2)
        st['ovr']['dfSr'] = v
        # - Chi-Square Score for not entered factors
        st['out']['Sne'] = scrChiSq(x, y, ym0, ym, w, st0, model, 'freg', ivi, ivo, pInv)
        v = np.matlib.repmat(ivi0.shape[1], len(ivo), 1)
        st['out']['p_valSne'] = gamq(v/2, st['out']['Sne']/2)
        # Global Null Hypothesis Test: BETA=0
        v = n - 1
        # - LogLikelihood Ratio
        L = - model['st']['ovr']['F']
        L0 = - st0['modelInt']['ovr']['F']
        st['ovr']['globNul'] = {'LR': 2 * (L - L0)}
        st['ovr']['globNul']['p_valLR'] = gamq(v/2, st['ovr']['globNul']['LR']/2)
        st['ovr']['globNul']['dfLR'] = v
        # - Score
        st['ovr']['globNul']['S0'] = scrChiSq(x, y, ym0, ym, w, st0, model, 'globNul', ivi, ivo, pInv)
        v = n * np.ones(st['ovr']['globNul']['S0'].shape) - 1
        st['ovr']['globNul']['p_valS0'] = gamq(v/2, st['ovr']['globNul']['S0']/2)
        st['ovr']['globNul']['dfS0'] = v
        # - Wald
        pm0 = np.vstack((st0['modelInt']['pm'], np.zeros((n - 1, 1))))
        pm = model['pm']
        dp = pm - pm0
        xin = x[:, ivi[:, 0] - 1]
        F1 = (xin*ym*(1 - ym)*w).T@xin
        Finv1 = nsinv(F1, pInv['smin'])
        if n > 1:
            stdpe = c_(np.sqrt(np.diag(Finv1)))
            st['ovr']['globNul']['W0'] = sum((dp[1:, :]/stdpe[1:, :])**2)
            v = n*np.ones(st['ovr']['globNul']['W0'].shape) - 1
            st['ovr']['globNul']['p_valW0'] = gamq(v/2,st['ovr']['globNul']['W0']/2)
            st['ovr']['globNul']['dfW0'] = v
    else:
        st['Sr'] = NaN
        st['p_valSr'] = NaN
        st['Sne'] = nans((len(model['ifo']), 1))
        st['p_valSne'] = nans((len(model['ifo']), 1))
        st['globNul']['LR'] = NaN
        st['globNul']['p_valLR'] = NaN
        st['globNul']['S0'] = NaN
        st['globNul']['p_valS0'] = NaN
        st['ovr']['globNul']['W0'] = NaN
        st['ovr']['globNul']['p_valW0'] = NaN
        st['ovr']['globNul']['df'] = NaN
    
# # Measures of Association
# st = assoc(model, st, y, ym);
# # Variance Inflation Factor
# st.in.VIF = vif(x(:, ivi));
    return st
###################################################################################
def visualz(model, par): 
    mode = par['dsp']
    if mode == 'no': return
    step = len(model) - par['iterate']
    print('Step: ', step, '  =================================================================================================================')
    modelInt = model[0]
    model = model[-1]
    FB = model['FB']
    if FB == 'FS' and step != 0:  print('Entered factor: ', model['xio'])
    elif FB=='BE' and step != 0:  print('Exited factor: ', model['xio'])
    elif FB=='FS' and step == 0:  print('Initial model: intercept')
    elif FB=='BE' and step == 0:  print('Initial model: full')
    
    pm = model['pm']
    n = len(pm)
    if mode == 'all':
        if n > 1:
            print('--- Overall model fit measures ---')
            Rg2 = model['st']['ovr']['Rg2n']
            MaxRescRg2 = model['st']['ovr']['Rg2adjn']
            AIC_Intercept = modelInt['st']['ovr']['AIC']
            BIC_Intercept = modelInt['st']['ovr']['BIC']
            BIC_Current = model['st']['ovr']['BIC']
            AIC_Current = model['st']['ovr']['AIC']
            L = model['st']['ovr']['F']
            L0 = modelInt['st']['ovr']['F']
            Neg2LogL_Intercept = - 2 * L0
            Neg2LogL_Current = - 2 * L
            print(pd.DataFrame({'Rg2': Rg2,
                                'MaxRescRg2': MaxRescRg2,
                                'BIC_Intercept': BIC_Intercept,
                                'BIC_Current': BIC_Current,
                                'AIC_Intercept': AIC_Intercept,
                                'AIC_Current': AIC_Current,
                                'Neg2LogL_Intercept': Neg2LogL_Intercept,
                                'Neg2LogL_Current': Neg2LogL_Current
                                }))
            print('------------------------------------------------------')
            print(' ')
        print(np.array(['--- Analysis of Maximum Likelihood Estimates & Odds Ratio Estimates ---']))
        No = np.arange(1,n+1) - 1
        Variable = model['cname_i'][:, 0]
        DF = np.ones(pm.shape[0])
        Estimate = pm[:, 0]
        StandardError = model['st']['in']['stdpe'][:, 0]
        WaldChiSquare = model['st']['in']['W'][:, 0]
        PrWaldChiSquare = model['st']['in']['p_valW'][:, 0]
        #    VIF = model.st.in.VIF;
        OddsRatio = model['st']['in']['Psi'][:, 0]
        Lower95Prc = model['st']['in']['PsiL'][:, 0]
        Upper95Prc = model['st']['in']['PsiU'][:, 0]
        #    disp(table(No, Variable, DF, Estimate, StandardError, VIF, WaldChiSquare, PrWaldChiSquare, OddsRatio, Lower95Prc, Upper95Prc))
        print(pd.DataFrame({'No': No,
                            'Variable': Variable,
                            'DF': DF,
                            'Estimate': Estimate,
                            'StandardError': StandardError,
                            'WaldChiSquare': WaldChiSquare,
                            'PrWaldChiSquare': PrWaldChiSquare,
                            'OddsRatio': OddsRatio,
                            'Lower95Prc': Lower95Prc,
                            'Upper95Prc': Upper95Prc
                            }))
        print('------------------------------------------------------')
        print(' ')
        if n > 1:
            print(np.array(['--- Global Null Hypothesis Test: BETA=0 ---']))
            if (step > 0 and str(mode) == str('all')) or str(FB) == str('BR'):
                if len(model['ivi']) > 1:
                    LR = model['st']['ovr']['globNul']['LR']
                    p_valLR = model['st']['ovr']['globNul']['p_valLR']
                    S0 = model['st']['ovr']['globNul']['S0']
                    p_valS0 = model['st']['ovr']['globNul']['p_valS0']
                    W0 = model['st']['ovr']['globNul']['W0']
                    p_valW0 = model['st']['ovr']['globNul']['p_valW0']
                    dfLR = model['st']['ovr']['globNul']['dfLR']
                    dfS0 = model['st']['ovr']['globNul']['dfS0']
                    dfW0 = model['st']['ovr']['globNul']['dfW0']
                else:
                    LR = NaN
                    p_valLR = NaN
                    S0 = NaN
                    p_valS0 = NaN
                    W0 = NaN
                    p_valW0 = NaN
                    dfLR = NaN
                    dfS0 = NaN
                    dfW0 = NaN
            Test = np.transpose(np.array(['Likelihood Ratio','Score','Wald']))
            Chi_Sq = np.array([LR, S0, W0[-1]])
            DF = np.array([dfLR, dfS0, dfW0[-1]])
            pval = np.array([p_valLR, p_valS0, p_valW0[-1]])[:, 0]
            print(pd.DataFrame({'Test': Test,
                                'Chi_Sq': Chi_Sq,
                                'DF': DF,
                                'pval': pval
                                }))
            print('------------------------------------------------------')
            print(np.transpose(np.array([' '])))
        print(np.array(['--- Residual Chi-Square Test ---']))
        ChiSq = model['st']['ovr']['Sr'][:, 0]
        DF = model['st']['ovr']['dfSr']
        p_valChiSq = model['st']['ovr']['p_valSr'][:, 0]
        print(pd.DataFrame({
                            'ChiSq': ChiSq,
                            'DF': DF,
                            'p_valChiSq': p_valChiSq
                            }))
        print('------------------------------------------------------')
        print(' ')
    
    if 'in' in model['st'] and mode == 'all':
        if n > 1:
            #       disp(['---------- Association of Prediction and Observed Response ----'])
#       Pc = model['st['ovr.assoc.Pc;
#       Pd = model['st['ovr.assoc.Pd;
#       Pt = model['st['ovr.assoc.Pt;
#       Nt = model['st['ovr.assoc.Nt;
#       SomersD = model['st['ovr.assoc.SomersD;
#       gamma = model['st['ovr.assoc.gamma;
#       tau_a = model['st['ovr.assoc.tau_a;
#       c = model['st['ovr.assoc.c;
#       RankCorStats = {'PrcConcordant', 'PrcDiscordant', 'PrcTied', 'Pairs', 'Somers'' D', 'Gamma', 'Tau_a', 'c'}';
#       Values = [Pc Pd, Pt, Nt, SomersD, gamma, tau_a, c]';
#       disp(table(RankCorStats, Values))
#       disp(['------------------------------------------------------'])
#       disp([' ']')
            pass
    
    if n > 1:
        print(np.array(['--- Factors Eligible for Removal ---']))
        No = np.arange(2, n+1) - 1
        Variable = model['cname_i'][1:][:, 0]
        W = model['st']['in']['W'][:, 0]
        p_valW = model['st']['in']['p_valW'][:, 0]
        DF = np.ones((W.shape[1-1] - 1,))
        WaldChiSquare = W[1:]
        PrWaldChiSquare = p_valW[1:]
        print(pd.DataFrame({'No': No,
                            'Variable': Variable, 
                            'DF': DF, 
                            'WaldChiSquare': WaldChiSquare, 
                            'PrWaldChiSquare': PrWaldChiSquare
                            }))
        print('------------------------------------------------------')
        print(' ')
        if not FB=='BE' :
            print('No factors are removed in Step', step)
            print(' ')
    
    if 'out' in model['st'] and mode == 'all':
        print('---Factors Eligible for Entry ---')
        ScoreChiSq = model['st']['out']['Sne'][:, 0]
        p_valScoreChiSq = model['st']['out']['p_valSne'][:, 0]
        No = np.arange(1, len(ScoreChiSq)+1)
        DF = np.ones((ScoreChiSq.shape[0], ))
        Variable = model['cname_o'][:, 0]
        print(pd.DataFrame({'No': No,
                            'Variable': Variable, 
                            'DF': DF, 
                            'ScoreChiS': ScoreChiSq, 
                            'p_valScoreChiSq': p_valScoreChiSq
                            }))
        print('------------------------------------------------------')
        print(' ')
    
    if mode == 'all': toc2()