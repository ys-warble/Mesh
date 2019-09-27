import json
import os
import uuid

from Mesh.System import SpaceFactor
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
from Mesh.System.Entity.Concrete.Wardrobe import Wardrobe
from Mesh.System.Entity.Function.Tasked import TaskName, SystemTask
from Mesh.System.System import System
from Mesh.util import Plotter
from MeshTest import test_settings
from MeshTest.AppTestCase import AppTestCase

import Mesh.util.numpy_ext as npx


class TestDevelopment(AppTestCase):
    def setUp(self):
        self.logger.info('')
        self.logger.info(test_settings.start_title_format(self.__class__.__name__ + '.' + self._testMethodName))

    def tearDown(self):
        self.logger.info(test_settings.end_title_format(self.__class__.__name__ + '.' + self._testMethodName))
        self.logger.info('')

    def test_dev(self):
        # Create System
        self.system = System('MyNewSystem')

        # Put Space on the System
        self.system.put_space(dimension=(40, 30, 12), resolution=1,
                              space_factor_types=[i for i in SpaceFactor.SpaceFactor], default_value=True)

        # Put Entity on the Space
        power_supply = PowerSupply(uuid=uuid.uuid4())
        light_switch1 = Switch(uuid=uuid.uuid4())
        wire_ls1 = PowerWire(power_supply, light_switch1)
        light1 = Light(uuid=uuid.uuid4())
        wire_l1 = PowerWire(light_switch1, light1)

        light_switch2 = Switch(uuid=uuid.uuid4())
        wire_ls2 = PowerWire(power_supply, light_switch2)
        light2 = Light(uuid=uuid.uuid4())
        wire_l2 = PowerWire(light_switch2, light2)

        # wall1 = Wall(uuid=uuid.uuid4(), dimension_x=(2, 10, 12))
        table1 = Table(uuid=uuid.uuid4(), dimension_x=(2, 1, 1))
        ac1 = AirConditioner(uuid=uuid.uuid4())
        sd1 = SmokeDetector(uuid=uuid.uuid4())
        thermostat1 = Thermostat(uuid=uuid.uuid4())
        ch1 = Chair(uuid=uuid.uuid4())
        h1 = Human(uuid=uuid.uuid4())
        w1 = Wardrobe(uuid=uuid.uuid4())

        self.system.put_entity(power_supply, (0, 0, 0))
        self.system.put_entity(light_switch1, (19, 0, 5))
        self.system.put_entity(light1, (9, 14, 9))
        self.system.put_entity(light_switch2, (21, 0, 5))
        self.system.put_entity(light2, (29, 14, 9))
        # self.system.put_entity(wall1, (5, 20, 0))
        self.system.put_entity(table1, (0, 0, 0))
        self.system.put_entity(ac1, (37, 22, 9), unit_orientation=(-1, 0, 0))
        self.system.put_entity(sd1, (19, 20, 11), unit_orientation=(0, 0, -1))
        self.system.put_entity(thermostat1, (30, 0, 5))
        self.system.put_entity(ch1, (4, 4, 0), unit_orientation=(0, -1, 0))
        self.system.put_entity(h1, (25, 20, 0), unit_orientation=(0, -1, 0))
        self.system.put_entity(w1, (0, 20, 0), unit_orientation=(1, 0, 0))

        # # PLOT LUMINOSITY
        # luminosity = npx.char.mod('hsl(%d,%d%,%d%)', (
        #     self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.HUE],
        #     self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.SATURATION],
        #     self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS]))
        # Plotter.plot_scatter_3d(
        #     array3d=luminosity,
        #     zero_value=-1,
        #     filename=os.path.join(test_settings.actual_path, self._testMethodName + '_luminosity_plot1.html'),
        #     auto_open=True,
        #     opacity=0.4
        # )

        power_supply.send_task(SystemTask(TaskName.ACTIVE))
        light_switch1.send_task(SystemTask(TaskName.ACTIVE))
        light1.send_task(SystemTask(TaskName.ACTIVE))
        light1.send_task(SystemTask(TaskName.ACTUATE, value={'space': self.system.space,
                                                             'location': self.system.entities[2][1],
                                                             'orientation': self.system.entities[2][1]}))
        res1 = light1.recv_task_resp()

        light_switch2.send_task(SystemTask(TaskName.ACTIVE))
        light2.send_task(SystemTask(TaskName.ACTIVE))
        light2.send_task(SystemTask(TaskName.ACTUATE, value={'space': self.system.space,
                                                             'location': self.system.entities[4][1],
                                                             'orientation': self.system.entities[4][1]}))
        res2 = light2.recv_task_resp()

        spacefactor_modifier = SpaceFactor.SpaceFactorModifier(selected_space_factors=(SpaceFactor.SpaceFactor.LUMINOSITY,))
        spacefactor_modifier.spacefactor_operators[SpaceFactor.SpaceFactor.LUMINOSITY] = SpaceFactor.LuminosityOperation()
        spacefactor_modifier.modify(self.system.space.space_factors, [res1.value, res2.value])

        # # PLOT LUMINOSITY
        # luminosity = npx.char.mod('hsl(%d,%d%,%d%)', (
        #     self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.HUE],
        #     self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.SATURATION],
        #     self.system.space.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS]))
        # Plotter.plot_scatter_3d(
        #     array3d=luminosity,
        #     zero_value=-1,
        #     filename=os.path.join(test_settings.actual_path, self._testMethodName + '_luminosity_plot2.html'),
        #     auto_open=True,
        #     opacity=0.4
        # )

        self.system.space.plot()

        print(self.system.to_json())
        with open('system.json', 'w') as file:
            json.dump(self.system.to_json(), file, indent=2)

        light1.destroy()
        light2.destroy()
