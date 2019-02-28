from unittest import TestCase

import numpy as np

from WarbleSimulation.System.Entity.Concrete import transform_shape
from WarbleSimulation.util import Logger


class TestConcrete(TestCase):
    def setUp(self):
        self.logger = Logger.get_logger(__name__)
        self.arr = np.arange(8).reshape((2, 2, 2))

    def test_transform_shape_valid(self):
        expected = self.arr
        actual = transform_shape(self.arr, (1, 0, 0), (1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[2, 3],
             [6, 7]],
            [[0, 1],
             [4, 5]]])
        actual = transform_shape(self.arr, (1, 0, 0), (0, 1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[1, 5],
             [3, 7]],
            [[0, 4],
             [2, 6]]])
        actual = transform_shape(self.arr, (1, 0, 0), (0, 0, 1))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[6, 7],
             [4, 5]],
            [[2, 3],
             [0, 1]]])
        actual = transform_shape(self.arr, (1, 0, 0), (-1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[4, 5],
             [0, 1]],
            [[6, 7],
             [2, 3]]])
        actual = transform_shape(self.arr, (1, 0, 0), (0, -1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[4, 0],
             [6, 2]],
            [[5, 1],
             [7, 3]]])
        actual = transform_shape(self.arr, (1, 0, 0), (0, 0, -1))
        self.assertTrue(np.array_equal(expected, actual))

        #########################################################

        expected = np.array([
            [[4, 5],
             [0, 1]],
            [[6, 7],
             [2, 3]]])
        actual = transform_shape(self.arr, (0, 1, 0), (1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = self.arr
        actual = transform_shape(self.arr, (0, 1, 0), (0, 1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[1, 3],
             [0, 2]],
            [[5, 7],
             [4, 6]]])
        actual = transform_shape(self.arr, (0, 1, 0), (0, 0, 1))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[2, 3],
             [6, 7]],
            [[0, 1],
             [4, 5]]])
        actual = transform_shape(self.arr, (0, 1, 0), (-1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[6, 7],
             [4, 5]],
            [[2, 3],
             [0, 1]]])
        actual = transform_shape(self.arr, (0, 1, 0), (0, -1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[2, 0],
             [3, 1]],
            [[6, 4],
             [7, 5]]])
        actual = transform_shape(self.arr, (0, 1, 0), (0, 0, -1))
        self.assertTrue(np.array_equal(expected, actual))

        ##########################################################

        expected = np.array([
            [[4, 0],
             [6, 2]],
            [[5, 1],
             [7, 3]]])
        actual = transform_shape(self.arr, (0, 0, 1), (1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[2, 0],
             [3, 1]],
            [[6, 4],
             [7, 5]]])
        actual = transform_shape(self.arr, (0, 0, 1), (0, 1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = self.arr
        actual = transform_shape(self.arr, (0, 0, 1), (0, 0, 1))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[1, 5],
             [3, 7]],
            [[0, 4],
             [2, 6]]])
        actual = transform_shape(self.arr, (0, 0, 1), (-1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[1, 3],
             [0, 2]],
            [[5, 7],
             [4, 6]]])
        actual = transform_shape(self.arr, (0, 0, 1), (0, -1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[5, 4],
             [7, 6]],
            [[1, 0],
             [3, 2]]])
        actual = transform_shape(self.arr, (0, 0, 1), (0, 0, -1))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[6, 7],
             [4, 5]],
            [[2, 3],
             [0, 1]]])
        actual = transform_shape(self.arr, (-1, 0, 0), (1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[4, 5],
             [0, 1]],
            [[6, 7],
             [2, 3]]])
        actual = transform_shape(self.arr, (-1, 0, 0), (0, 1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[4, 0],
             [6, 2]],
            [[5, 1],
             [7, 3]]])
        actual = transform_shape(self.arr, (-1, 0, 0), (0, 0, 1))
        self.assertTrue(np.array_equal(expected, actual))

        expected = self.arr
        actual = transform_shape(self.arr, (-1, 0, 0), (-1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[2, 3],
             [6, 7]],
            [[0, 1],
             [4, 5]]])
        actual = transform_shape(self.arr, (-1, 0, 0), (0, -1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[1, 5],
             [3, 7]],
            [[0, 4],
             [2, 6]]])
        actual = transform_shape(self.arr, (-1, 0, 0), (0, 0, -1))
        self.assertTrue(np.array_equal(expected, actual))

        #########################################################

        expected = np.array([
            [[2, 3],
             [6, 7]],
            [[0, 1],
             [4, 5]]])
        actual = transform_shape(self.arr, (0, -1, 0), (1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[6, 7],
             [4, 5]],
            [[2, 3],
             [0, 1]]])
        actual = transform_shape(self.arr, (0, -1, 0), (0, 1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[2, 0],
             [3, 1]],
            [[6, 4],
             [7, 5]]])
        actual = transform_shape(self.arr, (0, -1, 0), (0, 0, 1))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[4, 5],
             [0, 1]],
            [[6, 7],
             [2, 3]]])
        actual = transform_shape(self.arr, (0, -1, 0), (-1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = self.arr
        actual = transform_shape(self.arr, (0, -1, 0), (0, -1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[1, 3],
             [0, 2]],
            [[5, 7],
             [4, 6]]])
        actual = transform_shape(self.arr, (0, -1, 0), (0, 0, -1))
        self.assertTrue(np.array_equal(expected, actual))

        ##########################################################

        expected = np.array([
            [[1, 5],
             [3, 7]],
            [[0, 4],
             [2, 6]]])
        actual = transform_shape(self.arr, (0, 0, -1), (1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[1, 3],
             [0, 2]],
            [[5, 7],
             [4, 6]]])
        actual = transform_shape(self.arr, (0, 0, -1), (0, 1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[5, 4],
             [7, 6]],
            [[1, 0],
             [3, 2]]])
        actual = transform_shape(self.arr, (0, 0, -1), (0, 0, 1))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[4, 0],
             [6, 2]],
            [[5, 1],
             [7, 3]]])
        actual = transform_shape(self.arr, (0, 0, -1), (-1, 0, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = np.array([
            [[2, 0],
             [3, 1]],
            [[6, 4],
             [7, 5]]])
        actual = transform_shape(self.arr, (0, 0, -1), (0, -1, 0))
        self.assertTrue(np.array_equal(expected, actual))

        expected = self.arr
        actual = transform_shape(self.arr, (0, 0, -1), (0, 0, -1))
        self.assertTrue(np.array_equal(expected, actual))

    def test_transform_shape_invalid_type(self):
        self.assertRaises(TypeError, lambda: transform_shape(None, None, None))
        self.assertRaises(TypeError, lambda: transform_shape(1, 1, 1))
        self.assertRaises(TypeError, lambda: transform_shape('string', 'string', 'string'))
        self.assertRaises(TypeError, lambda: transform_shape(self.arr, None, None))
        self.assertRaises(TypeError, lambda: transform_shape(self.arr, (0, 0, 0), None))
        self.assertRaises(TypeError, lambda: transform_shape(self.arr, None, (0, 0, 0)))
        self.assertRaises(TypeError, lambda: transform_shape(None, (1, 0, 0), (0, 1, 0)))
        self.assertRaises(TypeError, lambda: transform_shape(1, (1, 0, 0), (0, 1, 0)))
        self.assertRaises(TypeError, lambda: transform_shape('string', (1, 0, 0), (0, 1, 0)))

    def test_transform_shape_invalid_unimplemented(self):
        self.assertRaises(NotImplementedError, lambda: transform_shape(self.arr, (0, 0, 0), (0, 0, 0)))
        self.assertRaises(NotImplementedError, lambda: transform_shape(self.arr, (0, 2, 0), (1, 0, 0)))
        self.assertRaises(NotImplementedError, lambda: transform_shape(self.arr, (0, 1, 0), (0, 0, 2)))
        self.assertRaises(NotImplementedError, lambda: transform_shape(self.arr, (0, 2, 0), (1, 0, 0)))
        self.assertRaises(NotImplementedError, lambda: transform_shape(self.arr, (0, 0.5, 0.5), (1, 0, 0)))
        self.assertRaises(NotImplementedError, lambda: transform_shape(self.arr, (0, 1, 0), (0.3, 0.4, 0)))

    def test_transform_shape_invalid_index(self):
        self.assertRaises(IndexError, lambda: transform_shape(self.arr, (0, 0), (0, 0)))
        self.assertRaises(IndexError, lambda: transform_shape(self.arr, (0, 1), (0, 1)))
        self.assertRaises(IndexError, lambda: transform_shape(self.arr, (0, 1, 0), (0, 1)))
        self.assertRaises(IndexError, lambda: transform_shape(self.arr, (0, 1), (0, 0, 1)))
        self.assertRaises(IndexError, lambda: transform_shape(self.arr, (0, 1, 0), (0, 0, 0, 1)))
        self.assertRaises(IndexError, lambda: transform_shape(self.arr, (0, 1, 0, 0), (0, 0, 1)))
        self.assertRaises(IndexError, lambda: transform_shape(self.arr, (0, 1, 0, 0), (0, 0, 1, 0)))
