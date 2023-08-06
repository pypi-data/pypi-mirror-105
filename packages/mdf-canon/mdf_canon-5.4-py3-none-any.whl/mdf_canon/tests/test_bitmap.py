#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest

import numpy as np
from PIL import Image

from mdf_canon import bitmap
from mdf_canon.tests import testdir

compressed = os.path.join(testdir,  'storage', 'compressed.bmp')
decompressed = os.path.join(testdir,  'storage', 'decompressed.bmp')
recompressed = os.path.join(testdir,  'storage', 'recompressed.bmp')
decompressed2 = os.path.join(testdir,  'storage', 'decompressed2.bmp')

class TestBitmapCompression(unittest.TestCase):
    def test(self):
        de = bitmap.decompress_path(compressed)
        open(decompressed, 'wb').write(de)
        im0 = Image.frombytes('L', (640, 480), de[::-1])
        sz = im0.size
        im = np.asarray(im0).reshape(sz[::-1])
        re = bitmap.compress(im)
        open(recompressed, 'wb').write(re)
        de2 = bitmap.decompress_path(recompressed)
        open(decompressed2, 'wb').write(de2)
        im2 = Image.frombytes('L', (640, 480), de2[::-1])
        self.assertEqual(im0.size, im2.size)
        im2a = np.asarray(im2).reshape(sz[::-1])
        self.assertTrue((im==im2).all())
        
        
        

if __name__ == "__main__":
    unittest.main(verbosity=2)