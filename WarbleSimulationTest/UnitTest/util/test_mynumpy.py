from unittest import TestCase

import numpy as np

import WarbleSimulation.util.mynumpy as mynumpy


class TestMyNumpy(TestCase):
    def test_char_mod_valid(self):
        dimension = (5, 5, 5)
        a = np.zeros(dimension)
        b = np.ones(dimension)

        c = mynumpy.char.mod('hsl(%d,%d%)', (a, b))
        # TODO pass-fail condition

        self.assertTrue(np.array_equal(np.full(dimension, 'hsl(0,1%)'), c))

    def test_char_mod_invalid(self):
        self.assertEqual(None, mynumpy.char.mod('hsl(%)', ()))

        a = np.zeros((5, 5, 5))
        b = np.ones((4, 4, 4))
        self.assertRaises(ValueError, lambda: (mynumpy.char.mod('hsl(%d,%d%)', (a, b))))
        self.assertRaises(ValueError, lambda: (mynumpy.char.mod('hsl(%d,%d%)', a)))
        self.assertRaises(ValueError, lambda: (mynumpy.char.mod('hsl(%d%)', (a, b))))
