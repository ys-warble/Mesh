import uuid

import numpy as np

from WarbleSimulation.System.Entity.Concrete.Light import Light
from WarbleSimulation.System.Entity.Function import Function
from WarbleSimulation.System.Entity.Function.Powered import ElectricPower
from WarbleSimulation.System.Entity.Function.Tasked import TaskName, Status, ProgramTask, SystemTask, Task, TaskResponse
from WarbleSimulation.System.SpaceFactor import MatterType
from WarbleSimulationTest import test_settings
from WarbleSimulationTest.AppTestCase import AppTestCase


class TestLight(AppTestCase):
    def setUp(self):
        super().setUp()
        self.light = Light(uuid=uuid.uuid4())

    def tearDown(self):
        self.logger.info(test_settings.end_title_format(self._testMethodName))
        self.logger.info('')

    def test_get_default_shape(self):
        self.assertEqual(self.light.get_default_shape().shape, (3, 3, 3))
        matter = MatterType.GLASS.value
        np.testing.assert_array_equal(self.light.get_default_shape(),
                                      [[[0, 0, 0],
                                        [0, matter, 0],
                                        [0, 0, 0]],
                                       [[0, matter, 0],
                                        [matter, matter, matter],
                                        [0, matter, 0]],
                                       [[0, 0, 0],
                                        [0, matter, 0],
                                        [0, 0, 0]]])

    def test_send_task(self):
        # ProgramTask
        self.light.send_task(ProgramTask(name=TaskName.END))

        # SystemTask
        self.light.send_task(SystemTask(name=TaskName.ACTIVE))

        # EntityTask
        self.light.send_task(Task(name=TaskName.GET_INFO))

    def test_recv_task_resp(self):
        self.light.send_task(SystemTask(name=TaskName.SET_POWER, value={'power': ElectricPower(110)}))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        # ProgramTask
        self.light.send_task(ProgramTask(name=TaskName.END))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.ERROR, value={'error': 'Not Implemented'}))

        # SystemTask
        self.light.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        # EntityTask
        self.light.send_task(Task(name=TaskName.GET_INFO))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value={'info': {
                             'uuid': str(self.light.uuid),
                             'identifier': type(self.light).identifier,
                             'type': {
                                 'actuator': [
                                     'POWER'
                                 ],
                                 'sensor': [],
                                 'accessor': []
                             },
                         }}))

    def test_task_no_compute(self):
        self.light.send_task(SystemTask(name=TaskName.SET_POWER, value={'power': ElectricPower(110)}))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        # SystemTask
        self.light.send_task(SystemTask(name=TaskName.DEACTIVATE))
        self.assertFalse(self.light.active)
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        self.light.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertTrue(self.light.active)
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        self.light.send_task(SystemTask(name=TaskName.DEACTIVATE))
        self.assertFalse(self.light.active)
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        # EntityTask
        self.light.send_task(Task(name=TaskName.GET_INFO))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value={'info': {
                             'uuid': str(self.light.uuid),
                             'identifier': type(self.light).identifier,
                             'type': {
                                 'actuator': [
                                     'POWER'
                                 ],
                                 'sensor': [],
                                 'accessor': []
                             },
                         }}))

    def test_task_with_compute(self):
        self.light.send_task(SystemTask(name=TaskName.SET_POWER, value={'power': ElectricPower(110)}))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        # START COMPUTE
        self.light.send_task(ProgramTask(name=TaskName.START))
        self.light.recv_task_resp()

        # SystemTask
        self.light.send_task(SystemTask(name=TaskName.DEACTIVATE))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        self.light.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(self.light.recv_task_resp().value['system_info']['active'])

        self.light.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        self.light.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(self.light.recv_task_resp().value['system_info']['active'])

        self.light.send_task(SystemTask(name=TaskName.DEACTIVATE))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))
        self.light.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(self.light.recv_task_resp().value['system_info']['active'])

        # EntityTask
        self.light.send_task(Task(name=TaskName.GET_INFO))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value={'info': {
                             'uuid': str(self.light.uuid),
                             'identifier': type(self.light).identifier,
                             'type': {
                                 'actuator': [
                                     'POWER'
                                 ],
                                 'sensor': [],
                                 'accessor': []
                             },
                         }}))

        # END COMPUTE
        self.light.send_task(ProgramTask(name=TaskName.END))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        self.light.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertTrue(self.light.recv_task_resp().value['system_info']['active'])

        self.light.send_task(SystemTask(name=TaskName.SET_POWER, value={'power': ElectricPower(0)}))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        self.light.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(self.light.recv_task_resp().value['system_info']['active'])

    def test_light_1(self):
        def check_active(l_light, expected):
            if expected:
                self.assertTrue(l_light.active)
            else:
                self.assertFalse(l_light.active)

        light = Light(uuid=uuid.uuid4(), selected_functions=(Function.POWERED,))
        check_active(light, False)

        light.get_function(Function.POWERED).get_power_input().set_power(ElectricPower(110))
        check_active(light, True)

        light.get_function(Function.POWERED).get_power_input().set_power(ElectricPower(220))
        check_active(light, False)

    def test_light_2(self):
        def check_active(l_light, expected):
            if expected:
                self.assertTrue(l_light.active)
                light.send_task(SystemTask(TaskName.GET_SYSTEM_INFO))
                self.assertTrue(light.recv_task_resp().value['system_info']['active'])
            else:
                self.assertFalse(l_light.active)
                light.send_task(SystemTask(TaskName.GET_SYSTEM_INFO))
                self.assertFalse(light.recv_task_resp().value['system_info']['active'])

        light = Light(uuid=uuid.uuid4(), selected_functions=(Function.POWERED, Function.TASKED))
        check_active(light, False)

        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)

        light.get_function(Function.POWERED).get_power_input().set_power(ElectricPower(110))
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, True)

        light.get_function(Function.POWERED).get_power_input().set_power(ElectricPower(0))
        check_active(light, False)
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)

        light.get_function(Function.POWERED).get_power_input().set_power(ElectricPower(220))
        check_active(light, False)
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)

    def test_light_3(self):
        def check_active(l_light, expected):
            if expected:
                light.send_task(SystemTask(TaskName.GET_SYSTEM_INFO))
                self.assertTrue(light.recv_task_resp().value['system_info']['active'])
            else:
                light.send_task(SystemTask(TaskName.GET_SYSTEM_INFO))
                self.assertFalse(light.recv_task_resp().value['system_info']['active'])

        light = Light(uuid=uuid.uuid4(), selected_functions=(Function.POWERED, Function.TASKED, Function.COMPUTE))
        check_active(light, False)

        # Compute OFF
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)

        light.get_function(Function.POWERED).get_power_input().set_power(ElectricPower(110))
        light.recv_task_resp()
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, True)

        light.get_function(Function.POWERED).get_power_input().set_power(ElectricPower(0))
        check_active(light, False)
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)

        light.get_function(Function.POWERED).get_power_input().set_power(ElectricPower(220))
        check_active(light, False)
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)

        # Compute ON
        light.send_task(ProgramTask(TaskName.START))
        light.recv_task_resp()

        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)
        self.assertTrue(light.get_function(Function.COMPUTE).is_computing())

        light.send_task(SystemTask(name=TaskName.SET_POWER, value={'power': ElectricPower(110)}))
        light.recv_task_resp()
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, True)

        light.send_task(SystemTask(name=TaskName.SET_POWER, value={'power': ElectricPower(0)}))
        light.recv_task_resp()
        check_active(light, False)
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)

        light.send_task(SystemTask(name=TaskName.SET_POWER, value={'power': ElectricPower(220)}))
        light.recv_task_resp()
        check_active(light, False)
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)

        light.send_task(ProgramTask(TaskName.END))
        light.recv_task_resp()
