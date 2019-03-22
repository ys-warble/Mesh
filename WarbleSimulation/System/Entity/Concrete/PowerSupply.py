import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.Entity.Function import Function
from WarbleSimulation.System.Entity.Function.Powered import PowerOutput, Powered
from WarbleSimulation.System.Entity.Function.Tasked import TaskLevel, TaskName, Status, TaskResponse, Tasked
from WarbleSimulation.System.SpaceFactor import MatterType


class PowerSupply(Concrete):
    identifier = 'PowerSupply'
    default_dimension = (1, 1, 1)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.METAL)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

        self.task_active = False

    def get_default_shape(self):
        i = self.matter_type.value
        shape = np.array([[[i]]])

        return shape

    def define_functions(self):
        powered = Powered(self)
        powered.power_outputs.append(PowerOutput(self))
        self.functions[Function.POWERED] = powered
        self.functions[Function.TASKED] = PowerSupplyTasked(self)


class PowerSupplyTasked(Tasked):
    def handle(self, task):
        if task.level == TaskLevel.ENTITY:
            if task.name == TaskName.GET_INFO:
                info = {
                    'uuid': str(self.entity.uuid),
                    'identifier': type(self.entity).identifier,
                    'type': {
                        'actuator': [
                            'POWER'
                        ],
                        'sensor': [],
                        'accessor': []
                    },
                }
                task_response = TaskResponse(Status.OK, {'info': info})
            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.SYSTEM:
            if task.name == TaskName.ACTIVE:
                self.entity.active = True
                task_response = TaskResponse(status=Status.OK, value=None)

            elif task.name == TaskName.DEACTIVATE:
                self.entity.active = False
                task_response = TaskResponse(status=Status.OK, value=None)

            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        else:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        return task_response
