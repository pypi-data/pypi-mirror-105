######################################################################
############## Self writen ###########################################
######################################################################

import numpy as np

def combine_error(eq, sym1, value = 0, value_sd = 0, rho = 0, cov = 0):
    '''
    Function for doing law of combining errors
    
    eq: is the equation, you want to solve for made using sympy
    sym1: n-tuple, with the symbols used in the equation
    
    value: n-tuple, with the values of the variables given in sym1
    value_sd: n-tuple, with the uncertainties on the values of the variables given in sym1
    
    rho: an NxN matrix with asigning how much the values are coralated, "see Barlow page 59"
    cov: the covariance matrix given by fitting algoriths like iminuit of scipy.optimize.curve_fit
    
    CODE, HERE IS SHOW THE CODE OF VERSION 1, MAY BE UPDATED WITHOUT GETTING HERE
    
    from sympy import zeros, symbols, diff, eye, sqrt
    sigma = array(['\sigma_{'+str(sym1[i])+'}, ' for i in range(len(sym1))])
    unc_str = ''
    for f in sigma: unc_str+=f
    sym2 = symbols(unc_str)
    n = len(sym1)
    if len(sym1) != len(sym2):
        raise NameError("Lenght of sym1 and sym2 must match")
    M1 = zeros(1, n)
    M2 = zeros(n, 1)
    if np.shape(cov) == ():
        for i in range(n):
            M1[i] = eq.diff(sym1[i])
            M2[i] = sym2[i]
        if np.shape(rho) == ():
            rho = eye(n)
        M = M2 * M2.T
        for i in range(n**2):
            M[i] = rho[i] * M[i]
        eq_unc = sqrt((M1 * M * M1.T)[0, 0])
    else:
        for i in range(n):
            M1[i] = eq.diff(sym1[i])
        eq_unc = sqrt((M1 * cov * M1.T)[0, 0])
        value_sd = sqrt(np.diag(cov))
    if np.shape(value) == ():
        return eq_unc
    elif np.shape(value_sd) == () and np.shape(value) != ():
        return eq.subs(zip(sym1, value)), eq_unc.subs(zip(sym1, value))
    else:
        return eq.subs(zip(sym1, value)), eq_unc.subs(zip(sym1 + sym2, (*value, *value_sd)))
    END
    
    '''
    from sympy import zeros, symbols, diff, eye, sqrt
    sigma = np.array(['\sigma_{'+str(sym1[i])+'}, ' for i in range(len(sym1))])
    unc_str = ''
    for f in sigma: unc_str+=f
    sym2 = symbols(unc_str)
    n = len(sym1)
    M1 = zeros(1, n)
    M2 = zeros(n, 1)
    if np.shape(cov) == ():
        for i in range(n):
            M1[i] = eq.diff(sym1[i])
            M2[i] = sym2[i]
        if np.shape(rho) == ():
            rho = eye(n)
        M = M2 * M2.T
        for i in range(n**2):
            M[i] = rho[i] * M[i]
        eq_unc = sqrt((M1 * M * M1.T)[0, 0])
    else:
        for i in range(n):
            M1[i] = eq.diff(sym1[i])
        eq_unc = sqrt((M1 * cov * M1.T)[0, 0])
        value_sd = sqrt(np.diag(cov))
    if np.shape(value) == ():
        return eq_unc
    elif np.shape(value_sd) == () and np.shape(value) != ():
        return eq.subs(zip(sym1, value)), eq_unc.subs(zip(sym1, value))
    else:
        return eq.subs(zip(sym1, value)), eq_unc.subs(zip(sym1 + sym2, (*value, *value_sd)))
    


def gauss(x,mu,sigma,N): return N/(sqrt(2*pi)*sigma)*exp(-(x-mu)** 2/(2*sigma**2))

def linear(x,a,b): return a*x+b



