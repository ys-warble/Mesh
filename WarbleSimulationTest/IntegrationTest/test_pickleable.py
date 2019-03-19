import pickle
import uuid
from pickle import PicklingError
from unittest import TestCase

from WarbleSimulation.System.Entity.Concrete.Light import Light
from WarbleSimulation.System.Space import Space
from WarbleSimulation.System.SpaceFactor import SpaceFactor
from WarbleSimulation.System.System import System


class TestPickleable(TestCase):
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
