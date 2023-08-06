# -*- coding: utf-8 -*-
"""Generalized logging utilities"""
import os
import logging
import functools
from datetime import datetime
from . import csutil
from .csutil import is_unicode, basestring, unicode_func   
    
root_log = logging.getLogger()
root_log.setLevel(-1)
formatter = logging.Formatter("%(levelname)s: %(asctime)s %(message)s")
for h in root_log.handlers:
    h.setFormatter(formatter)
    
def concatenate_message_objects(*msg):
    # Ensure all message tokens are actually strings
    # (avoid "None" objects pollute the buffer!)
    msg = list(msg)
    for i, e in enumerate(msg):
        if is_unicode(e):
            continue
        elif isinstance(e, basestring):
            msg[i] = unicode_func(e, 'utf-8', errors='ignore')
        else:
            msg[i] = unicode_func(repr(e), 'utf-8', errors='ignore')
    return msg
    
def formatMsg(*msg, **po):
    """Format the message for pretty visualization"""
    t = po.get('t' , csutil.time())
    st = datetime.fromtimestamp(t).strftime('%x %X.%f')
    # Owner e priority
    o = po.get('o')
    p = po.get('p')
    pid =po.get('pid', os.getpid())
    if p == None:
        p = logging.NOTSET
    if o == None or o == '':
        own = ' '
        o = ''
    elif pid:
        own = ' (%s%i): ' % (o, pid)
    else:
        own = ' (%s): ' % (o)
    msg = concatenate_message_objects(*msg)
    smsg = ' '.join(tuple(msg))
    smsg = smsg.splitlines()
    pmsg = '%s%s' % (own, smsg[0])
    if len(smsg) > 1:
        for l in smsg[1:]:
            pmsg += '\n\t | %s' % l
    return t, st, p, o, msg, pmsg


def justPrint(*msg, **po):
    t, st, p, o, msg, pmsg = formatMsg(*msg, **po)
    print(str(t)+' '+st+' '+pmsg)
    return pmsg


def toLogging(*msg, **po):
    """Send log to standard python logging library"""
    t, st, p, o, msg, pmsg = formatMsg(*msg, **po)
    return logging.log(po.get('p', 10), pmsg)

message_buffer = 10

class BaseLogger(object):

    """Interface for standard logging functions definition and routing."""
    __buffer = -1
    
    @property
    def _buffer(self):
        if self.__buffer<0:
            return message_buffer
        else:
            return self.__buffer
    
    def __init__(self, log=justPrint):
        self._log = log
        self._last_msg = []
        
    def log(self, *msg, **po):
        self._last_msg.append((msg, po))
        if len(self._last_msg)>self._buffer:
            self._last_msg.pop(0)
        return self._log(*msg, **po)
    
    def replay(self, n=0):
        if n<=0:
            n = len(self._last_msg)
        msg = []
        for m,po in self._last_msg[-n:]:
            msg.append(formatMsg(*m, **po)[-1])
        return '\n'.join(msg)
    
    def clear_buffer(self):
        self._last_msg = []

    def __call__(self, *msg, **po):
        return self.log(*msg, p=po.get('p', logging.DEBUG))

    def debug(self, *msg):
        return self.log(*msg, p=logging.DEBUG)

    def info(self, *msg):
        return self.log(*msg, p=logging.INFO)

    def warning(self, *msg):
        return self.log(*msg, p=logging.WARNING)

    def error(self, *msg, **o):
        return self.log(*msg, p=logging.ERROR)

    def critical(self, *msg):
        return self.log(*msg, p=logging.CRITICAL)


class SubLogger(BaseLogger):

    """Implicit owner logging."""

    def __init__(self, parent):
        # TODO: pass DirShelf option path as log, instead of using a
        # parent.desc.
        BaseLogger.__init__(self, self._log)
        self.parent = parent

    def _log(self, *msg, **po):
        p = po.get('p', 0)
        msg = list(msg)
        for i, e in enumerate(msg):
            msg[i] = unicode_func(str(e), 'utf-8',errors='ignore')
        smsg = u' '.join(tuple(msg))
        if self.parent and self.parent.desc:
            self.parent.desc.set_current('log', [p, smsg])
        return smsg

def get_module_logging(owner):
    logfunc = functools.partial(toLogging, o=owner, pid=False)
    r = BaseLogger(log=logfunc) 
    return r

def set_log_file(log_file=False, logsize=10e6, count=10):
    import logging.handlers
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    rotating_file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=logsize, 
                                                                     backupCount=count)
    rotating_file_handler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(rotating_file_handler)
    sa = logging.StreamHandler()
    sa.setFormatter(formatter)
    root.addHandler(sa)
    return rotating_file_handler

global Log, log
Log = BaseLogger(log=toLogging)
log = Log.log

