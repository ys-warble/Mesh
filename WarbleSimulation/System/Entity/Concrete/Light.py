import numpy as np

from WarbleSimulation import settings
from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.Entity.Function import Function
from WarbleSimulation.System.Entity.Function.Compute import Compute
from WarbleSimulation.System.Entity.Function.Powered import PowerInput, Powered
from WarbleSimulation.System.Entity.Function.Tasked import TaskLevel, TaskName, Status, TaskResponse, \
    Tasked
from WarbleSimulation.System.SpaceFactor import MatterType


class Light(Concrete):
    identifier = 'light'
    default_dimension = (3, 3, 3)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.GLASS)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

        self.active = False

        powered = Powered(self)
        powered.power_inputs.append(PowerInput(self))
        self.functions[Function.POWERED] = powered
        self.functions[Function.TASKED] = LightTasked(self)
        self.functions[Function.COMPUTE] = LightCompute(self)

    def get_default_shape(self):
        i = self.matter_type.value
        shape = np.array([
            [[0, 0, 0],
             [0, i, 0],
             [0, 0, 0]],
            [[0, i, 0],
             [i, i, i],
             [0, i, 0]],
            [[0, 0, 0],
             [0, i, 0],
             [0, 0, 0]],
        ])

        return shape


class LightCompute(Compute):
    def __init__(self, entity):
        super().__init__(entity)

    def run(self):
        if self.c_task_pipe is None:
            return

        while True:
            # TODO still need much definition and design decisions

            # Do the submitted task
            if self.entity.has_function(Function.TASKED):
                # Do the submitted Task
                if self.c_task_pipe is not None and self.c_task_pipe.poll(settings.ENTITY_TASK_POLLING_DURATION):
                    task = self.c_task_pipe.recv()

                    if task.level == TaskLevel.PROGRAM and task.name == TaskName.END:
                        break
                    else:
                        self.c_task_pipe.send(self.entity.get_function(Function.TASKED).handle(task))


class LightTasked(Tasked):
    def handle(self, task):
        def get_info():
            return {
                'uuid': str(self.entity.uuid),
                'identifier': type(self.entity).identifier,
                'type': {
                    'actuator': [
                        'LUMINOSITY'
                    ],
                    'sensor': [],
                    'accessor': []
                }
            }

        if task.level == TaskLevel.ENTITY:
            if task.name == TaskName.GET_INFO:
                task_response = TaskResponse(Status.OK, {'info': get_info()})
            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.SYSTEM:
            if task.name == TaskName.GET_SYSTEM_INFO:
                system_info = get_info()
                system_info['active'] = self.entity.active
                task_response = TaskResponse(status=Status.OK, value={'system_info': system_info})
            elif task.name == TaskName.ACTIVE:
                self.entity.active = True
                task_response = TaskResponse(status=Status.OK, value=None)
            elif task.name == TaskName.DEACTIVATE:
                self.entity.active = False
                task_response = TaskResponse(status=Status.OK, value=None)
            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.PROGRAM:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        else:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        return task_response
