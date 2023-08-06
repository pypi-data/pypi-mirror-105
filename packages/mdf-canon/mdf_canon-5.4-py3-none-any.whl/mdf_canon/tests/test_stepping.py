#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import numpy as np
from mdf_canon import stepping
mono1 = np.linspace(0, 90, 10)
mono2 = np.linspace(0, 99, 100)
mono3 = np.linspace(0, 99.9, 1000)

bi1a = np.concatenate((mono1, mono1+100))
bi1b = np.concatenate((mono1, mono1[::-1]+10))

bi2a = np.concatenate((mono2, mono2+100))
bi2b = np.concatenate((mono2, mono2[::-1]+1))

bi3a = np.concatenate((mono3, mono3+100))
bi3b = np.concatenate((mono3, mono3[::-1]+0.1))


class TestStepping(unittest.TestCase):
    def test_uniform_and_monotonic(self):
        r = list(stepping.stepping((mono1, )))
        self.assertEqual(r, [[i] for i in range(10)])
        
        r = list(stepping.stepping((mono1, mono1)))
        self.assertEqual(r, [[i,i] for i in range(10)])
        
        r = list(stepping.stepping((mono2, mono2)))
        self.assertEqual(r, [[i,i] for i in range(100)])
        
        r = list(stepping.stepping((mono1, mono1, mono1)))
        self.assertEqual(r, [[i,i,i] for i in range(10)])
        
    def test_uniform_and_monotonic_start(self):
        r = list(stepping.stepping((mono1, mono1), start=50))
        self.assertEqual(r, [[i,i] for i in range(5, 10)])
        
        r = list(stepping.stepping((mono2, mono2), start=50))
        self.assertEqual(r, [[i,i] for i in range(50, 100)])
        
    def test_uniform_and_monotonic_delta(self):
        r = list(stepping.stepping((mono1, mono1), delta=20))
        self.assertEqual(r, [[i,i] for i in range(0, 10, 2)])
        
        # Too small delta
        r = list(stepping.stepping((mono1, mono1), delta=1))
        self.assertEqual(r, [[i,i] for i in range(0, 10)])
        
        r = list(stepping.stepping((mono2, mono2), delta=2))
        self.assertEqual(r, [[i,i] for i in range(0, 100, 2)])
        
        r = list(stepping.stepping((mono3, mono3), delta=0.2))
        self.assertEqual(r, [[i,i] for i in range(0, 1000, 2)])
        
    def test_uniform_and_monotonic_start_delta(self):
        r = list(stepping.stepping((mono1, mono1), delta=20, start=50))
        self.assertEqual(r, [[i,i] for i in range(5, 10, 2)])
        
        # Too small delta
        r = list(stepping.stepping((mono1, mono1), delta=1, start=50))
        self.assertEqual(r, [[i,i] for i in range(5, 10)])
        
        r = list(stepping.stepping((mono2, mono2), delta=2, start=50))
        self.assertEqual(r, [[i,i] for i in range(50, 100, 2)])
        
        r = list(stepping.stepping((mono3, mono3), delta=0.2, start=50))
        self.assertEqual(r, [[i,i] for i in range(500, 1000, 2)])
        
        
    def test_difform_monotonic(self):
        r = list(stepping.stepping((mono1, mono2)))
        self.assertEqual(r, [[i,i*10] for i in range(10)])
        
        r = list(stepping.stepping((mono1, mono3)))
        self.assertEqual(r, [[i,i*100] for i in range(10)])
        
        r = list(stepping.stepping((mono1, mono2, mono3)))
        self.assertEqual(r, [[i,i*10,i*100] for i in range(10)])
        
        r = list(stepping.stepping((mono2, mono3)))
        self.assertEqual(r, [[i,i*10] for i in range(100)])
        
    def test_difform_monotonic_start(self):
        r = list(stepping.stepping((mono1, mono2), start=50))
        self.assertEqual(r, [[i,i*10] for i in range(5,10)])
        
        r = list(stepping.stepping((mono1, mono3), start=50))
        self.assertEqual(r, [[i,i*100] for i in range(5,10)])
        
        r = list(stepping.stepping((mono1, mono2, mono3), start=50))
        self.assertEqual(r, [[i,i*10,i*100] for i in range(5, 10)])
        
        r = list(stepping.stepping((mono2, mono3), start=50))
        self.assertEqual(r, [[i,i*10] for i in range(50, 100)])
        
    def test_difform_monotonic_delta(self):    
        r = list(stepping.stepping((mono1, mono2), delta=20))
        self.assertEqual(r, [[i,i*10] for i in range(0,10,2)])
        
        r = list(stepping.stepping((mono1, mono3), delta=20))
        self.assertEqual(r, [[i,i*100] for i in range(0,10,2)])
        
        r = list(stepping.stepping((mono1, mono2, mono3), delta=20))
        self.assertEqual(r, [[i,i*10,i*100] for i in range(0,10,2)])
        
        r = list(stepping.stepping((mono2, mono3), delta=2))
        self.assertEqual(r, [[i,i*10] for i in range(0,100,2)])
        
    def test_difform_monotonic_start_delta(self):    
        r = list(stepping.stepping((mono1, mono2), delta=20, start=50))
        self.assertEqual(r, [[i,i*10] for i in range(5,10,2)])
        
        r = list(stepping.stepping((mono1, mono3), delta=20, start=50))
        self.assertEqual(r, [[i,i*100] for i in range(5,10,2)])
        
        r = list(stepping.stepping((mono1, mono2, mono3), delta=20, start=50))
        self.assertEqual(r, [[i,i*10,i*100] for i in range(5,10,2)])
        
        r = list(stepping.stepping((mono2, mono3), delta=2, start=50))
        self.assertEqual(r, [[i,i*10] for i in range(50,100,2)])  
        
    def test_uniform_and_bitonic(self):        
        r = list(stepping.stepping((bi1a, bi1b)))
        self.assertEqual(r, [[i,i] for i in range(20)])
        
        r = list(stepping.stepping((bi2a, bi2b)))
        self.assertEqual(r, [[i,i] for i in range(200)])
        
        r = list(stepping.stepping((bi3a, bi3b, bi3a)))
        self.assertEqual(r, [[i,i,i] for i in range(2000)])
        
    def test_uniform_and_bitonic_start(self):
        r = list(stepping.stepping((bi1a, bi1b), start=50))
        print(r)
        print(bi1a)
        print(bi1b)
        self.assertEqual(r, [[i,i] for i in range(5, 20)])
        
        r = list(stepping.stepping((bi2a, bi2b), start=50))
        self.assertEqual(r, [[i,i] for i in range(50, 200)])
        
    def test_uniform_and_bitonic_delta(self):
        r = list(stepping.stepping((bi1a, bi1b), delta=20))
        self.assertEqual(r, [[i,i] for i in range(0, 20, 2)])
        
        # Too small delta
        r = list(stepping.stepping((bi1a, bi1b), delta=1))
        self.assertEqual(r, [[i,i] for i in range(0, 20)])
        
        r = list(stepping.stepping((bi2a, bi2b), delta=2))
        self.assertEqual(r, [[i,i] for i in range(0, 200, 2)])
        
        r = list(stepping.stepping((bi3a, bi3b), delta=0.2))
        self.assertEqual(r, [[i,i] for i in range(0, 2000, 2)])
        
        
if __name__ == "__main__":
    unittest.main(verbosity=2)