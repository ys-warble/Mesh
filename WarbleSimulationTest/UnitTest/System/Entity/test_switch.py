import uuid
from unittest import TestCase

import numpy as np

from WarbleSimulation.System.Entity.Concrete.Switch import Switch
from WarbleSimulation.System.SpaceFactor import MatterType


class TestSwitch(TestCase):
    def setUp(self):
        super().setUp()
        self.power_supply = Switch(uuid=uuid.uuid4())

    def test_get_default_shape(self):
        m = MatterType.PLASTIC.value
        np.testing.assert_array_equal(self.power_supply.get_default_shape(), [[[m, m]]])
        self.assertEqual(self.power_supply.get_default_shape().shape, (1, 1, 2))
