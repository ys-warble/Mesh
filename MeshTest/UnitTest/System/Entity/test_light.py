import uuid

import numpy as np

from Mesh.System.Entity.Concrete.Light import Light
from Mesh.System.Entity.Function import Function, FunctionUnsupportedError
from Mesh.System.Entity.Function.Powered import ElectricPower
from Mesh.System.Entity.Function.Tasked import TaskName, SystemTask, Task, ProgramTask, TaskResponse, Status
from Mesh.System.SpaceFactor import MatterType
from MeshTest import test_settings
from MeshTest.AppTestCase import AppTestCase


class TestLightPowered(AppTestCase):
    def setUp(self):
        super().setUp()
        self.light = Light(uuid=uuid.uuid4(), selected_functions=(Function.POWERED,))

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
        # SystemTask
        self.assertRaises(FunctionUnsupportedError, lambda: self.light.send_task(SystemTask(name=TaskName.ACTIVE)))

        # EntityTask
        self.assertRaises(FunctionUnsupportedError, lambda: self.light.send_task(Task(name=TaskName.GET_INFO)))

        # ProgramTask
        self.assertRaises(FunctionUnsupportedError, lambda: self.light.send_task(ProgramTask(name=TaskName.END)))

    def test_recv_task_resp(self):
        self.assertRaises(FunctionUnsupportedError, lambda: self.light.send_task(
            SystemTask(name=TaskName.SET_POWER, value={'power': ElectricPower(110)})))
        self.assertRaises(FunctionUnsupportedError, lambda: self.light.recv_task_resp())

        # SystemTask
        self.assertRaises(FunctionUnsupportedError, lambda: self.light.send_task(SystemTask(name=TaskName.ACTIVE)))
        self.assertRaises(FunctionUnsupportedError, lambda: self.light.recv_task_resp())

        # EntityTask
        self.assertRaises(FunctionUnsupportedError, lambda: self.light.send_task(Task(name=TaskName.GET_INFO)))
        self.assertRaises(FunctionUnsupportedError, lambda: self.light.recv_task_resp())


class TestLightTasked(TestLightPowered):
    def setUp(self):
        super().setUp()
        self.light = Light(uuid=uuid.uuid4(), selected_functions=(Function.POWERED, Function.TASKED))

    def test_send_task(self):
        # SystemTask
        self.light.send_task(SystemTask(name=TaskName.ACTIVE))

        # EntityTask
        self.light.send_task(Task(name=TaskName.GET_INFO))

    def test_recv_task_resp(self):
        self.light.send_task(SystemTask(name=TaskName.SET_POWER, value={'power': ElectricPower(110)}))
        self.assertEqual(TaskResponse(Status.OK), self.light.recv_task_resp())

        self.light.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertEqual(TaskResponse(Status.OK), self.light.recv_task_resp())

        self.light.send_task(Task(name=TaskName.GET_INFO))
        self.assertEqual(TaskResponse(status=Status.OK, value={'info': {
                             'uuid': str(self.light.uuid),
                             'identifier': type(self.light).identifier,
                             'type': {
                                 'actuator': [
                                     'POWER'
                                 ],
                                 'sensor': [],
                                 'accessor': []
                             },
        }}),
                         self.light.recv_task_resp())

    def test_active_deactivate(self):
        self.light.send_task(SystemTask(name=TaskName.SET_POWER, value={'power': ElectricPower(110)}))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

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

        self.light.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(self.light.recv_task_resp().value['system_info']['active'])

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

    def test_input_power(self):
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

    def test_input_power_autodeactivate(self):
        def check_active(l_light, expected):
            if expected:
                self.assertTrue(l_light.active)
                l_light.send_task(SystemTask(TaskName.GET_SYSTEM_INFO))
                self.assertTrue(light.recv_task_resp().value['system_info']['active'])
            else:
                self.assertFalse(l_light.active)
                l_light.send_task(SystemTask(TaskName.GET_SYSTEM_INFO))
                self.assertFalse(light.recv_task_resp().value['system_info']['active'])

        light = Light(uuid=uuid.uuid4(), selected_functions=(Function.POWERED, Function.TASKED))
        check_active(light, False)

        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)

        light.send_task(SystemTask(TaskName.SET_POWER, value={'power': ElectricPower(110)}))
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, True)

        light.send_task(SystemTask(TaskName.SET_POWER, value={'power': ElectricPower(0)}))
        check_active(light, False)
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)

        light.send_task(SystemTask(TaskName.SET_POWER, value={'power': ElectricPower(220)}))
        check_active(light, False)
        light.send_task(SystemTask(TaskName.ACTIVE))
        light.recv_task_resp()
        check_active(light, False)


class TestLightCompute(TestLightTasked):
    def setUp(self):
        super().setUp()
        self.light = Light(uuid=uuid.uuid4(), selected_functions=(Function.POWERED, Function.TASKED, Function.COMPUTE))

    def tearDown(self):
        self.light.destroy()
        super().tearDown()
