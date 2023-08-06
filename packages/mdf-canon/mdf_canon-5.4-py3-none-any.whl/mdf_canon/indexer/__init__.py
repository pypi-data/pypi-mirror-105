# -*- coding: utf-8 -*-
"""Indexing hdf5 files"""
import os
os.environ['HDF5_USE_FILE_LOCKING']='FALSE'
from .corefile import addHeader
from .interface import SharedFile
from .filemanager import FileManager
from .indexer import Indexer, create_tables, FileSystemLock

from . import toi

from .digisign import list_references, calc_hash, verify
