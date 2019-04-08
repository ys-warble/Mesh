import os
import uuid

import numpy as np

import Mesh.System.SpaceFactor as SpaceFactor
import Mesh.util.numpy_ext as npx
from Mesh.System.Entity.Channel.PowerWire import PowerWire
from Mesh.System.Entity.Concrete.AirConditioner import AirConditioner
from Mesh.System.Entity.Concrete.Chair import Chair
from Mesh.System.Entity.Concrete.Human import Human
from Mesh.System.Entity.Concrete.Light import Light
from Mesh.System.Entity.Concrete.PowerSupply import PowerSupply
from Mesh.System.Entity.Concrete.SmokeDetector import SmokeDetector
from Mesh.System.Entity.Concrete.Switch import Switch
from Mesh.System.Entity.Concrete.Table import Table
from Mesh.System.Entity.Concrete.Thermostat import Thermostat
from Mesh.System.Entity.Concrete.Wall import Wall
from Mesh.System.Entity.Concrete.Wardrobe import Wardrobe
from Mesh.System.Entity.Function import Function
from Mesh.System.Entity.Function.Tasked import SystemTask, TaskName, TaskResponse, Status
from Mesh.System.System import System
from Mesh.util import Plotter
from MeshTest import test_settings
from MeshTest.AppTestCase import AppTestCase


class TestMain(AppTestCase):
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

        light1.destroy()

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

        light1.destroy()

    def test_main_5(self):
        # Create System
        self.system = System('MyNewSystem')

        # Put Space on the System
        self.system.put_space(dimension=(40, 30, 12), resolution=1,
                              space_factor_types=[i for i in SpaceFactor.SpaceFactor])

        # Put Entity on the Space
        power_supply = PowerSupply(uuid=uuid.uuid4())
        light_switch1 = Switch(uuid=uuid.uuid4())
        wire_ls1 = PowerWire(power_supply, light_switch1)
        light1 = Light(uuid=uuid.uuid4())
        wire_l1 = PowerWire(light_switch1, light1)

        self.system.put_entity(power_supply, (19, 14, 9))
        self.system.put_entity(light_switch1, (19, 14, 9))
        self.system.put_entity(light1, (9, 14, 9))

        power_supply.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(power_supply.recv_task_resp().value['system_info']['active'])
        light_switch1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light_switch1.recv_task_resp().value['system_info']['active'])
        light1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light1.recv_task_resp().value['system_info']['active'])

        # Turn On PowerSupply
        power_supply.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertEqual(TaskResponse(status=Status.OK, value=None), power_supply.recv_task_resp())

        power_supply.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(power_supply.recv_task_resp().value['system_info']['active'])
        light_switch1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light_switch1.recv_task_resp().value['system_info']['active'])
        light1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light1.recv_task_resp().value['system_info']['active'])

        # Turn On Switch
        light_switch1.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertEqual(TaskResponse(status=Status.OK, value=None), light_switch1.recv_task_resp())

        power_supply.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(power_supply.recv_task_resp().value['system_info']['active'])
        light_switch1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(light_switch1.recv_task_resp().value['system_info']['active'])
        light1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light1.recv_task_resp().value['system_info']['active'])

        # Turn On Light
        light1.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertEqual(TaskResponse(status=Status.OK, value=None), light1.recv_task_resp())

        power_supply.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(power_supply.recv_task_resp().value['system_info']['active'])
        light_switch1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(light_switch1.recv_task_resp().value['system_info']['active'])
        light1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(light1.recv_task_resp().value['system_info']['active'])

        power_supply.destroy()
        light_switch1.destroy()
        light1.destroy()

    def test_main_6(self):
        # Create System
        self.system = System('MyNewSystem')

        # Put Space on the System
        self.system.put_space(dimension=(40, 30, 12), resolution=1,
                              space_factor_types=[i for i in SpaceFactor.SpaceFactor])

        # Put Entity on the Space
        power_supply = PowerSupply(uuid=uuid.uuid4())
        light_switch1 = Switch(uuid=uuid.uuid4())
        wire_ls1 = PowerWire(power_supply, light_switch1)
        light1 = Light(uuid=uuid.uuid4(), selected_functions=(Function.POWERED,))
        wire_l1 = PowerWire(light_switch1, light1)

        light_switch2 = Switch(uuid=uuid.uuid4())
        wire_ls2 = PowerWire(power_supply, light_switch2)
        light2 = Light(uuid=uuid.uuid4(), selected_functions=(Function.POWERED,))
        wire_l2 = PowerWire(light_switch2, light2)

        power_supply.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(power_supply.recv_task_resp().value['system_info']['active'])
        light_switch1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light_switch1.recv_task_resp().value['system_info']['active'])
        self.assertFalse(light1.active)
        light_switch2.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light_switch2.recv_task_resp().value['system_info']['active'])
        self.assertFalse(light2.active)

        # Turn On PowerSupply
        power_supply.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertEqual(TaskResponse(status=Status.OK, value=None), power_supply.recv_task_resp())

        power_supply.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(power_supply.recv_task_resp().value['system_info']['active'])
        light_switch1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light_switch1.recv_task_resp().value['system_info']['active'])
        self.assertFalse(light1.active)
        light_switch2.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light_switch2.recv_task_resp().value['system_info']['active'])
        self.assertFalse(light2.active)

        # Turn On Switch
        light_switch1.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertEqual(TaskResponse(status=Status.OK, value=None), light_switch1.recv_task_resp())

        power_supply.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(power_supply.recv_task_resp().value['system_info']['active'])
        light_switch1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(light_switch1.recv_task_resp().value['system_info']['active'])
        self.assertTrue(light1.active)
        light_switch2.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light_switch2.recv_task_resp().value['system_info']['active'])
        self.assertFalse(light2.active)

        light_switch2.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertEqual(TaskResponse(status=Status.OK, value=None), light_switch2.recv_task_resp())

        power_supply.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(power_supply.recv_task_resp().value['system_info']['active'])
        light_switch1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(light_switch1.recv_task_resp().value['system_info']['active'])
        self.assertTrue(light1.active)
        light_switch2.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(light_switch2.recv_task_resp().value['system_info']['active'])
        self.assertTrue(light2.active)

        # Turn Off Switch
        light_switch1.send_task(SystemTask(name=TaskName.DEACTIVATE))
        self.assertEqual(TaskResponse(status=Status.OK, value=None), light_switch1.recv_task_resp())

        power_supply.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(power_supply.recv_task_resp().value['system_info']['active'])
        light_switch1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light_switch1.recv_task_resp().value['system_info']['active'])
        self.assertFalse(light1.active)
        light_switch2.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(light_switch2.recv_task_resp().value['system_info']['active'])
        self.assertTrue(light2.active)

        light_switch2.send_task(SystemTask(name=TaskName.DEACTIVATE))
        self.assertEqual(TaskResponse(status=Status.OK, value=None), light_switch2.recv_task_resp())

        power_supply.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(power_supply.recv_task_resp().value['system_info']['active'])
        light_switch1.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light_switch1.recv_task_resp().value['system_info']['active'])
        self.assertFalse(light1.active)
        light_switch2.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(light_switch2.recv_task_resp().value['system_info']['active'])
        self.assertFalse(light2.active)

        power_supply.destroy()
        light_switch1.destroy()
        light_switch2.destroy()
        light1.destroy()
        light2.destroy()
