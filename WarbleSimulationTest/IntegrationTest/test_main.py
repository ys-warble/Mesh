import uuid
from unittest import TestCase

import WarbleSimulation.System.SpaceFactor as SpaceFactor
from WarbleSimulation.System.Entity.Wall import Wall
from WarbleSimulation.System.System import System
from WarbleSimulation.util import Logger


class TestMain(TestCase):
    def setUp(self):
        self.logger = Logger.get_logger(__name__)

    def test_main(self):
        # Create System
        self.system = System('MyNewSystem')

        # Put Space on the System
        self.system.put_space(dimension=(20, 10, 5), resolution=4,
                              space_factor_types=[i for i in SpaceFactor.SpaceFactor])
        self.logger.info('\n' + str(self.system.space))

        # Put Entity on the Space
        # Put Walls
        wall_1 = Wall(uuid=uuid.uuid4(), dimension=(3, 1, 5))
        self.system.put_entity(wall_1, (1, 1, 1), (1, 0, 0))
