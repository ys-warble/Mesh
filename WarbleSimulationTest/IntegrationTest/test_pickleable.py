import pickle
import uuid
from pickle import PicklingError
from unittest import TestCase

from WarbleSimulation.System.Entity.Concrete.Light import Light
from WarbleSimulation.System.Space import Space
from WarbleSimulation.System.SpaceFactor import SpaceFactor
from WarbleSimulation.System.System import System
from WarbleSimulation.util import Logger
from WarbleSimulationTest import test_settings


class TestPickleable(TestCase):
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

    def test_space(self):
        space = Space((5, 5, 5), space_factor_types=[i for i in SpaceFactor])

        try:
            pickle.dumps(space)
        except PicklingError:
            self.fail('Space is NOT pickable')

    def test_light(self):
        light = Light(uuid=uuid.uuid4())

        try:
            pickle.dumps(light)
        except PicklingError:
            self.fail('Space is NOT pickable')

    def test_system(self):
        system = System(name='MyNewSystem')
        system.put_space((5, 5, 5), space_factor_types=[i for i in SpaceFactor])

        light = Light(uuid=uuid.uuid4())
        system.put_entity(light, (0, 0, 0))

        try:
            pickle.dumps(system)
        except PicklingError:
            self.fail('Space is NOT pickable')
