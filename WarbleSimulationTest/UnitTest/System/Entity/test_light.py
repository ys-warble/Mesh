import uuid
from unittest import TestCase

from WarbleSimulation.System.Entity.Concrete.Light import Light
from WarbleSimulation.System.Entity.Task import ProgramTask, TaskName, SystemTask, Task, Status, TaskResponse
from WarbleSimulation.System.SpaceFactor import MatterType
from WarbleSimulation.util import Logger
from WarbleSimulationTest import test_settings


class TestLight(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = Logger.get_logger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger.info('')
        self.logger.info(test_settings.start_title_format(self._testMethodName))

        self.light = Light(uuid=uuid.uuid4())

    def tearDown(self):
        self.logger.info(test_settings.end_title_format(self._testMethodName))
        self.logger.info('')

    def test_get_default_shape(self):
        self.assertEqual(self.light.get_default_shape(), [[[MatterType.GLASS.value]]])
        self.assertEqual(self.light.get_default_shape().shape, (3, 3, 3))

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

    def test_handle_task(self):
        self.light.handle_task(Task(name=TaskName.GET_INFO))
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

    def test_task(self):
        # ProgramTask
        self.light.send_task(ProgramTask(name=TaskName.START))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.ERROR, value={'error': 'Not Implemented'}))

        self.light.send_task(ProgramTask(name=TaskName.END))
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.ERROR, value={'error': 'Not Implemented'}))

        # SystemTask
        self.light.send_task(SystemTask(name=TaskName.DEACTIVATE))
        self.assertFalse(self.light.task_active)
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        self.light.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertTrue(self.light.task_active)
        self.assertEqual(self.light.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        self.light.send_task(SystemTask(name=TaskName.DEACTIVATE))
        self.assertFalse(self.light.task_active)
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
