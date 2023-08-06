#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Unified multi-variable stepping"""
from .logger import get_module_logging
logging = get_module_logging(__name__)
from .csutil import find_nearest_val
import numpy as np

#TODO: *Accessor cache?

class ReferenceTimeAccessor(object):

    def __init__(self, ref):
        """Return time at index of `ref`""" 
        self.ref = ref
        
        
    def __len__(self):
        return len(self.ref)
    
    def max(self):
        return self.ref.time_at(-1)
    
    def min(self):
        return self.ref.time_at(0)
        
    def __getitem__(self, s):
        if isinstance(s, slice):
            s = [s.start or 0, s.stop or len(self), s.step or 1]
            return [self[i] for i in range(*s)]
        return self.ref.time_at(s)


class ForeignTimeValueAccessor(object):

    def __init__(self, t0,  # main 
                 t1, v1):  # foreign
        """When indexed, return value (t1,v1) corresponding to the time index on t0"""
        self.t0 = t0  # eg: frame time
        self.t1 = t1  # T time
        self.v1 = v1  # return T value
        
    def __len__(self):
        return len(self.t0)
    
    def max(self):
        return max(self.v1)
    
    def min(self):
        return min(self.v1)
        
    def __getitem__(self, s):
        """Get main time for index 0, calc nearest foreign value, get nearest foreign """
        if isinstance(s, slice):
            s = [s.start or 0, s.stop or len(self.t0), s.step or 1]
            return [self[i] for i in range(*s)]
        t = self.t0[s]
        i = find_nearest_val(self.t1, t, seed=s)
        return self.v1[i]
        

def my_min(*g):
    if len(g) > 1:
        return min(g)
    g = g[0]
    if hasattr(g, 'min'):
        return g.min()
    return min(g)

    
def my_max(*g):
    if len(g) > 1:
        return max(g)
    g = g[0]
    if hasattr(g, 'max'):
        return g.max()
    return max(g)            

# All variables must be in the same unit. Only one delta required.


def stepping(variables, delta=0, start=None):
    """Calculate indexes for `variables` iterables which result in `deltas` stepping,
    starting from minimum values `starts`"""
    assert delta>=0,'Delta must be positive'
    nv = len(variables)
    vmax = max([my_max(v) for v in variables])
    vmin = min([my_min(v) for v in variables])
    vlen = np.array([len(v) for v in variables])
    vend = vlen - 1
    indexes = [0] * nv
    values = [None] * nv
    
    while True:
        start_values = values[:]
        start_indexes = indexes[:]
        
        for i, v in enumerate(variables):
            if start is not None:
                # TODO: what if some variables are not monotonic?
                j = find_nearest_val(v, start, 
                                     start=start_indexes[i], 
                                     seed=start_indexes[i])
            else:
                j = 0
            start_indexes[i] = j
            start_values[i] = v[j]
            
        # Effective start is the biggest of all starts
        start = max(start_values)
        
        indexes = []
        values = []
        for i, v in enumerate(variables):
            if start_values[i] == start:
                indexes.append(start_indexes[i])
                values.append(start_values[i])
                print('found', i, start, start_values[i], start_indexes[i])
                continue
            j = find_nearest_val(v, start, 
                                 start=start_indexes[i],
                                 seed=start_indexes[i])
            indexes.append(j)
            values.append(v[j])
            print('searched',i, start, start_values[i], start_indexes[i])
        
        # Found new row
        print('row', indexes, values)
        yield indexes
        # Prepare next row
        
        # Search the maximum common delta between the minimum index change
        next_idx, next_values = indexes, values
        broken = False
        _delta = 0
        while _delta == 0:
            if np.any(next_idx >= vend):
                logging.debug('Reached end of at least one variable', indexes, vend)
                broken = True
                break
            next_idx = [i + 1 for i in next_idx]
            next_values = [v[next_idx[i]] for i, v in enumerate(variables)]
            deltas = [next_values[i] - values[i] for i in range(nv)]
            # Search the maximum absolute change
            a_deltas = [abs(d) for d in deltas]
            mi = a_deltas.index(max(a_deltas))
            _delta = deltas[mi]
            print('scan', next_idx, next_values, values, deltas, _delta)
            
        if broken:
            break
        
        if delta > abs(_delta):
            _delta = np.sign(_delta) * delta
            
        # Calculate new starting point
        if _delta > 0:
            start = max(values)
        else:
            start = min(values)
            
        start += _delta
        
        if start > vmax:
            logging.debug('Search exceeding max value', start, vmax)
            break
        if start < vmin:
            logging.debug('Search exceeding min value', start, vmin)
            break
        indexes = next_idx
        values = next_values
        print('next start', start, indexes,  values, _delta, deltas)
    
    
