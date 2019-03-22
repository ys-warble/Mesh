import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.Entity.Function import Function
from WarbleSimulation.System.Entity.Function.Powered import PowerOutput, Powered
from WarbleSimulation.System.Entity.Task import TaskLevel, TaskName, TaskResponse, Status
from WarbleSimulation.System.SpaceFactor import MatterType


class PowerSupply(Concrete):
    identifier = 'PowerSource'
    default_dimension = (1, 1, 1)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.METAL)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

        self.task_active = False

        powered = Powered()
        powered.power_outputs.append(PowerOutput(self))
        self.functions[Function.POWERED] = powered

    def get_default_shape(self):
        matter = self.matter_type.value
        shape = np.array([[[matter]]])

        return shape

    def send_task(self, task):
        if task.level == TaskLevel.ENTITY:
            if task.name == TaskName.GET_INFO:
                info = {
                    'uuid': str(self.uuid),
                    'identifier': type(self).identifier,
                    'type': {
                        'actuator': [
                            'POWER'
                        ],
                        'sensor': [],
                        'accessor': []
                    },
                }
                self.task_response = TaskResponse(Status.OK, {'info': info})
            else:
                self.task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.SYSTEM:
            if task.name == TaskName.ACTIVE:
                self.task_active = True
                self.task_response = TaskResponse(status=Status.OK, value=None)

            elif task.name == TaskName.DEACTIVATE:
                self.task_active = False
                self.task_response = TaskResponse(status=Status.OK, value=None)

        else:
            self.task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

    def recv_task_resp(self):
        temp = self.task_response
        self.task_response = None
        return temp
