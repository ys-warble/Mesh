import uuid

from WarbleSimulation.System.Entity.Concrete.Light import Light
from WarbleSimulation.System.Entity.Concrete.Table import Table
from WarbleSimulation.System.SpaceFactor import SpaceFactor
from WarbleSimulation.System.System import System
from WarbleSimulationTest.AppTestCase import AppTestCase


class TestSystem(AppTestCase):
    def setUp(self):
        super().setUp()

        # Create a default system
        self.system_name = 'NewSystem'
        self.dimension = (5, 5, 5)
        self.resolution = 4

        self.system = System(name=self.system_name)

    def test_system_init(self):
        self.assertEqual(self.system_name, self.system.name)

    def test_put_space(self):
        self.system.put_space(dimension=self.dimension, resolution=self.resolution, space_factor_types=[])

    def test_put_entity(self):
        # Put Space
        self.system.put_space(dimension=self.dimension, resolution=self.resolution,
                              space_factor_types=[SpaceFactor.MATTER])

        # Put Entity on the Space
        self.assertEqual(0, len(self.system.entities))

        table1 = Table(uuid=uuid.uuid4())
        self.system.put_entity(table1, (0, 0, 0))

        self.assertEqual(1, len(self.system.entities))
        self.assertTrue((table1, (0, 0, 0), None) in self.system.entities)

        light1 = Light(uuid=uuid.uuid4())
        self.system.put_entity(light1, (1, 1, 1))

        self.assertEqual(2, len(self.system.entities))
        self.assertTrue((table1, (0, 0, 0), None) in self.system.entities)
        self.assertTrue((light1, (1, 1, 1), None) in self.system.entities)

    def test_put_entity_invalid(self):
        # Put Entity on the Space
        table1 = Table(uuid=uuid.uuid4(), dimension_x=(1, 1, 1))
        self.assertRaises(AttributeError, lambda: self.system.put_entity(table1, (0, 0, 0)))

    def test_remove_entity(self):
        # Put Space
        self.system.put_space(dimension=self.dimension, resolution=self.resolution,
                              space_factor_types=[SpaceFactor.MATTER])

        # Put Entity on the Space
        table1 = Table(uuid=uuid.uuid4())
        self.system.put_entity(table1, (0, 0, 0))

        self.assertRaises(NotImplementedError, lambda: self.system.remove_entity(table1))

    def undefined_cases(self):
        self.system.put_space(dimension=self.dimension)
        self.system.put_space(dimension=self.dimension, space_factor_types=[])
        self.system.put_space(dimension=self.dimension, resolution=self.resolution)

