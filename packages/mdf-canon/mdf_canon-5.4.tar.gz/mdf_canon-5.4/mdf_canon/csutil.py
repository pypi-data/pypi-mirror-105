# -*- coding: utf-8 -*-
"""Common utilities between client and server"""
import os
import sys
import multiprocessing
import numpy as np
import functools
import collections
import subprocess
from traceback import format_exc, print_exc
import inspect
from operator import itemgetter
import ssl
py = sys.version_info[0]

enc_options = {}

import zlib
import base64
def gzdeflate(s, b64=False):
    if type(s)!=bytes:
        s = bytes(s, encoding='utf-8')
    compressed_data = zlib.compress(s) #[2:-4]
    if not b64:
        return compressed_data
    return base64.b64encode(compressed_data)

def gzinflate(s, b64=False):
    if b64:
        s = base64.b64decode(s)
    return zlib.decompress(s)

def unicode_func(value, *a, **k):
    if not isinstance(value, bytes):
        return value
    enc = k.pop('encoding', False)
    if not enc and len(a):
        a = list(a)
        enc = a.pop(0)
    if not enc:
        enc = 'utf8'
    return value.decode(enc, *a, **k)


def unicode_func2(value, *a, **k):
    if isinstance(value, unicode):
        return value
    return unicode(value, *a, **k)


def is_unicode3(s):
    return isinstance(s, str)


def is_unicode2(s):
    return isinstance(s, unicode)


def unicode_decode(msg, encoding='utf-8', errors='replace'):
    """python3"""
    if isinstance(msg, str):
        return msg
    else:
        return msg.decode(encoding, errors=errors)

    
def unicode_encode(msg, encoding='utf-8', errors='ignore'):
    if is_unicode(msg):
        return msg.encode(encoding, errors=errors)
    return msg
    

def py2_bytes(s, *a, **k):
    return str(s)


def go(cmd):
    """commands.getstatusoutput clone"""
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        if py == 3:
            output = output.decode()
        return 0, output
    except subprocess.CalledProcessError as cpe:
        output = cpe.output
        if py == 3:
            output = output.decode()
        return cpe.returncode, output


def mdf_opener3(uri, user, passwd, realm=b'MISURA'):
    ctx = ssl._create_unverified_context()
    https = HTTPSHandler(context=ctx)
    auth_handler = HTTPDigestAuthHandler(HTTPPasswordMgrWithPriorAuth())
    auth_handler.add_password(realm=realm, uri=uri, user=user, passwd=passwd)
    opener = build_opener(https, auth_handler)
    return opener


def mdf_opener2(uri, user, passwd, realm=b'MISURA'):
    ctx = ssl._create_unverified_context()
    https = HTTPSHandler(context=ctx)
    auth_handler = HTTPBasicAuthHandler()
    auth_handler.add_password(realm=realm, uri=uri, user=user, passwd=passwd)
    opener = build_opener(https, auth_handler)
    return opener


# PY2
#print('Running python', sys.version_info)
if py < 3:
    from urllib2 import urlopen, build_opener, install_opener, HTTPBasicAuthHandler, HTTPSHandler, URLError
    import httplib
    from urllib import quote, unquote, urlencode
    import cPickle as pickle
    import xmlrpclib
    from cPickle import dump, dumps, loads
    from cStringIO import StringIO
    from io import BytesIO
    import ConfigParser as configparser
    pickle.DEFAULT_PROTOCOL = 2
    DEFAULT_PROTOCOL = 2
    import exceptions
    unicode_func = unicode_func2
    unicode = unicode
    basestring = basestring
    bytes = py2_bytes
    walk = os.path.walk
    is_unicode = is_unicode2
    mdf_opener = mdf_opener2
# PY3
else:
    from urllib.request import urlopen, URLError, build_opener, install_opener, HTTPBasicAuthHandler, HTTPSHandler, quote, unquote, HTTPDigestAuthHandler, HTTPPasswordMgrWithPriorAuth
    import http.client as httplib
    from urllib.parse import urlencode
    from io import StringIO, BytesIO
    import builtins as exceptions
    import pickle
    import configparser
    DEFAULT_PROTOCOL = 2
    pickle.DEFAULT_PROTOCOL = DEFAULT_PROTOCOL
    from pickle import dump, dumps, loads
    from xmlrpc import client as xmlrpclib
    BaseException = BaseException
    unicode = str
    enc_options['encoding'] = 'utf-8' 
    enc_options['errors'] = 'ignore'
    basestring = str
    bytes = bytes
    walk = os.walk
    is_unicode = is_unicode3
    mdf_opener = mdf_opener3
    
