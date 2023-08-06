# -*- coding: utf-8 -*-
"""Option persistence on HDF files."""
from .binary import Binary
from mdf_canon.csutil import dumps, loads, DEFAULT_PROTOCOL


class Object(Binary):

    @classmethod
    def encode(cls, dat):
        t, dat = dat
        dat = dumps(dat, DEFAULT_PROTOCOL)
        return Binary.encode((t, dat))

    @classmethod
    def decode(cls, dat):
        t, obj = Binary.decode(dat)
        obj = loads(obj)
        return obj
