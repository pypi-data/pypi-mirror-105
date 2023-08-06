import numpy as np
import pandas as pd 

from sf import *

##############################################################################
def firstgen(pop, par, args):
    F = [func(pop[x], par, args) for x in range(len(pop))]
    sorted_F = sorted([[pop[x], F[x]] for x in range(len(pop))], key = lambda x: x[1])
    population = [sorted_F[x][0] for x in range(len(sorted_F))]
    F = [sorted_F[x][1] for x in range(len(sorted_F))]
    return {'individuals': population, 'F': sorted(F)}
##############################################################################
def func(x, par, args):
    from sklearn.metrics import confusion_matrix
    data = args['data']
    BRA = args['BRA']
    BRR = args['BRR']
    TA = args['TA']
    TR = args['TR']
    minNb = args['minNb']
    minNgb = args['minNgb']
    mindBR = args['mindBR']
    w = args['w']

    cutoffs_GB = [-np.inf, x[0], x[1], x[2], x[3], np.inf] 
    cutoffs_GBR = [-np.inf, x[4], x[5], x[6], x[7], np.inf]
    
    if len(set(cutoffs_GB)) != len(cutoffs_GB):   return -np.inf 
    if len(set(cutoffs_GBR)) != len(cutoffs_GBR): return -np.inf 

    try:
        GB_zones = pd.cut(data['Score_GB'], cutoffs_GB, labels = False, retbins = False, right = True)
        GBR_zones = pd.cut(data['Score_GBR'], cutoffs_GBR, labels = False, retbins = False, right = True)
    except:
        print("ERRORRRORRRORRR")

    
    if len(np.unique(GB_zones)) < 5 or len(np.unique(GBR_zones)) < 5: return -np.inf
        
    # confusion matrix
    good = confusion_matrix(GB_zones, GBR_zones, sample_weight = data['Good'].values).astype(int)
    good = np.fliplr(np.flipud(good))
    
    good = pd.DataFrame(good, index = ['A', 'LR', 'MR', 'HR', 'R'], columns = ['A', 'LR', 'MR', 'HR', 'R'])

    bad = confusion_matrix(GB_zones, GBR_zones, sample_weight = data['Bad'].values).astype(int)
    bad = np.fliplr(np.flipud(bad))
    bad = pd.DataFrame(bad, index = ['A', 'LR', 'MR', 'HR', 'R'], columns = ['A', 'LR', 'MR', 'HR', 'R'])
        
    reject = confusion_matrix(GB_zones, GBR_zones, sample_weight = data['Reject'].values).astype(int)
    reject = np.fliplr(np.flipud(reject))
    reject = pd.DataFrame(reject, index = ['A', 'LR', 'MR', 'HR', 'R'], columns = ['A', 'LR', 'MR', 'HR', 'R'])

    # bad rate
    bad_rate = bad/(good + bad)*100
    total_gb = good + bad
    total = good + bad + reject

    drBR = bad_rate.iloc[:, 1:].values - bad_rate.iloc[:, :-1].values   # rowwise delta BR
    dcBR = bad_rate.iloc[1:, :].values - bad_rate.iloc[:-1, :].values   # colwise delta BR

    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    negdrBR = drBR[drBR < mindBR]                                       # negative trend in rowwise delta BR
    negdcBR = dcBR[dcBR < mindBR]                                       # negative trend in colwise delta BR
    
    bad_rate = bad_rate.values
    total = total.values
    
    # discriminatory power of the current strategy  #  min(F1) = 0
    F1 = (((BRA - bad_rate[0,0])/max(1e-6,100-BRA))**2 )/2 #+ ((TA - total[0,0])/max(1e-6,TA))**2)/2
    F2 = (((BRR - bad_rate[-1,-1])/max(1e-6,BRR-0))**2 + ((TR - total[-1,-1])/max(1e-6,TR))**2)/2

    # monotonicity of BR  #  min(F2) = 0
    # F2 = np.max((np.max(negdrBR) + np.max(negdcBR))**2)
    F3 = np.sum((np.sum(negdrBR)/max(16,16*mindBR) + np.sum(negdcBR)/max(16,16*mindBR))**2)
    
    # mininmum number of records per segment  #  min(F3) = 0
    # F3 = sum(sum((bad.values < minNb) & (total_gb.values > 0)))
    F4 = sum(sum(((minNb - bad.values)/max(1e-6,25*minNb))**2 * (minNb > bad.values)))
    F5 = sum(sum(((minNgb - total_gb.values)/max(1e-6,25*minNgb))**2 * (total_gb.values < minNgb)))

    # minimum number of NaN cells
    F6 = (sum(sum(np.isnan(bad_rate)))/25)**2

    # minimum number of records in most populated cell
    # F7 = np.max(np.max(total))/sum(sum(total))**2
    F7 = np.max(np.max(total))/max(1e-6,sum(sum(total)))

    F = -(w[0]*F1 + w[1]*F2 + w[2]*F3 + w[3]*F4 + w[4]*F5 + w[5]*F6 + w[6]*F7)
    if np.isnan(F): return -np.inf 
    return F