rename_table = {
    'misura.canon': 'mdf_canon',
    }
    
    
class RenameUnpickler(pickle.Unpickler):

    # https://stackoverflow.com/a/53327348/1645874
    def find_class(self, module, name):
        for k in rename_table:
            if module.startswith(k):
                module = rename_table[k] + module[len(k):]
        return super(RenameUnpickler, self).find_class(module, name)


def load_compat(file_obj, **opt):
    return RenameUnpickler(file_obj, **opt).load()


def loads_compat(tree, **opt):
    file_obj = BytesIO(tree)
    return load_compat(file_obj, **opt)


profiling = True
isWindows = os.name == 'nt'
if isWindows:
    import psutil
else:
    psutil = False
#############
# TIME SCALING (testing)
# ##
import time as standardTime
time_scaled = multiprocessing.Value('i')
time_scaled.value = 0
time_factor = multiprocessing.Value('d')
time_factor.value = 1.0


def time():
    """If time_scaled is set, return current simulation-scaled time."""
    if time_scaled.value == 1:
        return time_step() * time_factor.value * 1.
    return float(standardTime.time())


utime = time


def sleep(t):
    return standardTime.sleep(t)


sh_time_step = multiprocessing.Value('i')


def time_step(set=-1):
    if set < 0:
        return sh_time_step.value
    else:
        sh_time_step.value = set
        return set


def doTimeStep(set=-1):
    t = time_step()
    if set >= 0:
        time_step(set=set)
    else:
        t += 1
        time_step(set=t)
    return t


def limit_freq(t, t1, maxfreq):
    if t1 < 0:
        t1 = time()
    t = (1. / maxfreq) - (t1 - t)
    t = min(t, 10)  # Minimum freq is 0.1!
    s = 0
    if t > 0:
        s = 0.99 * t
        sleep(s)
    return s


def camelcase(name):
    name = name.split('_')
    if len(name) == 1:
        return name[0]
    for i in range(1, len(name)):
        name[i] = name[i].capitalize()
    return ''.join(name)


class Void(object):
    pass


class FakeBinary(object):

    """Fake the xmlrpc.Binary behavior when not needing the overhead"""

    def __init__(self, data=''):
        self.data = data


binfunc = FakeBinary


def logprint(*a):
    print(a)


class FakeLogger(object):

    def __getattr__(self, *a):
        return logprint

    def __call__(self, *a, **k):
        print(k, a)


fakelogger = FakeLogger()


def xmlrpcSanitize(val, attr=[], otype=False):
    if otype == 'Profile':
        return binfunc(pickle.dumps(val))
    elif ('Binary' in attr):
        return binfunc(val)
    if isinstance(val, dict):
        r = {}
        for k, v in val.items():
            r[k] = xmlrpcSanitize(v)
        return r
    if py == 3 and isinstance(val, bytes):
        return unicode_func(val)
    if isinstance(val, (np.string_, np.str_, bytes)):
        val = ''.join(map(unicode_func, val[:]))
        return val
    if hasattr(val, '__iter__') and not isinstance(val, dict) and not isinstance(val, str):
        r = list(xmlrpcSanitize(el) for el in val)
        return r
    if type(val) in [type(np.float64(0)), type(np.float32(0))]:
        return float(val)
    if type(val) in [type(np.int64(0)), type(np.int32(0)), type(np.int8(0))]:
        return int(val)
    
    return val


import re


def sanitize(func):
    """XML Sanitizer decorator"""

    @functools.wraps(func)
    def sanitize_wrapper(self, *a, **k):
        r = func(self, *a, **k)
        return xmlrpcSanitize(r)

    # Save original argspec, so it can be retrieved by func_args().
    sanitize_wrapper.wrapped = inspect.getargspec(func)
    return sanitize_wrapper


def natural_keys(text):
    """Natural ordering key function for list.sort().
    See http://www.codinghorror.com/blog/archives/001018.html"""
    r = [int(s) if re.match(r'([-]?\d+)', s) else s for s in re.split(r'([-]?\d+)', text)]
    return r


def func_args(func):
    """Return a flatten list of function argument names.
    Correctly detect decorated functions"""
    if hasattr(func, 'wrapped'):
        w = func.wrapped
        r = w.args
        if w.varargs:
            r.append(w.varargs)
        if w.keywords:
            r.append(w.keywords)
        return r
    # non-wrapped
    if hasattr(func, 'func_code'):
        return func.func_code.co_varnames
    if hasattr(func, '__code__'):
        return func.__code__.co_varnames
    # Non-function?
    return []


