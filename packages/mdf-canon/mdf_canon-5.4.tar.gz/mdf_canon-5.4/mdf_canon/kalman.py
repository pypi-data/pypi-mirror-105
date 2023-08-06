# -*- coding: utf-8 -*-
"""Basic Kalman filtering utility"""

# https://scipy-cookbook.readthedocs.io/items/KalmanFiltering.html
def update(xminus, Pminus, xplus, R, Q=0):
    """xminus,Pminus, previous value and variance
    xplus, Pplus, current value and variance
    Q, process variance
    R, variance estimate"""
    Pminus += Q or (R/10.)
    K = Pminus/(Pminus+R)
    x = xminus + K*(xplus-xminus)
    P = (1-K)*Pminus
    return [x, P]



def update_dict(old_res, old_var, new_res, new_var):
    out_res = {}
    out_var = {}
    for k in new_var.keys():
        if k not in new_res:
            continue
        if k not in old_var:
            old_var[k] = new_var[k]*10
        if k not in old_res:
            out_res[k] = new_res[k]
            old_res[k] = new_res[k]
            continue
        nr, nv = update(old_res[k], old_var[k], new_res[k], new_var[k])
        out_res[k], out_var[k] = nr, nv
    return out_res, out_var
    
    
    
    
