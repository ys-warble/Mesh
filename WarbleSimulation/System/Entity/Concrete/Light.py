from multiprocessing import Process

import numpy as np

from WarbleSimulation import settings
from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.Entity.Function import Function
from WarbleSimulation.System.Entity.Function.Compute import Compute
from WarbleSimulation.System.Entity.Function.Powered import PowerInput, Powered
from WarbleSimulation.System.Entity.Function.Tasked import TaskLevel, TaskName, Status, ProgramTask, TaskResponse
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

    def send_task(self, task):
        self.last_task = task

        if task.level == TaskLevel.PROGRAM and task.name == TaskName.START:
            if self.has_function(Function.COMPUTE):
                compute = self.get_function(Function.COMPUTE)
                if not compute.is_computing():
                    compute.process = Process(target=compute.run)
                    compute.process.start()
                    self.last_task_response = TaskResponse(status=Status.OK, value=None)
                else:
                    self.last_task_response = TaskResponse(status=Status.ERROR, value={'error': 'Already Computing'})
            else:
                self.last_task_response = TaskResponse(status=Status.ERROR, value={'error': 'Not Implemented'})

        elif task.level == TaskLevel.PROGRAM and task.name == TaskName.END:
            if self.has_function(Function.COMPUTE):
                compute = self.get_function(Function.COMPUTE)
                if compute.is_computing():
                    compute.p_task_pipe.send(task)
                    compute.process.join()
                    compute.process = None
                    self.last_task_response = TaskResponse(status=Status.OK, value=None)
                else:
                    self.last_task_response = TaskResponse(status=Status.ERROR, value={'error': 'Already Computing'})
            else:
                self.last_task_response = TaskResponse(status=Status.ERROR, value={'error': 'Not Implemented'})

        else:
            if self.has_function(Function.COMPUTE) and self.get_function(Function.COMPUTE).is_computing():
                self.get_function(Function.COMPUTE).p_task_pipe.send(task)
            else:
                self.last_task_response = self.handle_task(task)

    def recv_task_resp(self):
        if self.has_function(Function.COMPUTE) and self.get_function(Function.COMPUTE).is_computing():
            if self.last_task != ProgramTask(TaskName.START):
                self.last_task_response = self.get_function(Function.COMPUTE).p_task_pipe.recv()

        temp = self.last_task_response
        self.last_task_response = None
        return temp

    def handle_task(self, task):
        if task.level == TaskLevel.ENTITY:
            if task.name == TaskName.GET_INFO:
                task_response = TaskResponse(Status.OK, {'info': {
                    'uuid': str(self.uuid),
                    'identifier': type(self).identifier,
                    'type': {
                        'actuator': [
                            'LUMINOSITY'
                        ],
                        'sensor': [],
                        'accessor': []
                    },
                }})
            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.SYSTEM:
            if task.name == TaskName.GET_SYSTEM_INFO:
                task_response = TaskResponse(status=Status.OK, value={'system_info': {
                    'uuid': str(self.uuid),
                    'identifier': type(self).identifier,
                    'type': {
                        'actuator': [
                            'LUMINOSITY'
                        ],
                        'sensor': [],
                        'accessor': []
                    },
                    'active': self.task_active
                }})
            elif task.name == TaskName.ACTIVE:
                self.task_active = True
                task_response = TaskResponse(status=Status.OK, value=None)
            elif task.name == TaskName.DEACTIVATE:
                self.task_active = False
                task_response = TaskResponse(status=Status.OK, value=None)
            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.PROGRAM:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        else:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        return task_response


class LightCompute(Compute):
    def __init__(self, entity):
        super().__init__(entity)

    def is_computing(self):
        return self.process is not None

    def run(self):
        if self.c_task_pipe is None:
            return

        while True:
            # TODO still need much definition and design decisions

            # Do the submitted Task
            if self.c_task_pipe is not None and self.c_task_pipe.poll(settings.ENTITY_TASK_POLLING_DURATION):
                task = self.c_task_pipe.recv()
                if task.level == TaskLevel.PROGRAM and task.name == TaskName.END:
                    break
                else:
                    self.c_task_pipe.send(self.handle_task(task))

    def handle_task(self, task):
        return self.entity.handle_task(task)
