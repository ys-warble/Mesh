from unittest import TestCase

from WarbleSimulation.System.System import System
from WarbleSimulation.util import Logger
from WarbleSimulationTest import test_settings


class TestSystem(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = Logger.get_logger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger.info('')
        self.logger.info(test_settings.start_title_format(self._testMethodName))

        # Create a default system
        self.system_name = 'NewSystem'
        self.dimension = (5, 5, 5)
        self.resolution = 4

        self.system = System(name=self.system_name)

    def tearDown(self):
        self.logger.info(test_settings.end_title_format(self._testMethodName))
        self.logger.info('')

    def test_system_init(self):
        self.assertEqual(self.system_name, self.system.name)

    def test_put_space(self):
        self.system.put_space(dimension=self.dimension, resolution=self.resolution, space_factor_types=[])

    def test_put_entity(self):
        self.fail()

    def undefined_cases(self):
        self.system.put_space(dimension=self.dimension)
        self.system.put_space(dimension=self.dimension, space_factor_types=[])
        self.system.put_space(dimension=self.dimension, resolution=self.resolution)