##############################################################################
def func_sim(max_F, itrConstF):
    result = False
    br = 0
    for i in range(len(max_F)-1):
        if max_F[i] == max_F[i+1]: br += 1
        else:                      br = 0
    if br == itrConstF - 1: result = True
    return result
##############################################################################
def genopt(par, args):
    itrConstF = par['stop_itrConstF']
    w = args['w']  # Acc  Rej  mt    Nb   Ngb  NaN  min_maxCell
    
    w = w/np.sum(w)
    pop = population(par, args, 0)
    gen = []
    gen.append(firstgen(pop, par, args))
    fitness_avg = np.array([sum(gen[0]['F'])/len(gen[0]['F'])])
    fitness_max = np.array([max(gen[0]['F'])])
    finish = False
    itr = 0 
    maxiter = 1200
    while finish == False:
        itr += 1
        if itr == maxiter:                              break
        if max(fitness_max) >= 0:                       break
        if max(fitness_avg) >= 0:                       break
        if func_sim(fitness_max, itrConstF) == True:    break
        gen.append(nextgen(gen[-1], par, args, itr))
        fitness_avg = np.append(fitness_avg, sum(gen[-1]['F'])/len(gen[-1]['F']))
        fitness_max = np.append(fitness_max, max(gen[-1]['F']))
        print (itr, 'Fmin = ', -gen[-1]['F'][-1])
    x_opt = gen[-1]['individuals'][-1]
    F_opt = gen[-1]['F'][-1]

    return F_opt, x_opt
##############################################################################
def individual(args, mode=1):  # ng - number of genes, lb - lower bound, ub - upper bound
    ng1 = args['ng1']
    ub1 = args['ub1']
    lb1 = args['lb1']
    ng2 = args['ng2']
    ub2 = args['ub2']
    lb2 = args['lb2']
    seed = args['seed1']
    indv_1 = rand((1,ng1), l=lb1, h=ub1, tp='int', seed=seed).flatten().tolist()
    indv_2 = rand((1,ng2), l=lb2, h=ub2, tp='int', seed=seed + ng1 + 1).flatten().tolist()
    indv_1.sort()
    indv_2.sort()
    indv = indv_1 + indv_2
    return indv 
##############################################################################
def mating(parents, seed, met='Single Point'):
    
    if met == 'Single Point':
        cut = rand(l=1, h=len(parents[0]), tp='int', seed=seed)[0,0]
        child = [parents[0][0:cut] + parents[1][cut:]]
        child.append(parents[1][0:cut] + parents[0][cut:])
    seed = seed + 1
    if met == 'Two Pionts':
        cut_1 = rand(l=1, h=len(parents[0])-1, tp='int', seed=seed)
        cut_2 = rand(l=1, h=len(parents[0]), tp='int', seed=seed+cut_1)
        br = 0
        while cut_2 < cut_1:
            br += 1
            cut_2 = rand(l=1, h=len(parents[0]), tp='int', seed=seed+2+br)
        child = [parents[0][0:cut_1] + parents[1][cut_1:cut_2] + [parents[0][cut_2:]]]
        child.append([parents[1][0:cut_1] + parents[0][cut_1:cut_2] + [parents[1][cut_2:]]])
    child_1 = child[0][0:4]
    child_2 = child[0][4:8]
    child_1.sort()
    child_2.sort()
    child[0] = child_1 + child_2 
    child_1 = child[1][0:4]
    child_2 = child[1][4:8]
    child_1.sort()
    child_2.sort()
    child[1] = child_1 + child_2 
    return child
