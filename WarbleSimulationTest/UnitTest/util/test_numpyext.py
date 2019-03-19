from unittest import TestCase

import numpy as np

import WarbleSimulation.util.numpy_ext as npx


class TestNumpyExt(TestCase):
    def test_char_mod_valid(self):
        test_name = 'test_char_mod_valid'
        print('===== Running %s =====' % test_name)

        dimension = (5, 5, 5)
        a = np.zeros(dimension)
        b = np.ones(dimension)

        c = npx.char.mod('hsl(%d,%d%)', (a, b))
        # TODO pass-fail condition

        self.assertTrue(np.array_equal(np.full(dimension, 'hsl(0,1%)'), c))

    def test_char_mod_invalid(self):
        test_name = 'test_char_mod_valid'
        print('===== Running %s =====' % test_name)

        self.assertEqual(None, npx.char.mod('hsl(%)', ()))

        a = np.zeros((5, 5, 5))
        b = np.ones((4, 4, 4))
        self.assertRaises(ValueError, lambda: (npx.char.mod('hsl(%d,%d%)', (a, b))))
        self.assertRaises(ValueError, lambda: (npx.char.mod('hsl(%d,%d%)', a)))
        self.assertRaises(ValueError, lambda: (npx.char.mod('hsl(%d%)', (a, b))))
