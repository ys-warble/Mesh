from unittest import TestCase

from WarbleSimulation.System.Space import Space, SpaceFactor


class TestSpace(TestCase):
    def setUp(self):
        self.space = Space(name='MySpace', x=100, y=200, z=300,
                           space_factors=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER],
                           resolution=1)

    def tearDown(self):
        pass

    def test_constructor_valid_1(self):
        space = Space(name='MySpace', x=100, y=200, z=300, space_factors=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER],
                      resolution=1)

        self.assertTrue(isinstance(space, Space))

    def test_constructor_invalid_1(self):
        def func1():
            space = Space(name=1, x=100, y=200, z=300, space_factors=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER],
                          resolution=1)

        def func2():
            space = Space(name='MySpace', x='100', y=200, z=300,
                          space_factors=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER],
                          resolution=1)

        def func3():
            space = Space(name='MySpace', x=100, y='200', z=300,
                          space_factors=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER],
                          resolution=1)

        def func4():
            space = Space(name='MySpace', x=100, y=200, z='300', space_factors=['TEMPERATURE'],
                          resolution=1)

        def func5():
            space = Space(name='MySpace', x=100, y=200, z=300,
                          space_factors=[SpaceFactor.TEMPERATURE, SpaceFactor.MATTER],
                          resolution='100')

        self.assertRaises(TypeError, func1)
        self.assertRaises(TypeError, func2)
        self.assertRaises(TypeError, func3)
        self.assertRaises(TypeError, func4)
        self.assertRaises(TypeError, func5)

    def test_add_space_factor_valid_single(self):
        self.space.add_space_factor(SpaceFactor.AIR_MOVEMENT)
        self.space.add_space_factor(SpaceFactor.HUMIDITY)

    def test_add_space_factor_valid_list(self):
        self.space.add_space_factor([SpaceFactor.AIR_MOVEMENT, SpaceFactor.HUMIDITY, SpaceFactor.LUMINOSITY])
        self.space.add_space_factor([])

    def test_add_space_factor_invalid_single(self):
        def func1():
            self.space.add_space_factor(1)

        def func2():
            self.space.add_space_factor(['HUMIDITY'])

        self.assertRaises(TypeError, func1)
        self.assertRaises(TypeError, func2)

    def test_add_space_factor_invalid_list(self):
        def func1():
            self.space.add_space_factor([1, 2, 3])

        def func2():
            self.space.add_space_factor(['HUMIDITY', 'AIR_MOVEMENT'])

        self.assertRaises(TypeError, func1)
        self.assertRaises(TypeError, func2)
