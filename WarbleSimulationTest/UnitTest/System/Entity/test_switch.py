import uuid
from unittest import TestCase

import numpy as np

from WarbleSimulation.System.Entity.Concrete.Switch import Switch
from WarbleSimulation.System.SpaceFactor import MatterType
from WarbleSimulation.util import Logger
from WarbleSimulationTest import test_settings


class TestSwitch(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = Logger.get_logger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger.info('')
        self.logger.info(test_settings.start_title_format(self._testMethodName))

        self.power_supply = Switch(uuid=uuid.uuid4())

    def tearDown(self):
        self.logger.info(test_settings.end_title_format(self._testMethodName))
        self.logger.info('')

    def test_get_default_shape(self):
        m = MatterType.PLASTIC.value
        np.testing.assert_array_equal(self.power_supply.get_default_shape(), [[[m, m]]])
        self.assertEqual(self.power_supply.get_default_shape().shape, (1, 1, 2))
