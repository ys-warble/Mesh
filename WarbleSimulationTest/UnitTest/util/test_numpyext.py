from unittest import TestCase

import numpy as np

import WarbleSimulation.util.numpy_ext as npx
from WarbleSimulation.util import Logger
from WarbleSimulationTest import test_settings


class TestNumpyExt(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = Logger.get_logger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger.info('')
        self.logger.info(test_settings.start_title_format(self._testMethodName))

    def tearDown(self):
        self.logger.info(test_settings.end_title_format(self._testMethodName))
        self.logger.info('')

    def test_char_mod_valid(self):
        dimension = (5, 5, 5)
        a = np.zeros(dimension)
        b = np.ones(dimension)

        c = npx.char.mod('hsl(%d,%d%)', (a, b))
        # TODO pass-fail condition

        self.assertTrue(np.array_equal(np.full(dimension, 'hsl(0,1%)'), c))

    def test_char_mod_invalid(self):
        self.assertEqual(None, npx.char.mod('hsl(%)', ()))

        a = np.zeros((5, 5, 5))
        b = np.ones((4, 4, 4))
        self.assertRaises(ValueError, lambda: (npx.char.mod('hsl(%d,%d%)', (a, b))))
        self.assertRaises(ValueError, lambda: (npx.char.mod('hsl(%d,%d%)', a)))
        self.assertRaises(ValueError, lambda: (npx.char.mod('hsl(%d%)', (a, b))))