#####
# FILESYSTEM UTILS
#######
goodchars = ['-', '_', ' ']
badchars = []


def validate_filename(fn, good=goodchars, bad=badchars):
    """Purifica un filename da tutti i caratteri potenzialmente invalidi"""
    fn = unicode(fn)
    if py == 2:
        fn = fn.encode('ascii', 'ignore')
    fn = list(fn)

    def check_char(x):
        return (x.isalpha() or x.isdigit()) or (x in goodchars and x not in badchars)

    fn = filter(check_char, fn)
    # scarta tutti i caratteri non alfanumerici
    fn = "".join(list(fn))
    return fn


def incremental_filename(original):
    if not os.path.exists(original):
        return original
    ext = ''
    base = original.split('.')
    
    if len(base) > 1:
        ext = '.' + base.pop(-1)
    base = '.'.join(base)
    prenum = base.split('_')
    number = 1
    if len(prenum) > 1 and prenum[-1][0]!='0' and len(prenum[-1])<4:
        try:    
            number = int(prenum[-1]) + 1
            prenum.pop(-1)
        except:
            pass
            
    prenum = '_'.join(prenum)
    
    new = prenum + '_' + str(number) + ext
    while os.path.exists(new):
        number += 1
        new = prenum + '_' + str(number) + ext
        
    return new


def iter_cron_sort(top, field=1, reverse=False):
    """
    Return ordered of tuples (path,ctime,size) for all files from `top` folder recursively and ordered by field.
    field 0: name, 1: time, 2: size
    """
    r = []
    for root, dirs, files in os.walk(top):
        for name in files:
            f = os.path.join(root, name)
            s = os.stat(f)
            r.append((f, s.st_ctime, s.st_size))
    r = sorted(r, key=itemgetter(field), reverse=reverse)
    return r


def disk_free(path, unit=1048576.):
    """Calculate free disk space"""
    if isWindows:
        u = psutil.disk_usage(path)
        return u.free / unit, u.total / unit, u.used / unit
    st = os.statvfs(path)
    f = st.f_frsize / unit
    free = st.f_bavail * f
    total = st.f_blocks * f
    used = (st.f_blocks - st.f_bfree) * f
    return free, total, used


def list_file_types(path, ext='.h5'):
    r = []
    for root, dirs, files in os.walk(path):
        f = list(filter(lambda f: f.endswith(ext), files))
        r += list([os.path.join(root, f) for f in f])
    return r


def chunked_upload(upfunc, fp, sigfunc=lambda v: 0):
    name = os.path.basename(fp)
    w = 2000000
    N = 1. * os.stat(fp).st_size / w
    if N < 1:
        N = 1
    f = open(fp, 'rb')
    pf = 100. / N
    for i in range(int(N)):
        dat = f.read(w)
        upfunc(xmlrpclib.Binary(dat), i, name)
        pc = pf * i
        sigfunc(int(pc))
        print('sent %.2f' % (pc))
    ui = -1
    if N == 1:
        ui = 0
    dat = f.read()
    upfunc(xmlrpclib.Binary(dat), ui, name)
    if N == 1:
        upfunc(xmlrpclib.Binary(''), -1, name)
    sigfunc(100)


def flatten(x):
    """Build a flat list out of any iter-able at infinite depth"""
    result = []
    for el in x:
        # Iteratively call itself until a non-iterable is found
        if hasattr(el, "__len__") and not isinstance(el, str):
            flt = flatten(el)
            result.extend(flt)
        else:
            result.append(el)
    return result


def find_nearest_brute(v, x):
    """`v`: lista o vettore monodimensionale dove ricercare il valore `x`"""
    v = abs(np.array(v) - np.array(x))
    f = np.where(v == v.min())[0][0]
    return f


