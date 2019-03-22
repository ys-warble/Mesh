from unittest import TestCase

from WarbleSimulation.util import Logger
from WarbleSimulationTest import test_settings


class AppTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = Logger.get_logger(cls.__module__ + '.' + cls.__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger.info('')
        self.logger.info(test_settings.start_title_format(self.__class__.__name__ + '.' + self._testMethodName))

    def tearDown(self):
        self.logger.info(test_settings.end_title_format(self.__class__.__name__ + '.' + self._testMethodName))
        self.logger.info('')
