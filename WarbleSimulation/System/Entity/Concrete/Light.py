import numpy as np

from WarbleSimulation import settings
from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.Entity.Function import Function
from WarbleSimulation.System.Entity.Function.Compute import Compute
from WarbleSimulation.System.Entity.Function.Powered import PowerInput, Powered
from WarbleSimulation.System.Entity.Task import TaskName, TaskResponse, Status
from WarbleSimulation.System.SpaceFactor import MatterType


class Light(Concrete):
    identifier = 'light'
    default_dimension = (3, 3, 3)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.GLASS)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

        self.task_active = False

        powered = Powered()
        powered.power_inputs.append(PowerInput(self))
        self.functions[Function.POWERED] = powered
        self.functions[Function.COMPUTE] = LightCompute(self)

    def get_default_shape(self):
        matter = self.matter_type.value
        shape = np.array([
            [[0, 0, 0],
             [0, matter, 0],
             [0, 0, 0]],
            [[0, matter, 0],
             [matter, matter, matter],
             [0, matter, 0]],
            [[0, 0, 0],
             [0, matter, 0],
             [0, 0, 0]],
        ])

        return shape

    def send_task(self, task):
        pass

    def recv_task_resp(self):
        pass

    def handle_task(self, task):
        if task.name == TaskName.GET_INFO:
            info = {
                'uuid': str(self.uuid),
                'identifier': type(self).identifier,
                'type': {
                    'actuator': [
                        'LUMINOSITY'
                    ],
                    'sensor': [],
                    'accessor': []
                },
            }
            task_response = TaskResponse(Status.OK, {'info': info})
        else:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        return task_response


class LightCompute(Compute):
    def __init__(self, entity):
        super().__init__(entity)

    def run(self):
        if self.c_task_pipe is None:
            return

        while True:
            # TODO still need much definition and design decisions

            # Do the submitted Task
            if self.c_task_pipe is not None and self.c_task_pipe.poll(settings.ENTITY_TASK_POLLING_DURATION):
                task = self.c_task_pipe.recv()
                if task.name == TaskName.END:
                    self.entity.task_active = False
                    self.c_task_pipe.send(TaskResponse(Status.OK, None))
                    self.c_task_pipe.close()
                    break
                elif task.name == TaskName.ACTIVE:
                    self.entity.task_active = True
                    self.c_task_pipe.send(TaskResponse(Status.OK, None))
                elif task.name == TaskName.DEACTIVATE:
                    self.entity.task_active = False
                    self.c_task_pipe.send(TaskResponse(Status.OK, None))
                else:
                    if self.entity.task_active:
                        self.c_task_pipe.send(self.handle_task(task))

    def handle_task(self, task):
        return self.entity.handle_task(task)