def find_nearest_val(v, t, get=False, seed=None, start=0, end=-1):
    """Finds value nearest to `t` in array `v`, assuming v is monotonic.
    Optionally use the `get` function instead of v.__getitem__, in order to retrieve single elements from the array.
    Limit the search in range (start, end)"""
    # TODO: explore builtin bisect module!!!
    if get is False:
        g = v.__getitem__
    else:
        g = get

    if len(v) <= 1:
        #print('find_nearest_val: empty arg')
        return 0
    n = len(v)
    start, end = int(start), int(end)
    if end < 0:
        end = n + end
    if end > n:
        end = n - 1
    if start < 0:
        start = n + start
    g0 = g(start)
    g_1 = g(end)
    positive = g_1 > g0
    if (t < g0 and positive) or (t > g0 and not positive):
        return start
    if (t > g_1 and positive) or (t < g_1 and not positive):
        return end
    if seed is None:
        i = int(start + (end - start) // 2)  # starting index
    else:
        i = int(seed)
    i = min(end, max(start, i))
    smaller = start  # prev smaller index
    bigger = end  # prev bigger index
    bi = i  # best index
    bd = np.inf  # min delta
    ok = 2  # ping-pong counter
    while ok > 0:
        i = int(i)
        c = g(i)  # current delta
        d = t - c  # delta
        b = abs(d)
        # remember best index and delta
        if b < bd:
            bd = b
            bi = i
        # can't be better than that
        if d == 0:
            bi = i
            break
        # bigger d: choose smaller index
        if (d < 0 and positive) or (d > 0 and not positive):
            if i - smaller < 1:
                break
            bigger = i
            # Detect last integer reduction
            if i == smaller + 1:
                i = smaller
                ok -= 1
            else:
                # Half-way reduce towards `smaller`
                i = smaller + (i - smaller) // 2
        # smaller d: choose bigger index
        else:
            if bigger - i < 1:
                break
            smaller = i
            # Detect last integer increase
            if i == bigger - 1:
                i = bigger
                ok -= 1
            else:
                # Half-way increase towards `bigger`
                i += (bigger - i) // 2

    return int(bi)


def smooth(x, window=10, method='hanning', recurse=0):
    """method='flat', 'hanning', 'hamming', 'bartlett', 'blackman', 'kaiser'"""
    s = np.r_[2 * x[0] - x[window - 1::-1], x, 2 * x[-1] - x[-1:-window:-1]]
    # print(len(s))
    if method == 'flat':  # moving average
        w = np.ones(window, 'd')
    else:
        w = eval('np.' + method + '(window)')
    y = np.convolve(w / w.sum(), s, mode='same')
    y = y[window:-window + 1]
    if recurse>0:
        y = smooth(x, window, method, recurse-1)
    return y


from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5, btype='band'):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    if btype.startswith('band'):
        b, a = butter(order, [low, high], btype=btype)
    elif btype == 'lowpass':
        b, a = butter(order, high, btype=btype)
    else:
        b, a = butter(order, low, btype=btype)
        
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5, invert=False):
    btype = 'band'
    if lowcut <= 0:
        btype = 'lowpass'
    elif highcut > fs:
        bytpe = 'highpass'
    # Invert the meaning
    if invert:
        btype = {'h': 'lowpass', 'l':'highpass', 'b': 'bandstop'}[btype[0]]
    b, a = butter_bandpass(lowcut, highcut, fs, order=order, btype=btype)
    y = lfilter(b, a, data)
    return y


def _update_filter(new, old):
    """Add new filter to old filter in old array indexes"""
    j = 0
    nj = 0
    n = len(new)
    print('start', new, old)
    for o in old:
        if o >= j:
            j += o - j + 1
        
        while nj < n - 1 and new[nj] + 1 < j: 
            nj += 1
        
        if new[nj] + 1 < j:
            break
            
        new[nj:] += 1
        
    return np.sort(np.concatenate((old, new)))


def smooth_discard(x, percent=10., drop='absolute', passes=1, **kw):
    y = smooth(x, **kw)
    d = abs(x - y)
    if drop == 'absolute':
        # Delete all elements which exceeds the stdev by percent%
        m = (d.mean() + d.std()) * (100 + percent) / 100.
        s = np.where(d > m)[0]
        n = None  # take all
    elif drop == 'relative':
        s = np.argsort(d)
        # Delete most distant percent% elements
        n = -int(len(s) * percent / 100.)
    else:
        raise BaseException('Unknown parameter drop: ' + drop)
     
    if not len(s):
        print('smooth_discard: not filtering', drop, percent, passes)
        return y, x, s
    # Delete selected far points
    s = s[n:]
    
    y = np.delete(y, s)
    # Multi-pass filtering
    if passes > 1:
        print('smooth pass', passes, len(y), len(s))
        y, x1, s1 = smooth_discard(y, percent=percent, drop=drop, passes=passes - 1, **kw)
        # Concatenate filters
        if len(s) and len(s1):
            s = _update_filter(s1, s)
    # Delete raw only in the end
    else:
        x = np.delete(x, s) 
    # Smoothed filtered, raw filtered, filter
    return y, x, s