def BinnedChi2Fit(func, x, y, bin_width, sy = 1, minuit = False, print_level = 0, **params):
    '''
    DOES NOT WORK with lambda functions
    
    from iminuit.cost import LeastSquares
    from iminuit import Minuit
    _func = func.__code__.co_name
    _number_args = func.__code__.co_argcount
    _lambda_string = ('_f=lambda ' + _number_args*'{},' + ': bin_width*({}(' + _number_args*'{},'
                      + '))').format(*func.__code__.co_varnames, _func, *func.__code__.co_varnames)
    print(_lambda_string)
    var = locals()
    exec(_lambda_string, globals(), var)
    _f = var['_f']
    _chi2 = LeastSquares(x, y, sy, _f)
    _min_chi2 = Minuit(_chi2, **params)
    _min_chi2.errordef = 1
    _min_chi2.print_level = print_level
    if minuit:
        return _min_chi2,_f
    _min_chi2.migrad()
    return _min_chi2.values, _min_chi2.errors,_f
    '''
    from iminuit.cost import LeastSquares
    from iminuit import Minuit
    _func = func.__code__.co_name
    _number_args = func.__code__.co_argcount
    _lambda_string = ('_f=lambda ' + _number_args*'{},' + ': bin_width*({}(' + _number_args*'{},'
                      + '))').format(*func.__code__.co_varnames, _func, *func.__code__.co_varnames)
    print(_lambda_string)
    var = locals()
    exec(_lambda_string, globals(), var)
    _f = var['_f']
    _chi2 = LeastSquares(x, y, sy, _f)
    _min_chi2 = Minuit(_chi2, **params)
    _min_chi2.errordef = 1
    _min_chi2.print_level = print_level
    if minuit:
        return _min_chi2,_f
    _min_chi2.migrad()
    return _min_chi2.values, _min_chi2.errors,_f



def Chi2Fit(f,x,y,sy=1,minuit=False,print_level=0,**params):
    '''
    from iminuit.cost import LeastSquares
    from iminuit import Minuit
    _chi2 = LeastSquares(x,y,sy,f)
    _min_chi2 = Minuit(_chi2,**params)
    _min_chi2.errordef = 1
    _min_chi2.print_level = print_level
    if minuit:
        return _min_chi2
    _min_chi2.migrad()
    return _min_chi2.values, _min_chi2.errors
    
    
    
    '''
    from iminuit.cost import LeastSquares
    from iminuit import Minuit
    _chi2 = LeastSquares(x,y,sy,f)
    _min_chi2 = Minuit(_chi2,**params)
    _min_chi2.errordef = 1
    _min_chi2.print_level = print_level
    if minuit:
        return _min_chi2
    _min_chi2.migrad()
    return _min_chi2.values, _min_chi2.errors


def zoom_axis(ax, xlim = (0, 1), ylim = (0, 1), pos = [0.5, 0.5, 0.47, 0.47]):
    '''
    _ax_inset = ax.inset_axes(pos)
    _ax_inset.set_xlim(*xlim)
    _ax_inset.set_ylim(*ylim)
    ax.indicate_inset_zoom(_ax_inset)
    return _ax_inset
    
    '''
    _ax_inset = ax.inset_axes(pos)
    _ax_inset.set_xlim(*xlim)
    _ax_inset.set_ylim(*ylim)
    ax.indicate_inset_zoom(_ax_inset)
    return _ax_inset


def hist_plot(data,
              bins = 'auto',
              std = True,
              capsize = 2,
              label_hist = 'Histogram',
              label_plot = 'unc'):
    '''
    import matplotlib.pyplot as plt
    _fig, _ax = plt.subplots()
    _count, _edges, _line = _ax.hist(data, bins = bins, label = label_hist, histtype = 'step')
    _x = ((_edges[1:] + _edges[:-1]) / 2)[_count > 0]
    _y = _count[_count > 0]
    _stdy = np.sqrt(_y)
    _stdx = ((_edges[1:] - _edges[:-1]) / 2)[_count > 0]
    if std:
        _ax.errorbar(_x, _y, xerr = _stdx, yerr = _stdy, fmt = 'r.', capsize = 1, label = label_plot)
    else:
        _ax.plot(_x, _y, '.', label = label_plot)
    return (_fig, _ax), (_x, _y, _stdx, _stdy)
    '''
    import matplotlib.pyplot as plt
    _fig, _ax = plt.subplots()
    _count, _edges, _line = _ax.hist(data, bins = bins, label = label_hist, histtype = 'step')
    _x = ((_edges[1:] + _edges[:-1]) / 2)[_count > 0]
    _y = _count[_count > 0]
    _stdy = np.sqrt(_y)
    _stdx = ((_edges[1:] - _edges[:-1]) / 2)[_count > 0]
    if std:
        _ax.errorbar(_x, _y, xerr = _stdx, yerr = _stdy, fmt = 'r.', capsize = 1, label = label_plot)
    else:
        _ax.plot(_x, _y, '.', label = label_plot)
    return (_fig, _ax), (_x, _y, _stdx, _stdy)

