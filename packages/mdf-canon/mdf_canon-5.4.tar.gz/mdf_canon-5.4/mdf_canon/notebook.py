# -*- coding: utf-8 -*-
"""
Short demo for Notebook functionality. Targets: 
0. Print test info
1. Show an image by index
2. Show an image by T
3. Print characteristic shapes
4. Default Plot Vol/T
"""
from mdf_canon.indexer import SharedFile
from mdf_canon import reference
import numpy as np
import logging
from matplotlib import pylab
logging.getLogger().setLevel(55)
from collections import namedtuple
from scipy.interpolate import UnivariateSpline

Curve = namedtuple('Curve', ['t', 'T', 'v', 'ft', 'fT'])
Curve.__new__.__defaults__ = tuple([None] * 5)


class TimeTemperatureValue(object):
    t = None 
    T = None
    v = None
    fT = None
    ft = None

    def __init__(self, *a):
        a = list(a)
        a += [None] * 5
        self.t, self.T, self.v, self.fT, self.ft = a[:5]
    
    def cut(self, T1=None, T2=None, zero=False):
        i1, i2 = None, None
        t, T, v = self.t, self.T, self.v
        if T1 or T2:
            if T1:
                i1 = np.searchsorted(T, T1)
            if T2:
                i2 = np.searchsorted(T, T2)    
            s = slice(i1, i2)
            t = t[s]
            v = v[s]
            T = T[s]
            while 1:
                i = np.concatenate(([1], np.diff(T)))
                mask = i <= 0
                if not sum(mask):
                    break
                mask = np.invert(mask)
                t = t[mask]
                T = T[mask]
                v = v[mask]
        if zero:
            v -= v[0]
        fT, ft = None, None
        if T1 or T2:
            fT = UnivariateSpline(T, v, s=0)
            ft = UnivariateSpline(t, v, s=0)
        return TimeTemperatureValue(t, T, v, ft, fT)


    def export(self, sep=';', fmt='g'):
        out = "#time(min){0}temperature(C){0}value\n".format(sep)
        for i, t in enumerate(self.t):
            T = self.T[i]
            v = self.v[i]
            
            out += "{2:{1}}{0}{3:{1}}{0}{4:{1}}\n".format(sep,fmt, t, T, v)
        return out

    
    
def render_meta(obj):
    out = '<table>\n<tr><th>Name</th><th>Temperature</th><th>Time</th></tr>'
    keys = []
    for key, opt in obj.desc.items():
        if opt['type'] != 'Meta':
                continue
        keys.append(key)
    keys.sort()
    for key in keys:
        opt = obj.desc[key]
        m = opt['current']
        ok = True
        for k, v in m.items():
            if not isinstance(v, str):
                f = '{:.1f}'
                if k == 'time':
                    v /= 60.
                    f += ' min'
                elif k == 'temp':
                    f += ' °C'
                if k == 'value':
                    m[k] = '{:E}'.format(v)
                else:
                    m[k] = f.format(v)
            elif k == 'time' and v in ['None', None]:
                ok = False
        if not ok:
            continue
        out += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(opt['name'], m['temp'], m['time'])
    out += '</table>\n'
    return out

            
class NodeAccessor(object):
    _node = False
    route = ['get_time']

    def __init__(self, sharedfile, path='/'):
        self._sh = sharedfile
        self._path = path
        self._local = ['_sh', '_path', '_local'] + dir(self)
        
    @property 
    def node(self):
        if self._node is False:
            self._node = self._sh.test.get_node(self._path)
        return self._node
        
    def __getattr__(self, subpath):
        if subpath.startswith('_') or subpath in self._local:
            return object.__getattribute__(self, subpath)
        if subpath not in self.node:
            return object.__getattribute__(self, subpath)
        if not self._path.endswith('/'):
            s = self._path + '/' + subpath
        else: 
            s = self._path + subpath
        return NodeAccessor(self._sh, s)
    
    def __call__(self):
        p = reference.get_node_reference(self._sh, self._path)
        return p
    
    def __getitem__(self, *a, **k):
        return self().__getitem__(*a, **k)

    def values_at_time(self, t, names):
        """Returns indexes and values for `names` at time `t`"""
        idxes = []
        vals = []
        for var in names:
            p1 = getattr(self, var)()
            idx = p1.get_time(t)
            val = p1[idx]
            idxes.append(idx)
            vals.append(val)
            
        return idxes, vals
        
    def get_profile(self, idx=None, T=None, t=None):
        if not 'profile' in self.node:
            print('This node has no profile dataset')
            return False
        p = reference.get_node_reference(self._sh, self._path + '/profile')
        if T is not None:
            idx, t, val = self._sh.nearest(self._path + '/T', T)
        if t is not None:
            idx = self._sh.get_time_func(self._path + '/profile', t,
                                         func=p.unbound['decode_time'])
        if idx is not None:
            dat = p[idx]
            return dat
        print('No profile found.')
        return False
        
    def draw_profile(self, idx=None, T=None, t=None):
        dat = self.get_profile(idx=idx, T=T, t=t)
        if not dat:
            return False
        t, ((h, w), x, y) = dat
        y -= min(y)
        y = max(y) - y
        x -= min(x)
        pylab.plot(x, y)
        m = max((max(x), max(y)))
        pylab.ylim((-50, m))
        pylab.xlim((-50, m))
        pylab.show()
        return True
    
    def curve(self, T1=None, T2=None, zero=False):
        p = self._path
        if not p.startswith('/summary'):
            p = '/summary' + p
        v = self._sh.col(p)
        T = self._sh.col('/'.join(p.split('/')[:-1]) + '/T')
        if (T is None) or not len(T):
            T = self._sh.col('/summary/kiln/T')
        t = v[:, 0]
        e = min(len(T), len(v))
        t, T, v = t[:e], T[:e], v[:e]
        v -= v[0]
        d0 = 0
        try:
            d0 = self._sh.conf.instrument_obj.sample0['initialDimension']
        except:
            d0 = 1 
        if not d0: 
            d0 = 1
        v /= d0
        v *= 100
        return TimeTemperatureValue(t, T[:, 1], v[:, 1]).cut(T1, T2, zero=zero)  

                


class MdfFile(SharedFile):

    def __init__(self, *a, **k):
        SharedFile.__init__(self, *a, **k)
        self.load_conf()
        self.nb = NodeAccessor(self)
        
    @property
    def name(self):
        return self.conf.instrument_obj.measure['name']
    
    @property
    def date(self):
        return self.conf.instrument_obj.measure['date']
    
    @property
    def elapsed(self):
        return self.conf.instrument_obj.measure['elapsed'] / 60.0

    def info(self):
        """Pretty-print main test info"""
        from IPython.display import display, HTML
        ins = self.conf.instrument_obj
        out = '<h1>Name: {}</h1>\n'.format(self.name)
        out += '<h3> Started: {}, Elapsed: {:.1f} min</h3>\n'.format(self.date, self.elapsed)
        out += '<h2> Measurement metadata </h2>\n'
        out += render_meta(ins.measure)
        out += '<h2>  Sample metadata for: {} </h2>\n'.format(ins.sample0['name'])
        out += render_meta(ins.sample0)
        display(HTML(out))