##############################################################################
def mutation(indv, par, args, seed, i_mut, i):
    if not any(i_mut == i): return indv
    lb1 = args['lb1']
    ub1 = args['ub1']
    lb2 = args['lb2']
    ub2 = args['ub2']
    seed1 = args['seed1']
    met = par['mut_met']
    mut_strength = par['mut_strength']
    stdev = par['mut_stdev']
    mut_indv_1 = indv[0:4]
    mut_indv_2 = indv[4:8]
    ind = rand(size=(mut_strength,), l=0, h=3, tp='int', seed=seed)
    if met == 'Gauss':
        for x in ind:
            seed=seed*x + 1
            mut_indv_1[x] = int(indv[x] + randn(m=0, s=stdev, seed=seed))
            seed = seed*x + 2
            mut_indv_2[x] = int(indv[x] + randn(m=0, s=stdev, seed=seed))
    if met == 'Reset':
        for x in ind:
            seed = seed*x + 1
            mut_indv_1[x] = rand(l=lb1, h=ub1+1, tp='int', seed=seed)[0,0]
            seed = seed*x + 2
            mut_indv_2[x] = rand(l=lb2, h=ub2+1, tp='int', seed=seed)[0,0]
    mut_indv_1.sort()
    mut_indv_2.sort()
    mut_indv = mut_indv_1 + mut_indv_2 
    return mut_indv 
##############################################################################
def nextgen(gen, par, args, itr):
    Nind = par['Nind']
    selection_met = par['select_met']
    pairing_met = par['pairing_met']
    mut_rate = par['mut_rate']
    best = {}
    next_sgen = {}
    best['individuals'] = gen['individuals'].pop(-1)
    best['F'] = gen['F'].pop(-1)
    selected = selection(gen, itr, selection_met)
    parents = pairing(best, selected, itr, met=pairing_met)
    children = [[[mating(parents[i], itr+i+j) for i in range(len(parents))]
                    [j][h] for h in range(2)]
                    for j in range(len(parents))]
    children1 = [children[i][0] for i in range(len(parents))]
    children2 = [children[i][1] for i in range(len(parents))]
    unmutated = selected['individuals'] + children1 + children2
    n = len(gen['individuals'])
    i_mut = find(rand(size=(n,), seed=itr) < mut_rate/100)
    mutated = [mutation(unmutated[i], par, args, itr*Nind+i, i_mut, i) for i in range(n)]
    indvs = mutated + [best['individuals']]
    next_gen = [func(mutated[i], par, args) for i in range(len(mutated))]
    F = [next_gen[x] for x in range(len(gen['F']))] + [best['F']]
    sorted_next_gen = sorted([[indvs[x], F[x]] for x in range(len(indvs))], key=lambda x: x[1])
    next_sgen['individuals'] = [sorted_next_gen[x][0] for x in range(len(sorted_next_gen))]
    next_sgen['F'] = [sorted_next_gen[x][1] for x in range(len(sorted_next_gen))]
    gen['individuals'].append(best['individuals'])
    gen['F'].append(best['F'])
    return next_sgen