def LD(arr1, arr2, ddof = 1):
    '''
    cov_inv = np.linalg.inv(np.cov(arr1, ddof = ddof) + np.cov(arr2, ddof = ddof))
    mu1 = np.mean(arr1, axis = 1)
    mu2 = np.mean(arr2, axis = 1)
    wf = np.matmul(cov_inv, mu1 - mu2)
    return wf
    '''
    cov_inv = np.linalg.inv(np.cov(arr1, ddof = ddof) + np.cov(arr2, ddof = ddof))
    mu1 = np.mean(arr1, axis = 1)
    mu2 = np.mean(arr2, axis = 1)
    wf = np.matmul(cov_inv, mu1 - mu2)
    return wf

def fisher(arr1,arr2,c=0,**kwargs):
    '''
    _wf = LD(arr1,arr2,**kwargs)
    _fisher_data_A = 0
    _fisher_data_B = 0
    for i in range(len(wf)):
        _fisher_data_A += _wf[i] * arr1[i] + c
        _fisher_data_B += _wf[i] * arr2[i] + c
    return fisher_data_A, fisher_data_B
    '''
    _wf = LD(arr1,arr2,**kwargs)
    _fisher_data_A = 0
    _fisher_data_B = 0
    for i in range(len(wf)):
        _fisher_data_A += _wf[i] * arr1[i] + c
        _fisher_data_B += _wf[i] * arr2[i] + c
    return fisher_data_A, fisher_data_B


def error(arr1, arr2, point = 0, pos = 1):
    '''
    if np.shape(point)!=():
        return (np.sum(np.greater(arr1,point),axis=1) / len(arr1), np.sum(np.less(arr2,point),axis=1) / len(arr2))[::pos]
    return (np.sum(np.greater(arr1,point)) / len(arr1), np.sum(np.less(arr2,point)) / len(arr2))[::pos]
    '''
    if np.shape(point)!=():
        return (np.sum(np.greater(arr1,point),axis=1) / len(arr1), np.sum(np.less(arr2,point),axis=1) / len(arr2))[::pos]
    return (np.sum(np.greater(arr1,point)) / len(arr1), np.sum(np.less(arr2,point)) / len(arr2))[::pos]

def truevalue(arr1, arr2, point = 0, pos = 1):
    '''
    if np.shape(point)!=():
        return (np.sum(np.less_equal(arr1,point),axis=1) / len(arr1), np.sum(np.greater_equal(arr2,point),axis=1) / len(arr2))[::pos]
    return (np.sum(np.less_equal(arr1,point)) / len(arr1), np.sum(np.greater_equal(arr2,point)) / len(arr2))[::pos]
    '''
    if np.shape(point)!=():
        return (np.sum(np.less_equal(arr1,point),axis=1) / len(arr1), np.sum(np.greater_equal(arr2,point),axis=1) / len(arr2))[::pos]
    return (np.sum(np.less_equal(arr1,point)) / len(arr1), np.sum(np.greater_equal(arr2,point)) / len(arr2))[::pos]


def ROC(arr1, arr2, res = 10000, pos = 1):
    '''
    point = np.repeat(np.linspace(min(x),max(y),res)[:,np.newaxis],len(x),axis=1)
    FN, FP = error(arr1, arr2, point = point, pos = 1)
    TP, TN = truevalue(arr1, arr2, point = point, pos = 1)
    TPR = (TP / (TP+FN))
    FPR = (FP / (FP+TN))
    return FPR, TPR
    '''
    point = np.repeat(np.linspace(min(x),max(y),res)[:,np.newaxis],len(x),axis=1)
    FN, FP = error(arr1, arr2, point = point, pos = 1)
    TP, TN = truevalue(arr1, arr2, point = point, pos = 1)
    TPR = (TP / (TP+FN))
    FPR = (FP / (FP+TN))
    return FPR, TPR





### MAKE IT COMPLETE ###