import filecmp
import os
import uuid
from unittest import TestCase

import WarbleSimulation.System.SpaceFactor as SpaceFactor
import WarbleSimulation.util.mynumpy as mynp
from WarbleSimulation.System.Entity.Concrete.AirConditioner import AirConditioner
from WarbleSimulation.System.Entity.Concrete.Chair import Chair
from WarbleSimulation.System.Entity.Concrete.Human import Human
from WarbleSimulation.System.Entity.Concrete.Light import Light
from WarbleSimulation.System.Entity.Concrete.SmokeDetector import SmokeDetector
from WarbleSimulation.System.Entity.Concrete.Table import Table
from WarbleSimulation.System.Entity.Concrete.Thermostat import Thermostat
from WarbleSimulation.System.Entity.Concrete.Wall import Wall
from WarbleSimulation.System.Entity.Concrete.Wardrobe import Wardrobe
from WarbleSimulation.System.System import System
from WarbleSimulation.util import Logger, Plotter
from WarbleSimulationTest import test_settings


class TestMain(TestCase):
    def setUp(self):
        self.logger = Logger.get_logger(__name__)

    def test_main(self):
        test_name = 'test_main'

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

    def test_main_1(self):
        test_name = 'test_main_1'

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
        self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_matter.txt'))
        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_matter.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_matter.txt')))

        # Plot
        Plotter.plot_scatter_3d(
            array3d=self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER],
            zero_value=SpaceFactor.MatterType.ATMOSPHERE.value,
            filename=os.path.join(test_settings.actual_path, test_name + '_matter_plot.html'),
            auto_open=test_settings.auto_open)

    def test_main_2(self):
        test_name = 'test_main_2'

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
        self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_matter.txt'))
        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_matter.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_matter.txt')))

        # Plot
        Plotter.plot_scatter_3d(
            array3d=self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER],
            zero_value=SpaceFactor.MatterType.ATMOSPHERE.value,
            filename=os.path.join(test_settings.actual_path, test_name + '_matter_plot.html'),
            auto_open=test_settings.auto_open)

    def test_main_3(self):
        test_name = 'test_main_3'

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
        self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_matter.txt'))
        self.system.space.space_factors[SpaceFactor.SpaceFactor.TEMPERATURE][
            SpaceFactor.Temperature.TEMPERATURE].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_temperature.txt'))
        self.system.space.space_factors[SpaceFactor.SpaceFactor.HUMIDITY][SpaceFactor.Humidity.HUMIDITY].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_humidity.txt'))
        self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.HUE].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_hue.txt'))
        self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.SATURATION].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_saturation.txt'))
        self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_brightness.txt'))
        self.system.space.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.X].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_air_x.txt'))
        self.system.space.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.Y].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_air_y.txt'))
        self.system.space.space_factors[SpaceFactor.SpaceFactor.AIR_MOVEMENT][SpaceFactor.AirMovement.Z].tofile(
            os.path.join(test_settings.actual_path, test_name + '_space_air_z.txt'))

        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_matter.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_matter.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_temperature.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_temperature.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_humidity.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_humidity.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_hue.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_hue.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_saturation.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_saturation.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_brightness.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_brightness.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_air_x.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_air_x.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_air_y.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_air_y.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(test_settings.expected_path, test_name + '_space_air_z.txt'),
                                    os.path.join(test_settings.actual_path, test_name + '_space_air_z.txt')))

        # Plot
        Plotter.plot_scatter_3d(
            array3d=self.system.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER],
            zero_value=SpaceFactor.MatterType.ATMOSPHERE.value,
            filename=os.path.join(test_settings.actual_path, test_name + '_matter_plot.html'),
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

        luminosity = mynp.char.mod('hsl(%d,%d%,%d%)', (
        self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.HUE],
        self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.SATURATION],
        self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS]))

        Plotter.plot_scatter_3d(
            array3d=luminosity,
            zero_value=-1,
            filename=os.path.join(test_settings.actual_path, test_name + '_luminosity_plot.html'),
            auto_open=test_settings.auto_open,
            opacity=0.6
        )