##############################################################################
def pairing(best, selected, seed, met='Fbest'):
    indvs = [best['individuals']] + selected['individuals']
    F = [best['F']]+selected['F']
    n = len(indvs)
    if met == 'Fbest':
        parents = [[indvs[i], indvs[i+1]] for i in range(n//2)]
    if met == 'rnd':
        parents = []
        n2 = n//2
        for i in range(n2):
            seed = seed + n2 + i
            parents.append([indvs[rand(l=0, h=n-1, tp='int', seed=seed)[0,0]], indvs[rand(l=0, h=n-1, tp='int', seed=seed+n2)[0,0]]])
            br = 0
            while parents[i][0] == parents[i][1]:
                br += 1
                seed = seed + 2*n2 + i + br
                parents[i][1] = indvs[rand(l=0, h=n-1, tp='int', seed=seed)[0,0]]
    if met == 'wrnd':
        normalized_F = sorted([F[i]/sum(F) for i in range(n//2)], reverse = True)
        csum = np.array(normalized_F).cumsum()
        parents = []
        for i in range(n//2):
            parents.append([indvs[roulette(csum, rand(seed=seed+i))], indvs[roulette(csum, rand(seed=seed+n+i))]])
            j = 0
            while parents[i][0] == parents[i][1]:
                j += 1
                parents[i][1] = indvs[roulette(csum, rand(seed=seed+2*n+j))]
    return parents
##############################################################################
def population(par, args, itr):
    Nind = par['Nind']
    pop = []
    for i in range(Nind):
        args['seed1'] = (itr + i)*(args['ng1'] + args['ng2'])
        pop += [individual(args, 1)]
    return pop
##############################################################################    
def roulette(cum_sum, chance):
    cumF = list(cum_sum.copy())
    cumF.append(chance)
    cumF = sorted(cumF)
    return cumF.index(chance)
##############################################################################
def selection(gen, seed, met='Fhalf'):
    n = len(gen['individuals'])
    ns = int(np.ceil(n/2))
    if met == 'roulette':
        ind = 1-np.isinf(gen['F']) == 1
        if all(ind==0):     sF = -1 # !!!!!!!!!!!!!!!! sF = 1
        elif any(ind==0):   sF = -1 # !!!!!!!!!!!!!!!! sF = np.max(gen['F'][ind])
        else:               sF = sum(gen['F'])
        # sorted(F)
        # F1 = copy.deepcopy(F)
        # Fn = rnml(F)
        Fn = sorted([gen['F'][i]/sF for i in range(len(gen['F']))], reverse = True) # normalization of F
        cumFn = np.array(Fn).cumsum()
        selected = []
        for i in range(n//2):
            selected.append(roulette(cumFn, rand(seed=seed+i)[0,0]))
            j = 0
            while len(set(selected)) != len(selected):
                j += 1
                selected[i] = roulette(cumFn, rand(seed+n+j)[0,0])
        selected = {'individuals': [gen['individuals'][int(selected[i])] for i in range(n//2)], 
                    'F': [gen['F'][int(selected[i])] for i in range(n//2)]}
    elif met == 'Fhalf':
        selected_indvs = [gen['individuals'][-i-1] for i in range(ns)]
        Fwinners = [gen['F'][-i-1] for i in range(ns)]
        selected = {'individuals': selected_indvs, 'F': Fwinners}
    elif met == 'rnd':
        selected_indvs = [gen['individuals'][rand(l=0, h=len(gen['F'])-1, tp='int', seed=seed+i)[0,0]] for i in range(ns)]
        Fwinners = [gen['F'][rand(l=0, h=len(gen['F'])-1, tp='int', seed=seed+i)[0,0]] for i in range(ns)]
        selected = {'individuals': selected_indvs, 'F': Fwinners}
    return selected
##############################################################################
def tables(cs, data):
    from sklearn.metrics import confusion_matrix
    cutoffs_GB = [-np.inf, cs[0], cs[1], cs[2], cs[3], np.inf] 
    cutoffs_GBR = [-np.inf, cs[4], cs[5], cs[6], cs[7], np.inf]
    
    if len(set(cutoffs_GB)) != len(cutoffs_GB):
        return -np.inf 
    if len(set(cutoffs_GBR)) != len(cutoffs_GBR):
        return -np.inf 

    GB_zones = pd.cut(data['Score_GB'], cutoffs_GB, labels = False, retbins = False, right = False)
    GBR_zones = pd.cut(data['Score_GBR'], cutoffs_GBR, labels = False, retbins = False, right = False)
    
    if len (GB_zones) < 5:  print (GB_zones)
    if len (GBR_zones) < 5: print (GBR_zones)    
        
# confusion matrix
    good = confusion_matrix(GB_zones, GBR_zones, sample_weight = data['Good'].values).astype(int)
    good = np.fliplr(np.flipud(good))
    good = pd.DataFrame(good, index = ['GB_A', 'GB_LR', 'GB_MR', 'GB_HR', 'GB_R'], columns = ['GBR_A', 'GBR_LR', 'GBR_MR', 'GBR_HR', 'GBR_R'])

    bad = confusion_matrix(GB_zones, GBR_zones, sample_weight = data['Bad'].values).astype(int)
    bad = np.fliplr(np.flipud(bad))
    bad = pd.DataFrame(bad, index = ['GB_A', 'GB_LR', 'GB_MR', 'GB_HR', 'GB_R'], columns = ['GBR_A', 'GBR_LR', 'GBR_MR', 'GBR_HR', 'GBR_R'])
        
    reject = confusion_matrix(GB_zones, GBR_zones, sample_weight = data['Reject'].values).astype(int)
    reject = np.fliplr(np.flipud(reject))
    reject = pd.DataFrame(reject, index = ['GB_A', 'GB_LR', 'GB_MR', 'GB_HR', 'GB_R'], columns = ['GBR_A', 'GBR_LR', 'GBR_MR', 'GBR_HR', 'GBR_R'])

# bad rate
    bad_rate = (bad/(good + bad) * 100)
    total_gb = good + bad
    total = good + bad + reject
    return good, bad, reject, total_gb, total, bad_rate
##############################################################################
def tables2(G, B, R, TGB, TGBR, BR):
    # GB Scorecard
    G1 = np.sum(G, axis=1)
    B1 = np.sum(B, axis=1)
    R1 = np.sum(R, axis=1)
    BadRej = B1 + R1   
    TGBR1 = np.sum(TGBR, axis=1)
    TotalPrc = TGBR1/np.sum(TGBR1)*100
    BR = B1/(G1 + B1)*100
    BadAndRejectRate = BadRej/(G1 + BadRej)*100
    T1 = np.vstack((G1, B1, R1, BadRej, TGBR1, np.round(TotalPrc, 1), np.round(BR, 1), np.round(BadAndRejectRate, 1)))
    BR1 = np.sum(B1)/np.sum(G1 + B1)
    BadAndRejectRate1 = np.sum(B1 + R1)/np.sum(G1 + B1 + R1)
    Tot1 = [np.sum(np.sum(G1)), np.sum(np.sum(B1)), np.sum(np.sum(R1)), np.sum(np.sum(BadRej)), np.sum(np.sum(TGBR1)), np.sum(np.sum(TotalPrc)), BR1, BadAndRejectRate1]
    Tot = np.round(np.array([Tot1]).T, 1)
    T1 = np.hstack((T1, Tot))
    T1 = pd.DataFrame(T1, index = ['Good', 'Bad', 'Reject', 'BadAndReject', 'Total', 'TotalPrc', 'BadRate', 'BadAndRejectRate'], columns = ['Accept', 'LowRisk', 'MidRisk', 'HighRisk', 'Reject', 'Total'])
    # GBR Scorecard
    G2 = np.sum(G, axis=0)
    B2 = np.sum(B, axis=0)
    R2 = np.sum(R, axis=0)
    BadRej = B2 + R2
    TGBR2 = np.sum(TGBR, axis=0)
    TotalPrc = TGBR2/np.sum(TGBR2)*100
    BR = B2/(G2 + B2)*100
    BadAndRejectRate = BadRej/(G2 + BadRej)*100
    T2 = np.vstack((G2, B2, R2, BadRej, TGBR2, np.round(TotalPrc, 1), np.round(BR, 1), np.round(BadAndRejectRate, 1)))
    BR1 = np.sum(B2)/np.sum(G2 + B2)
    BadAndRejectRate1 = np.sum(B2 + R2)/np.sum(G2 + B2 + R2)
    Tot1 = [np.sum(np.sum(G2)), np.sum(np.sum(B2)), np.sum(np.sum(R2)), np.sum(np.sum(BadRej)), np.sum(np.sum(TGBR2)), np.sum(np.sum(TotalPrc)), BR1, BadAndRejectRate1]
    Tot = np.round(np.array([Tot1]).T, 2)
    T2 = np.hstack((T2, Tot))
    T2 = pd.DataFrame(T2, index = ['Good', 'Bad', 'Reject', 'BadAndReject', 'Total', 'TotalPrc', 'BadRate', 'BadAndRejectRate'], columns = ['Accept', 'LowRisk', 'MidRisk', 'HighRisk', 'Reject', 'Total'])
    return T1, T2
###############################################################################
