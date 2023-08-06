# -*- coding: utf-8 -*-
"""Utilities for digitally signing/verifying Mdf files"""
from traceback import print_exc
import hashlib
from mdf_canon.csutil import unicode_func
import Crypto
from Crypto.PublicKey import RSA
import Crypto.Hash.SHA as SHA
import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5


def purge_path(path, result):
    for cl, refs in result.items():
        if path in refs:
            refs.remove(path)
            result[cl] = refs
    return result

def list_references(parent, result=False):
    """Recursively search all references available starting from `parent` node, 
    and append their path to `result`,"""
    if result is False:
        result = {}
    for child in parent._f_list_nodes():
        # Do not list paths from different versions
        path = child._v_pathname
        # Skip special paths
        if path=='/userdata':
            continue
        # iteratively call itself onto Group nodes
        if child.__class__.__name__ in ('Group', 'RootGroup'):
            result = list_references(child, result=result)
            continue
            
        # if it is of the desired reference class
        while hasattr(child, 'dereference'):
                child = child.dereference()
        rc = getattr(child._v_attrs, '_reference_class', False)
        if not rc:
            if path!='/conf':
                print('No _reference_class', rc, path)
            continue
        rc = unicode_func(rc)
        if rc not in result:
            result[rc] = []
            
        result[rc].append(path)
        continue
    return result


def get_node_hash(f, path):
    """Calculate node hashes"""
    # FIXME: fails on VLArray (image, profile, object)
    d = ''
    try:
        n = f.get_node(path)
        if n._v_pathname != path:
            print('get_node_hash: skipping link', n._v_pathname, path)
            return d
        d = hashlib.md5(n[:]).hexdigest()
        n.close()
    except:
        print('while hashing', path)
        print_exc()
    return d


def calc_hash(f):
    """Create the data message used for digital sign"""
    data = {}
    for rc, paths in list_references(f.root).items():
        for path in paths:
            if path.startswith('/ver_'):
                continue
            data[path] = get_node_hash(f, path)
    data['/conf'] = get_node_hash(f, '/conf')
    # Fixed ordering
    msg = ''
    k = sorted(list(data.keys()))
    for p in k:
        msg += p + ':' + data[p]
    return msg


def verify(f):
    """Verify the authenticity of the data contained in a Mdf Test File (already opened)"""
    # Read the certificate
    key = getattr(f.root.conf._v_attrs, 'public_key', False)
    if not key:
        print('No certificate saved in the file')
        return False

    # Read the signature
    signature = getattr(f.root.conf._v_attrs, 'signature', False)
    if not signature:
        print('No singature saved in the file')
        return False

    # Create the key
    key = Crypto.PublicKey.RSA.importKey(key)

    # Create the data message
    data = calc_hash(f)

    # Create message digest
    h = SHA.new(data)
    # Create the verifier
    verifier = PKCS1_v1_5.new(key)

    # Verify
    return verifier.verify(h, signature)
