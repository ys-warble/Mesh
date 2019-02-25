from unittest import TestCase

from WarbleSimulation.System.Space import Space
from WarbleSimulation.System.SpaceFactor import SpaceFactor


class TestSpace(TestCase):
    def setUp(self):
        self.dimension = (5, 5, 5)
        self.resolution = 4

        self.space = Space(dimension=self.dimension,
                           space_factor_types=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER],
                           resolution=self.resolution)

    def tearDown(self):
        pass

    def test_constructor_valid_1(self):
        print('===== Running test_constructor_valid_1 =====')

        def func1():
            return Space(dimension=self.dimension,
                         resolution=self.resolution,
                         space_factor_types=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER])

        def func2():
            space = Space(dimension=self.dimension)
            return space

        self.assertTrue(isinstance(func1(), Space))
        self.assertTrue(isinstance(func2(), Space))

    def test_constructor_invalid_1(self):
        print('===== Running test_constructor_invalid_1 =====')

        def func2():
            space = Space(dimension=('5', 5, 5),
                          resolution=self.resolution,
                          space_factor_types=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER])

        def func3():
            space = Space(dimension=(5, '5', 5),
                          resolution=self.resolution,
                          space_factor_types=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER])

        def func4():
            space = Space(dimension=(5, 5, '5'),
                          resolution=self.resolution,
                          space_factor_types=['TEMPERATURE'])

        def func5():
            space = Space(dimension=self.dimension,
                          resolution='1',
                          space_factor_types=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER])

        def func6():
            space = Space(dimension=(5, 5, 5, 5, 5),
                          resolution='1',
                          space_factor_types=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER])

        self.assertRaises(TypeError, func2)
        self.assertRaises(TypeError, func3)
        self.assertRaises(TypeError, func4)
        self.assertRaises(TypeError, func5)
        self.assertRaises(IndexError, func6)

    def test_add_space_factor_valid_single(self):
        print('===== Running test_add_space_factor_valid_single =====')

        total_space_factor = len(self.space.space_factors)
        space_factor_types = list(self.space.space_factors.keys())

        self.space.add_space_factor(SpaceFactor.AIR_MOVEMENT)
        self.space.add_space_factor(SpaceFactor.HUMIDITY)
        total_space_factor += 2
        space_factor_types.append(SpaceFactor.AIR_MOVEMENT)
        space_factor_types.append(SpaceFactor.HUMIDITY)

        self.assertEqual(total_space_factor, len(self.space.space_factors))
        self.assertEqual(space_factor_types, list(self.space.space_factors.keys()))

        for a, b in self.space.space_factors.items():
            for c, d in b.items():
                self.assertEqual(tuple([i * self.resolution for i in self.dimension]), d.shape)

    def test_add_space_factor_valid_list(self):
        print('===== Running test_add_space_factor_valid_list =====')

        total_space_factor = len(self.space.space_factors)
        space_factor_types = list(self.space.space_factors.keys())

        self.space.add_space_factor([SpaceFactor.AIR_MOVEMENT, SpaceFactor.HUMIDITY, SpaceFactor.LUMINOSITY])
        self.space.add_space_factor([])
        total_space_factor += 3
        space_factor_types.append(SpaceFactor.AIR_MOVEMENT)
        space_factor_types.append(SpaceFactor.HUMIDITY)
        space_factor_types.append(SpaceFactor.LUMINOSITY)

        self.assertEqual(total_space_factor, len(self.space.space_factors))
        self.assertEqual(space_factor_types, list(self.space.space_factors.keys()))

        for a, b in self.space.space_factors.items():
            for c, d in b.items():
                self.assertEqual(tuple([i * self.resolution for i in self.dimension]), d.shape)

    def test_add_space_factor_invalid_single(self):
        print('===== Running test_add_space_factor_invalid_single =====')

        def func1():
            self.space.add_space_factor(1)

        def func2():
            self.space.add_space_factor(['HUMIDITY'])

        self.assertRaises(TypeError, func1)
        self.assertRaises(TypeError, func2)

    def test_add_space_factor_invalid_list(self):
        print('===== Running test_add_space_factor_invalid_list =====')

        def func1():
            self.space.add_space_factor([1, 2, 3])

        def func2():
            self.space.add_space_factor(['HUMIDITY', 'AIR_MOVEMENT'])

        self.assertRaises(TypeError, func1)
        self.assertRaises(TypeError, func2)

    # TODO: Test data types
