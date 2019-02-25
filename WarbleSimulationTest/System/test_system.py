from unittest import TestCase

from WarbleSimulation.System.System import System


class TestSystem(TestCase):
    def setUp(self):
        self.system_name = 'NewSystem'
        self.dimension = (5, 5, 5)
        self.resolution = 4

        self.system = System(name=self.system_name)

    def tearDown(self):
        pass

    def test_system_init(self):
        self.assertEqual(self.system_name, self.system.name)

    def test_put_space(self):
        self.system.put_space(dimension=self.dimension, resolution=self.resolution, space_factor_types=[])

    def test_init_normal_space(self):
        self.fail()

    def test_put_entity(self):
        self.fail()

    def undefined_cases(self):
        self.system.put_space(dimension=self.dimension)
        self.system.put_space(dimension=self.dimension, space_factor_types=[])
        self.system.put_space(dimension=self.dimension, resolution=self.resolution)