def toslice(v):
    """Recursive conversion of an iterable into slices"""
    if isinstance(v, slice):
        r = [v.start, v.stop, v.step]
        for i in (0, 1, 2):
            if not isinstance(r[i], (int, type(None))):
                r[i] = int(r[i])
        return slice(*r)
    if not isinstance(v, collections.Iterable):
        if not isinstance(v, slice):
            v = int(v)
        return v
    r = []
    isSlice = True
    for i, el in enumerate(v):
        if isinstance(el, collections.Iterable):
            el = toslice(el)
            isSlice = False
        if isinstance(el, slice):
            isSlice = False
        r.append(el)
    if isSlice == True:
        return toslice(slice(*r))
    return tuple(r)


def decode_cool_event(event):
    """Decode a ">cool,temperature,timeout" thermal cycle event"""
    if not event.startswith('>cool'):
        return False
    event = event.split(',')
    T = float(event[1])
    if len(event) > 2:
        timeout = float(event[2])
    return T, timeout


def decode_checkpoint_event(event):
    if not event.startswith('>checkpoint'):
        return False
    event = event.split(',')
    delta = float(event[1])
    if len(event) > 2:
        timeout = float(event[2])
    return delta, timeout

def power_event_duration(ev):
    if isinstance(ev, str):
        ev = ev.split(',')
    return float(ev[2])*int(ev[3])+float(ev[4])

move_openclose_wait = 60

def move_event_duration(ev):
    if isinstance(ev, str):
        ev = ev.split(',')
    if len(ev)==2:
        ev.append(0)
    return float(ev[2])+move_openclose_wait

def event_duration(ev):
    if ev.startswith('>power'):
        return power_event_duration(ev)
    if ev.startswith('>move'):
        return move_event_duration(ev)
    return 0

def next_point(crv, row, delta=1, events=False):
    """Search next non-event point in thermal cycle curve `crv`.
    Starts by checking `row` index, then adds `delta` (+-1),
    until proper value is found."""
    N = len(crv)
    while row >= 0 and row < N:
        ent = crv[row]
        c = isinstance(ent[1], basestring)
        print('next_point',row, ent, c, events, delta)
        # Found an event
        if c and not events:
            row += delta
            continue
        # Avoid natural cooling event
        #if c and events and ent[1].startswith('>cool'):
        #    row += delta
        #else:
        #    break
        break
        
    if row < 0:
        return -1, False
    if row >= N:
        return N, False

    return row, ent


class initializeme(object):
    """Decorator to protect a function call behind an initializing flag"""

    def __init__(self, repeatable=False):
        """`repeatable`=False will not allow the decorated function to be called if the object is 
        already initializing."""
        self.repeatable = repeatable
    
    def __call__(self, func):
        repeatable = self.repeatable

        @functools.wraps(func)
        def initializeme_wrapper(self, *args, **kwargs):
            if self['initializing'] and not repeatable:
                self.log.error('Already initializing: cannot exec', func)
                raise BaseException('Already initializing: cannot execute')
            try:
                self['initializing'] = True
                r = func(self, *args, **kwargs)
                self['initializing'] = False
                return r
            except KeyboardInterrupt:
                raise KeyboardInterrupt()
            except:
                self.log.error('initializing_flag: exc calling', func, args, kwargs, format_exc())
                raise
            finally:
                self['initializing'] = False
            return False

        return initializeme_wrapper


class lockme(object):
    """Decorator to lock/unlock method execution.
    The class having its method decorated must expose
    a _lock object compatible with threading.Lock."""

    def __init__(self, timeout=5):
        self.timeout = timeout
        
    def __call__(self, func):
        timeout = self.timeout

        @functools.wraps(func)
        def lockme_wrapper(self, *args, **kwargs):
            if self._lock is False:
                return func(self, *args, **kwargs)
            if isinstance(self._lock, multiprocessing.synchronize.Lock):
                r = self._lock.acquire(timeout=timeout)
                if not r:
                    raise BaseException("Failed to acquire lock")
            else:
                # Threading locks does not support timeout (py2)
                self._lock.acquire()
            try:
                return func(self, *args, **kwargs)
            except KeyboardInterrupt:
                raise KeyboardInterrupt()
            except:
                print('lockme: exc calling', self, func, args, kwargs)
                print_exc()
            finally:
                try:
                    self._lock.release()
                except:
                    pass

        return lockme_wrapper


