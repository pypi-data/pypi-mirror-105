#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
API for common data operations on local or remote HDF files.
"""

from scipy.interpolate import UnivariateSpline, interp1d
import numpy as np
import functools
import numexpr as ne
from .. import csutil
from ..csutil import lockme
from .. import reference
ne.set_num_threads(8)


class DataOperator(object):
    _zerotime = -1

    @property
    def zerotime(self):
        """Time at which the acquisition stats.
No data will be evaluate if older than zerotime."""
        if self.test is False:
            return 0
        if self._zerotime < 0:
            self.log.debug('ask zerotime')
            if not self.has_node('/conf'):
                self.log.warning('NO CONF NODE')
                return 0
            self._zerotime = self.get_node_attr('/conf', 'zerotime')
        return self._zerotime

    def get_zerotime(self):
        return self.zerotime

    def _xy(self, path=False, arr=False):
        """limit: limiting slice"""
        path = self._versioned(path)
        x = False
        node = False
        if path is not False:
            arr = self._get_node(path)
            y = arr.cols.v
            n = len(y)
            # FixedTimeArray
            if 't' in arr.cols._v_colnames:
                x = arr.cols.t
            else:
                x = arr._v_attrs.t0+arr._v_attrs.dt*np.arange(n)
        else:
            x = arr[:, 0]
            y = arr[:, 1]
            n = len(y)
        if n == 0:
            self.log.info('Empty dataset', path)
            return False, False
        if x is False:
            return False, False
        return x, y

    @lockme()
    def col(self, path, idx_or_slice=None, raw=False):
        """Reads an array in the requested slice. If an integer index is specified, reads just one point."""
        path = self._versioned(path)
        n = self._get_node(path)
        if idx_or_slice is None:
            idx_or_slice = [None,None,None]
        slc = csutil.toslice(idx_or_slice)
        n1 = n[slc]
        if raw:
            return n1
        # Convert to regular array
        ret = np.array([])
        if len(n1):
            # Just one element
            if (not n1.shape) or n1.shape[0]==1:
                ret = np.array(list(n1))
            else:
                try:
                    ret = n1.view(np.float64).reshape(n1.shape + (-1,))
                except:
                    raise
        # FixedTimeArray
        if ret.shape[-1]==1 and hasattr(n._v_attrs,'t0'):
            if len(ret.shape)==2:
                ret = ret[:,0]
            t = n._v_attrs.t0+n._v_attrs.dt*np.arange(len(n))
            t = t[slc].reshape(ret.shape)
            ret = np.stack((t, ret), axis=-1)
            if len(ret)==1:
                ret = ret[0]
        return ret
    
    @lockme()
    def col_length(self, path):
        path = self._versioned(path)
        n = self._get_node(path)
        return len(n)      

    def _col_at(self, path, idx, raw=False):
        """Retrive single index `idx` from node `path`"""
        if hasattr(idx,'__iter__'):
            r = [self._col_at(path, ii, raw=raw) for ii in idx]
            return r
        path = self._versioned(path)
        node = self._get_node(path)
        idx = int(idx)
        if idx>len(node)-1:
            self.log.error('Non-existent idx', path, idx)
            return None
        n = node[idx]
        if not raw:
            n = np.array(list(n))
        # FixedTimeArray
        if len(n.shape)==1 and n.shape[0]==1:
            t = node._v_attrs.t0 + idx*node._v_attrs.dt
            n = np.array([t,n[0]])
        return n

    @lockme()
    def col_at(self, *a, **k):
        """Retrive single index `idx` from node `path`, locked"""
        return self._col_at(*a, **k)
    
    def _col_at_time(self, path, t, raw=False):
        if hasattr(t,'__iter__'):
            self.log('_col_at_time iterating', path, t)
            r = [self._col_at_time(path, ti, raw=raw) for ti in t]
            return r
        idx = self._get_time(path, t)
        return self._col_at(path, idx, raw=raw)
    
    @lockme()
    def col_at_time(self, *a, **k):
        """Retrive single time `t` from node `path`, locked"""
        return self._col_at_time(*a, **k)        

    def clean_start(self, g, start):
        # FIXME: Cut start limit. Send bug to pytables
        while len(g) > 0:
            if g[0] < start:
                g.pop(0)
                continue
            break
        return g

    def find_nearest_cond(self, tab, path, s, f=2., start_time=0, end_time=np.inf):
        """Search for the nearest value to `s` in table `tab`,
        by iteratively reducing the tolerance by a factor of `f`."""
        start_index = self._get_time(path, start_time)
        end_index = self._get_time(path, end_time)
        # Try exact term
        g = tab.get_where_list('v==s', stop=end_index)
        g = self.clean_start(g, start_index)
        if len(g) > 0:
            return g[0]

        ur = max(tab.cols.v) - s  # initial upper range
        lr = s - min(tab.cols.v)  # initial lower range
        last = None

        while True:
            # Tighten upper/lower ranges
            ur /= f
            lr /= f
            g = tab.get_where_list('((s-lr)<v) & (v<(s+ur))', stop=end_index)
            # Found!
            if g is None or len(g) == 0:
                if last is None:
                    return None
                return last[0]
            # FIXME: Cut start limit
            while True:
                if len(g) == 0:
                    if last is None:
                        return None
                    return last[0]
                if g[0] < start_index:
                    g.pop(0)
                    continue
                break
            # Save for next iter
            last = g
            if ur + lr < 0.0000000001:
                return None
            
    def _start_end_indexes(self, path0, start_time, end_time):
        path = self._versioned(path0)
        tab = self._get_node(path)
        y = tab.cols.v
        if not len(y):
            self.log.debug('Empty column', path, path0)
            return False
        
        if 't' in tab.cols._v_colnames:
            x = tab.cols.t
        else:
            x = tab._v_attrs.t0 + np.arange(len(y))*tab._v_attrs.dt
                
        if start_time == 0:
            start_index = 0
        else:
            start_index = csutil.find_nearest_val(x, start_time)
        if end_time == -1:
            end_index = len(y) - 1
        else:
            end_index = csutil.find_nearest_val(x, end_time)
        if start_index >= end_index - 1:
            self.log.debug('Selected an empty range', start_index, end_index)
            return False
        return tab, x, y, path, start_index, end_index

    @lockme()
    def search(self, path0, op, cond='x==y', pos=-1, start_time=0, end_time=-1, step=1):
        """Search dataset path with operator `op` for condition `cond`"""
        self.log.debug('searching in ', path0, cond, start_time, end_time, step)
        r = self._start_end_indexes(path0, start_time, end_time)
        if not r:
            return False
        tab, x, y, path, start_index, end_index = r
        y1, m = op(y)
        last = -1
        # Handle special cases
        if cond == 'x>y':  # raises
            if step > 0 and y[start_index] > m:
                last = start_index
            elif step < 0 and y[end_index] > m:
                last = end_index
            cond = 'y>m'
        elif cond == 'x<y':  # drops
            if step > 0 and y[start_index] < m:
                last = start_index
            elif step < 0 and y[end_index] < m:
                last = end_index    
            cond = 'y<m'
        elif cond == 'x~y':
            # FIXME: inefficient, restore find_nearest_cond!
            y1, m = op(y[start_index:end_index])
            d = abs(y1 - m)
            last = np.where(d == min(d))[0][0]
            # last = self.find_nearest_cond(
            #    tab, path, m, start_time=start_time, end_time=end_time)
            if last is None:
                return False
            last += start_index
        else:
            cond = 'y==m'
            
        if last < 0:
            
            condvars = {'y':y, 'm': m}
            kw = {'condvars': condvars, 'step': abs(step),
                  'start': start_index, 'stop': end_index}
            last = list(tab.get_where_list(cond, **kw))
            last0 = last[:]
            # WARNING: start selector is not working.
            # TODO: Send bug to pytables!
            while start_index:
                if len(last) == 0:
                    last = None
                    break
                if last[0] < start_index:
                    last.pop(0)
                    continue
                break
            if last is None or len(last) == 0:
                self.log.debug('DataOps.search FAILED', path, cond, start_index, end_index, m, len(y), last0, last)
                return False
            if step > 0:
                last = last[0]
            else:
                last = last[-1]
        return last, x[last], y[last]
    
    @lockme()
    def max(self, path0, start_time=0, end_time=-1):
        r = self._start_end_indexes(path0, start_time, end_time)
        if not r:
            return False
        tab, x, y, path, start_index, end_index = r
        y1 = y[start_index:end_index] 
        i = np.where(y1==max(y1))[0][0]
        last = start_index+i
        return last, x[last], y[last]
    
    @lockme()
    def min(self, path0, start_time=0, end_time=-1):
        r = self._start_end_indexes(path0, start_time, end_time)
        if not r:
            return False
        tab, x, y, path, start_index, end_index = r
        y1 = y[start_index:end_index] 
        i = np.where(y1==min(y1))[0][0]
        last = start_index+i
        return last, x[last], y[last]
    
    def nearest(self, path, val, start_time=0, end_time=-1):
        op = lambda y: (y, val)
        return self.search(path, op, cond='x~y',
                           start_time=start_time,
                           end_time=end_time)

    def equals(self, path, val, tol=10 ** -12, start_time=0, end_time=-1):
        op = lambda y: (y, val)
        r = self.search(path, op,
                           start_time=start_time,
                           end_time=end_time)
        if not r:
            return False
        i, xi, yi = r
        if abs(yi - val) > tol:
            return False
        return i, xi, yi

    def drops(self, path, val, start_time=0, end_time=-1, step=1):
        cond = 'x<y'
        op = lambda y: (y, val)
        self.log.debug('drops', path, val)
        return self.search(path, op, cond, pos=0, start_time=start_time,
                           end_time=end_time, step=step)

    def rises(self, path, val, start_time=0, end_time=-1, step=1):
        cond = 'x>y'
        op = lambda y: (y, val)
        self.log.debug('rises', path, val)
        return self.search(path, op, cond, pos=0,
                           start_time=start_time,
                           end_time=end_time,
                           step=step)
    
        
        
    
    def _time_at(self, path, idx, decode_func):
        if hasattr(idx,'__iter__'):
            r = [self._time_at(path, ii, decode_func) for ii in idx]
            return r
        path = self._versioned(path)        
        tab = self._get_node(path)
        if 't0' in tab._v_attrs and 'dt' in tab._v_attrs:
            x = tab._v_attrs.t0 + idx*tab._v_attrs.dt
        else: # FixedTimeArray
            x = decode_func(tab, idx)
        return x
    
    @lockme()
    def time_at(self, *a, **kw):
        return self._time_at(*a, **kw)
        
    def _time_getter(self, node):
        if "_reference_class" not in node._v_attrs:
            return False
        rc = node._v_attrs._reference_class
        if rc in ("Profile", b"Profile"):
            return reference.Profile.unbound['decode_time']
        if rc in ("CumulativeProfile", b"CumulativeProfile"):
            return reference.CumulativeProfile.unbound['decode_time']
        if rc in ("Image", b"Image"):
            return  reference.Image.unbound['decode_time']
        return False
    
    def _get_time(self, path, t, get=False, seed=None):
        """Optimized search of the nearest index to time `t` using the getter function `get` and starting from `seed` index."""
        if hasattr(t,'__iter__'):
            r = [self._get_time(path, ti, get=get, seed=seed) for ti in t]
            return r
        path = self._versioned(path)
        tab = self._get_node(path)
        if not get:
            get = self._time_getter(tab)
        # FixedTimeArray
        if 't0' in tab._v_attrs and 'dt' in tab._v_attrs:
            idx = (t-tab._v_attrs.t0)/tab._v_attrs.dt
            n = len(tab)
            if idx>n:
                idx = n
            return idx
            
        if get is False:
            get = lambda i: tab[i][0]
        else:
            get = functools.partial(get, tab)
        idx = csutil.find_nearest_val(tab, t, get=get, seed=seed)
        return idx

    @lockme()
    def get_time(self, *a, **k):
        return self._get_time(*a, **k)

    @lockme()
    def get_time_profile(self, path, t):
        return self._get_time(path, t, get=reference.Profile.unbound['decode_time'])
    
    @lockme()
    def get_time_cumulative_profile(self, path, t):
        return self._get_time(path, t, get=reference.CumulativeProfile.unbound['decode_time'])
    
    @lockme()
    def get_time_func(self, path, t, func):
        return self._get_time(path, t, get=func)   

    @lockme()
    def get_time_image(self, path, t):
        return self._get_time(path, t, get=reference.Image.unbound['decode_time'])

    @lockme()
    def spline_col(self, path=False, startIdx=0, endIdx=-1, time_sequence=[0], arr=False, k=3):
        """Returns a 1D interpolated version of the array, as per """
        x, y = self._xy(path, arr)
        if x is False:
            return False
        self.log.debug('building spline', path)
        f = UnivariateSpline(x, y, k=k)
        self.log.debug('interp')
        r = f(time_sequence)
        return r

    @lockme()
    def interpolated_col(self, path=False, startIdx=0, endIdx=None, time_sequence=[0], arr=False, kind='cubic'):
        x, y = self._xy(path, arr)
        if x is False:
            return False
        if startIdx == endIdx == -1:
            # Detect from time_sequence
            startIdx = self._get_time(path, time_sequence[0] - 1)
            endIdx = self._get_time(path, time_sequence[-1] + 1, seed=startIdx)
        s = slice(startIdx, endIdx)
        self.log.debug('Interpolating ', path, s)
        f = interp1d(x[s], y[s], kind=kind, bounds_error=False, fill_value=0)
        self.log.debug('interp')
        r = f(time_sequence)
        return r
