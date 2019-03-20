import os
import uuid
from multiprocessing import Process, Pipe, Queue
from unittest import TestCase

import numpy as np

import WarbleSimulation.System.SpaceFactor as SpaceFactor
import WarbleSimulation.util.numpy_ext as npx
from WarbleSimulation.System.Entity.Concrete.AirConditioner import AirConditioner
from WarbleSimulation.System.Entity.Concrete.Chair import Chair
from WarbleSimulation.System.Entity.Concrete.Human import Human
from WarbleSimulation.System.Entity.Concrete.Light import Light
from WarbleSimulation.System.Entity.Concrete.SmokeDetector import SmokeDetector
from WarbleSimulation.System.Entity.Concrete.Table import Table
from WarbleSimulation.System.Entity.Concrete.Thermostat import Thermostat
from WarbleSimulation.System.Entity.Concrete.Wall import Wall
from WarbleSimulation.System.Entity.Concrete.Wardrobe import Wardrobe
from WarbleSimulation.System.Entity.Task import Task, Command
from WarbleSimulation.System.System import System
from WarbleSimulation.util import Logger, Plotter
from WarbleSimulationTest import test_settings


class TestMain(TestCase):
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

    def test_main(self):
        # Create System
        self.system = System('MyNewSystem')

        # Put Space on the System
        self.system.put_space(dimension=(40, 30, 12), resolution=1,
                              space_factor_types=[i for i in SpaceFactor.SpaceFactor])

        # Put Entity on the Space
        light1 = Light(uuid=uuid.uuid4(), dimension_x=(1, 1, 1))
        self.system.put_entity(light1, (19, 14, 9))
        light2 = Light(uuid=uuid.uuid4(), dimension_x=(1, 1, 1))
        self.system.put_entity(light2, (9, 14, 9))
        light3 = Light(uuid=uuid.uuid4(), dimension_x=(1, 1, 1))
        self.system.put_entity(light3, (29, 14, 9))

        # Multiprocessing Init
        mp = {}
        result_queue = Queue()

        for entity, dimension, orientation in self.system.entities:
            if entity.runnable is True:
                p_pipe, c_pipe = Pipe()
                process = Process(target=entity.run, args=(result_queue, c_pipe))
                mp[entity] = {
                    'p_pipe': p_pipe,
                    'c_pipe': c_pipe,
                    'process': process,
                }

        # Multiprocessing Start
        for entity in mp:
            mp[entity]['process'].start()

        # Multiprocessing Do
        for entity_process in mp:
            task = Task(command=Command.ACTIVE)
            mp[entity_process]['p_pipe'].send(task)
        for entity_process in mp:
            task = Task(command=Command.GET_INFO)
            mp[entity_process]['p_pipe'].send(task)

        # Multiprocessing End
        for entity_process in mp:
            task = Task(command=Command.END)
            mp[entity_process]['p_pipe'].send(task)
            mp[entity_process]['process'].join()

    def test_main_1(self):
        # Create System
        self.system = System('MyNewSystem')

        # Put Space on the System
        self.system.put_space(dimension=(20, 10, 5), resolution=4,
                              space_factor_types=[i for i in SpaceFactor.SpaceFactor])
        self.logger.info('\n' + str(self.system.space))

        # Put Entity on the Space
        # Put Walls
        wall_1 = Wall(uuid=uuid.uuid4(), dimension_x=(20, 0.25, 5))
        self.system.put_entity(wall_1, (0, 9.75, 0))
        wall_2 = Wall(uuid=uuid.uuid4(), dimension_x=(20, 0.25, 5))
        self.system.put_entity(wall_2, (0, 0, 0))
        wall_3 = Wall(uuid=uuid.uuid4(), dimension_x=(0.25, 9.5, 5))
        self.system.put_entity(wall_3, (0, 0.25, 0))
        wall_4 = Wall(uuid=uuid.uuid4(), dimension_x=(0.25, 9.5, 5))
        self.system.put_entity(wall_4, (19.75, 0.25, 0))

        # Compare Space Factor Matter
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_matter.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER])
        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_matter.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER])

        # Plot
        Plotter.plot_scatter_3d(
            array3d=self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER],
            zero_value=SpaceFactor.MatterType.ATMOSPHERE.value,
            filename=os.path.join(test_settings.actual_path, self._testMethodName + '_matter_plot.html'),
            auto_open=test_settings.auto_open)

    def test_main_2(self):
        # Create System
        self.system = System('MyNewSystem')

        # Put Space on the System
        self.system.put_space(dimension=(40, 30, 10), resolution=1,
                              space_factor_types=[i for i in SpaceFactor.SpaceFactor])

        # Put Entity on the Space
        table1 = Table(uuid=uuid.uuid4(), dimension_x=(2, 1, 1))
        self.system.put_entity(table1, (0, 0, 0))
        light1 = Light(uuid=uuid.uuid4(), dimension_x=(1, 1, 1))
        self.system.put_entity(light1, (19, 14, 7))
        ac1 = AirConditioner(uuid=uuid.uuid4())
        self.system.put_entity(ac1, (37, 10, 7), unit_orientation=(-1, 0, 0))
        sd1 = SmokeDetector(uuid=uuid.uuid4())
        self.system.put_entity(sd1, (0, 10, 8), unit_orientation=(1, 0, 0))
        thermostat1 = Thermostat(uuid=uuid.uuid4())
        self.system.put_entity(thermostat1, (30, 0, 5))

        # Compare Space Factor Matter
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_matter.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER])
        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_matter.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER])

        # Plot
        Plotter.plot_scatter_3d(
            array3d=self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER],
            zero_value=SpaceFactor.MatterType.ATMOSPHERE.value,
            filename=os.path.join(test_settings.actual_path, self._testMethodName + '_matter_plot.html'),
            auto_open=test_settings.auto_open)

    def test_main_3(self):
        # Create System
        self.system = System('MyNewSystem')

        # Put Space on the System
        self.system.put_space(dimension=(40, 30, 12), resolution=1,
                              space_factor_types=[i for i in SpaceFactor.SpaceFactor])

        # Put Entity on the Space
        table1 = Table(uuid=uuid.uuid4(), dimension_x=(2, 1, 1))
        light1 = Light(uuid=uuid.uuid4(), dimension_x=(1, 1, 1))
        ac1 = AirConditioner(uuid=uuid.uuid4())
        sd1 = SmokeDetector(uuid=uuid.uuid4())
        thermostat1 = Thermostat(uuid=uuid.uuid4())
        ch1 = Chair(uuid=uuid.uuid4())
        h1 = Human(uuid=uuid.uuid4())
        w1 = Wardrobe(uuid=uuid.uuid4())

        self.system.put_entity(table1, (0, 0, 0))
        self.system.put_entity(light1, (19, 14, 9))
        self.system.put_entity(ac1, (37, 10, 9), unit_orientation=(-1, 0, 0))
        self.system.put_entity(sd1, (10, 10, 11), unit_orientation=(0, 0, -1))
        self.system.put_entity(thermostat1, (30, 0, 5))
        self.system.put_entity(ch1, (4, 4, 0), unit_orientation=(0, -1, 0))
        self.system.put_entity(h1, (25, 20, 0), unit_orientation=(0, -1, 0))
        self.system.put_entity(w1, (0, 20, 0), unit_orientation=(1, 0, 0))

        # Compare Space Factors
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_matter.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER])
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_temperature.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.TEMPERATURE][
                    SpaceFactor.Temperature.TEMPERATURE])
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_humidity.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.HUMIDITY][SpaceFactor.Humidity.HUMIDITY])
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_hue.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.HUE])
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_saturation.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.SATURATION])
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_brightness.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS])
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_air_x.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.X])
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_air_y.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.Y])
        np.save(os.path.join(test_settings.actual_path, self._testMethodName + '_space_air_z.npy'),
                self.system.space.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.Z])

        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_matter.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER])
        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_temperature.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.TEMPERATURE][SpaceFactor.Temperature.TEMPERATURE])
        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_humidity.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.HUMIDITY][SpaceFactor.Humidity.HUMIDITY])
        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_hue.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.HUE])
        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_saturation.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.SATURATION])
        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_brightness.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS])
        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_air_x.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.X])
        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_air_y.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.Y])
        np.testing.assert_array_equal(
            np.load(os.path.join(test_settings.expected_path, self._testMethodName + '_space_air_z.npy')),
            self.system.space.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.Z])

        # Plot
        Plotter.plot_scatter_3d(
            array3d=self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER],
            zero_value=SpaceFactor.MatterType.ATMOSPHERE.value,
            filename=os.path.join(test_settings.actual_path, self._testMethodName + '_matter_plot.html'),
            auto_open=test_settings.auto_open)

        x_dark, y_dark, z_dark = (self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][
                                      SpaceFactor.Matter.MATTER] > 300).nonzero()
        for i in range(len(x_dark)):
            self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS][
                x_dark[i], y_dark[i], z_dark[i]] = 0

        self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS][0:3,
        20:25, 0:7] = 0
        self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS][0:9, 0:3,
        0:3] = 0

        luminosity = npx.char.mod('hsl(%d,%d%,%d%)', (
            self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.HUE],
            self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.SATURATION],
            self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS]))

        Plotter.plot_scatter_3d(
            array3d=luminosity,
            zero_value=-1,
            filename=os.path.join(test_settings.actual_path, self._testMethodName + '_luminosity_plot.html'),
            auto_open=test_settings.auto_open,
            opacity=0.6
        )