def unlockme(func):
    """Decorator to finally unlock after method execution.
    Useful if locking must be delayed.
    The class having its method decorated must expose
    a _lock object compatible with threading.Lock."""

    @functools.wraps(func)
    def unlockme_wrapper(self, *args, **kwargs):
        if self._lock is False:
            return func(self, *args, **kwargs)
        try:
            return func(self, *args, **kwargs)
        finally:
            try:
                self._lock.release()
            except:
                pass

    return unlockme_wrapper


class retry(object):

    """Decorator class to retry a function execution"""

    def __init__(self, times=None, hook=False):
        self.times = times
        self.hook = hook

    def __call__(self, func):

        @functools.wraps(func)
        def retry_loop(*args, **kwargs):
            # If retry was defined as None,
            # it is expected as a property of the first argument (the func's
            # self).
            retry = self.times
            if retry is None:
                retry = args[0].retry
            times = retry
            retry0 = retry
            while True:
                try:
                    r = func(*args, **kwargs)
                    return r
                except KeyboardInterrupt:
                    raise KeyboardInterrupt()
                except:
                    print('retry', retry0 - retry, func, times)
                    retry -= 1
                    if retry <= 0:
                        print('End retry')
                        raise
                    # Call the retry hook
                    if self.hook is not False:
                        self.hook(
                            func, args, kwargs, sys.exc_info(), times - retry)

        return retry_loop


import cProfile
import pstats

profile_path = '/tmp/mdf/profile/'


def start_profiler(obj):
    obj.__p = cProfile.Profile()
    obj.__p.enable()


def stop_profiler(obj):
    out = '{}{}_{}.prf'.format(
        profile_path, obj.__class__.__name__, str(id(obj)))
    print('PROFILING STATS FOR', out)
    s = pstats.Stats(obj.__p)
    s.sort_stats('cumulative')
    s.dump_stats(out)
    obj.__p.disable()


prf_uid = -1


def profile(func):
    """Profiling decorator for multiprocessing calls"""
    if not profiling:
        return func

    @functools.wraps(func)
    def profile_wrapper(self, *a, **k):
        global prf_uid
        prf_uid += 1
        p = cProfile.Profile()
        try:
            fp = getattr(self, '__getitem__', {'fullpath': ''}.get)('fullpath')
        except:
            fp = ''
        name = func.__name__
        if isinstance(self, object):
            name = self.__class__.__name__ + '.' + name
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
        out = '{}{}_{}_{}.prf'.format(profile_path,
                                      name,
                                      fp.replace('/', '_'),
                                      prf_uid)
        print('START PROFILING STATS FOR', func.__name__, ' AT ', repr(self), out)
        p.enable()
        r = func(self, *a, **k)
        s = pstats.Stats(p)
        s.sort_stats('cumulative')
        s.dump_stats(out)
        p.disable()
        print('END PROFILING STATS FOR', func.__name__, ' AT ', repr(self), out)
        return r

    return profile_wrapper


def from_seconds_to_hms(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)


def ensure_directory_existence(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


# LOCALE CONTEXT MANAGER
from contextlib import contextmanager
import locale
import threading
LOCALE_LOCK = threading.Lock()


@contextmanager
def setlocale(name):
    """Temporary locale context manager. For datetime.strptime with Qt
    From: http://stackoverflow.com/a/24070673/1645874"""
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)
          

from datetime import datetime  


def decode_datetime(val, format='%a %b %d %H:%M:%S %Y'):
    # Wed Nov 11 18:35:36 2015
    with setlocale('C'):
        ret = datetime.strptime(val, format)
    return ret


def filter_calibration_filenames(filenames):
    return [filename for filename in filenames if not '/calibration/' in filename.lower()]


def only_hdf_files(filenames):
    return [filename for filename in filenames if filename.endswith('.h5')]


from random import random


class SharedProcessResources(object):
    
    def __init__(self):
        self.res = []
        self.pid = multiprocessing.current_process().pid
        self.name = '{}-{}'.format(self.pid, random())
    
    def register(self, setter, *args, **kwargs): 
        if os.name != 'nt':
            return
        print('Register', self.name)   
        self.res.append((setter, args, kwargs))
    
    def __call__(self):
        if os.name != 'nt':
            return
        t0 = standardTime.time()
        print('Restoring', self.name, len(self.res))
        for (setter, args, kwargs) in self.res:
            setter(*args, **kwargs)
        print('RESTORED', 1000 * (standardTime.time() - t0))


sharedProcessResources = SharedProcessResources()
        
