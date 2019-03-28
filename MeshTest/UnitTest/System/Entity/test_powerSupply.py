import uuid

from Mesh.System.Entity.Concrete.PowerSupply import PowerSupply
from Mesh.System.Entity.Function.Tasked import TaskName, Status, ProgramTask, SystemTask, Task, TaskResponse
from Mesh.System.SpaceFactor import MatterType
from MeshTest.AppTestCase import AppTestCase


class TestPowerSupply(AppTestCase):
    def setUp(self):
        super().setUp()
        self.power_supply = PowerSupply(uuid=uuid.uuid4())

    def test_get_default_shape(self):
        self.assertEqual(self.power_supply.get_default_shape(), [[[MatterType.METAL.value]]])
        self.assertEqual(self.power_supply.get_default_shape().shape, (1, 1, 1))

    def test_send_task(self):
        # ProgramTask
        self.power_supply.send_task(ProgramTask(name=TaskName.END))

        # SystemTask
        self.power_supply.send_task(SystemTask(name=TaskName.ACTIVE))

        # EntityTask
        self.power_supply.send_task(Task(name=TaskName.GET_INFO))

    def test_recv_task_resp(self):
        # ProgramTask
        self.power_supply.send_task(ProgramTask(name=TaskName.END))
        self.assertEqual(self.power_supply.recv_task_resp(),
                         TaskResponse(status=Status.ERROR, value={'error': 'Not Implemented'}))

        # SystemTask
        self.power_supply.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertEqual(self.power_supply.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        # EntityTask
        self.power_supply.send_task(Task(name=TaskName.GET_INFO))
        self.assertEqual(self.power_supply.recv_task_resp(),
                         TaskResponse(status=Status.OK, value={'info': {
                             'uuid': str(self.power_supply.uuid),
                             'identifier': type(self.power_supply).identifier,
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
        self.power_supply.send_task(ProgramTask(name=TaskName.START))
        self.assertEqual(self.power_supply.recv_task_resp(),
                         TaskResponse(status=Status.ERROR, value={'error': 'Not Implemented'}))

        self.power_supply.send_task(ProgramTask(name=TaskName.END))
        self.assertEqual(self.power_supply.recv_task_resp(),
                         TaskResponse(status=Status.ERROR, value={'error': 'Not Implemented'}))

        # SystemTask
        self.power_supply.send_task(SystemTask(name=TaskName.DEACTIVATE))
        self.assertFalse(self.power_supply.active)
        self.assertEqual(self.power_supply.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        self.power_supply.send_task(SystemTask(name=TaskName.ACTIVE))
        self.assertTrue(self.power_supply.active)
        self.assertEqual(self.power_supply.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        self.power_supply.send_task(SystemTask(name=TaskName.DEACTIVATE))
        self.assertFalse(self.power_supply.active)
        self.assertEqual(self.power_supply.recv_task_resp(),
                         TaskResponse(status=Status.OK, value=None))

        # EntityTask
        self.power_supply.send_task(Task(name=TaskName.GET_INFO))
        self.assertEqual(self.power_supply.recv_task_resp(),
                         TaskResponse(status=Status.OK, value={'info': {
                             'uuid': str(self.power_supply.uuid),
                             'identifier': type(self.power_supply).identifier,
                             'type': {
                                 'actuator': [
                                     'POWER'
                                 ],
                                 'sensor': [],
                                 'accessor': []
                             },
                         }}))
