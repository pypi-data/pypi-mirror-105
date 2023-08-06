#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Mdf Language or Mini Language.
Secure minimal Python language subset for conditional evaluation of numerical datasets."""

from .dataenv import DataEnvironment
from .objenv import InterfaceEnvironment
from .milang import MiLang
import re

script_registry = {}
_script_registry = None

def compile_script_registry():
    global _script_registry
    _script_registry = {}
    for k, v in script_registry.items():
        k1 = re.compile(k)
        _script_registry[k1] = v

class Scriptable(object):

    """A configuration object fragment which can contain and execute Script-type options"""

    def __init__(self):
        self.scripts = []
        self.end_scripts = []
        self.always_scripts = []
        self.all_scripts = []
        self.env = DataEnvironment()
        
    def check_script_registry(self, opt, path):
        if opt['factory_default']!=opt['current']:
            self.log.debug('Skip customized script update:', path)
            return False
        n = 0
        for k in _script_registry:
            m = k.match(path)
            if not m:
                continue
            if opt['current']==_script_registry[k]:
                continue
            self.log.debug('Updating script source:',path)
            self[opt['handle']] = _script_registry[k]
            n+=1
        return n
    
    def compile_scripts(self, hdf=False):
        """Compile all Script-type options,
        assigning them to the appropriate container dictionary."""
        self.scripts = []
        self.end_scripts = []
        self.always_scripts = []
        self.all_scripts = {}
        self.script_env = InterfaceEnvironment(self)
        cold = isinstance(self.desc, dict)
        if cold and (_script_registry is None):
            compile_script_registry()
        if hdf is not False:
            self.env.hdf = hdf
            self.script_env.hdf = hdf
        for handle, opt in self.describe().items():
            if opt['type'] != 'Script':
                continue
            if not opt.get('enabled', True):
                continue
            if cold:
                self.check_script_registry(opt, self['fullpath']+handle)
                
            p = opt['flags'].get('period', None)
            exe = MiLang(
                opt['current'], env=self.env, script_env=self.script_env)
            exe.period = p
            exe.handle = handle
            exe.meta = opt.get('parent', False)
            # Identify scripts which output on the holding Scriptable itself
            h = 'Meta_' + handle
            if h in self:
                if self.gettype(h) == 'Meta':
                    exe.handle = h
            self.add_script(exe)

    def add_script(self, exe):
        if not exe.code:
            self.log.error('Compilation failed', exe.handle, exe.error)
            return False
        # Insert into all_scripts
        self.all_scripts[exe.handle] = exe
        # Inserting into frequency containers
        # If no period is defined, the script will be executed at
        # characterization time (about every 30s)
        if exe.period == None:
            self.scripts.append(exe.handle)
        # If an >=0 period is defined, the script is always executed
        #TODO: implement custom execution freq based on this number
        elif exe.period >= 0:
            self.always_scripts.append(exe.handle)
        # If period <0, the script will be executed only at the end of the test
        elif exe.period < 0:
            self.end_scripts.append(exe.handle)
        return True

    def execute_scripts(self, ins=None, period=False):
        """Execute script contained in `scripts` dictionary, passing `ins` onto eval()"""
        r = True
        if period == False:
            scripts = self.scripts
        elif period == 'end' :
            scripts = self.end_scripts
        elif period == 'always':
            scripts = self.always_scripts
        elif period == 'all':
            scripts = self.all_scripts

        scripts = set(scripts)
        for handle in scripts:
            r1 = self.execute_script(handle, ins)
            r = r and r1 
        return r

    def execute_script(self, handle, ins):
        exe = self.all_scripts[handle]
        en = exe.script_env.obj.getFlags(handle).get('enabled', True)
        if not en:
            self.log.debug('Disabled script, skipping:', handle)
            return True
        if ins:
            exe.set_env_outFile(ins.outFile)
        u = exe.eval(self, ins=ins)
        if u:
            self.log.debug('execute_script done:', handle, u, 
                       exe.env.time, exe.env.temp, exe.env.value)
        return u

    def validate_script(self, handle):
        """Validates a script option by name"""
        if handle not in self.script:
            self.log.info('Not a Script option!', handle)
            return False
        exe = MiLang(self[handle], self.env)
        if not exe.code:
            self.log.error(
                'Compilation failed', handle, self[handle], exe.error)
            return False
        return True
    xmlrpc_validate_script = validate_script

    def validate_script_text(self, text):
        """Validates a script text"""
        exe = MiLang(text, self.env)
        if not exe.code:
            self.log.error(
                'Custom text compilation failed', exe.error, exe.error_line, exe.error_col)
            return exe.error, exe.error_line, exe.error_col
        return "", -1, -1
    xmlrpc_validate_script_text = validate_script_text

    ######
    # Instrument-related methods

    def distribute_scripts(self, hdf=False):
        """Compile Samples and Measure scripts."""
        if not hasattr(self, 'measure'):
            self.log.error('Script distribution makes no sense on this object')
            return False
        if hdf is False:
            hdf = self.outFile
        self.log.debug('distributing scripts',repr(self.samples))
        self.measure.compile_scripts(hdf)
        for smp in self.samples:
            if not smp:
                self.log.error('Invalid sample', smp, self.samples)
                continue
            self.log.debug('distributing sample scripts',smp)
            smp.compile_scripts(hdf)
            
    def xmlrpc_distribute_scripts(self, *a, **k):
        return self.distribute_scripts(*a, **k)

    def characterization(self, period=False):
        """Execute scripts."""
        if not hasattr(self, 'measure'):
            self.log.error('Characterization makes no sense on this object')
            return False
        self.measure.execute_scripts(self, period=period)
        for smp in self.samples:
            smp.execute_scripts(self, period=period)
