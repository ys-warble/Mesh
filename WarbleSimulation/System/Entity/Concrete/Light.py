import numpy as np

from WarbleSimulation import settings
from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.Entity.Function import Function
from WarbleSimulation.System.Entity.Function.Compute import Compute
from WarbleSimulation.System.Entity.Function.Powered import PowerInput, Powered, ElectricPower
from WarbleSimulation.System.Entity.Function.Tasked import TaskLevel, TaskName, Status, TaskResponse, \
    Tasked
from WarbleSimulation.System.SpaceFactor import MatterType


class Light(Concrete):
    identifier = 'light'
    default_dimension = (3, 3, 3)
    default_orientation = (0, 1, 0)

    default_consume_power_ratings = [ElectricPower(110)]

    def __init__(self, uuid, dimension_x=(1, 1, 1),
                 selected_functions=(Function.POWERED, Function.TASKED, Function.COMPUTE)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.GLASS,
                         selected_functions=selected_functions)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

        self.active = False

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

    def validate_functions(self, selected_functions):
        if (Function.COMPUTE in selected_functions or Function.TASKED in selected_functions) and \
                Function.POWERED not in selected_functions:
            return False
        else:
            return True

    def define_functions(self, selected_functions):
        if Function.POWERED in selected_functions:
            powered = Powered(self)
            powered.power_inputs.append(PowerInput(self))
            powered.input_power_ratings.extend(Light.default_consume_power_ratings)
            self.functions[Function.POWERED] = powered

        if Function.TASKED in selected_functions:
            self.functions[Function.TASKED] = LightTasked(self)

        if Function.COMPUTE in selected_functions:
            self.functions[Function.COMPUTE] = LightCompute(self)


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
                        self.c_task_pipe.send(self.entity.active)
                        break
                    else:
                        self.c_task_pipe.send(self.entity.get_function(Function.TASKED).handle(task))


class LightTasked(Tasked):
    tasks = [
        TaskName.GET_SYSTEM_INFO,
        TaskName.ACTIVE,
        TaskName.DEACTIVATE,

        TaskName.GET_INFO,
    ]

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

        powered = self.entity.get_function(Function.POWERED)
        power = powered.get_power_input().get_power()

        if task.level == TaskLevel.ENTITY and power in powered.input_power_ratings:
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
                if power in powered.input_power_ratings:
                    self.entity.active = True
                    task_response = TaskResponse(status=Status.OK, value=None)
                else:
                    task_response = TaskResponse(status=Status.ERROR, value={'error': 'No Input Power'})
            elif task.name == TaskName.DEACTIVATE:
                self.entity.active = False
                task_response = TaskResponse(status=Status.OK, value=None)
            elif task.name == TaskName.SET_POWER:
                powered.get_power_input().set_power(task.value['power'])
                task_response = TaskResponse(status=Status.OK, value=None)
            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.PROGRAM:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        else:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        return task_response
