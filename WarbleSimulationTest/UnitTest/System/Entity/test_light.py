import uuid

import numpy as np

from WarbleSimulation.System.Entity.Concrete.Light import Light
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
        self.light.recv_task_resp()

        self.light.send_task(SystemTask(name=TaskName.GET_SYSTEM_INFO))
        self.assertFalse(self.light.recv_task_resp().value['system_info']['active'])
