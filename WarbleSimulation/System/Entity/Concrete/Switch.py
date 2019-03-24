import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.Entity.Function import Function
from WarbleSimulation.System.Entity.Function.Powered import PowerInput, PowerOutput, Powered, ElectricPower
from WarbleSimulation.System.Entity.Function.Tasked import Tasked, TaskLevel, TaskResponse, Status, TaskName
from WarbleSimulation.System.SpaceFactor import MatterType


class Switch(Concrete):
    identifier = 'switch'
    default_dimension = (1, 1, 2)
    default_orientation = (0, 1, 0)

    default_consume_power_ratings = [ElectricPower(110)]

    def __init__(self, uuid, dimension_x=(1, 1, 1), selected_functions=(Function.POWERED, Function.TASKED)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.PLASTIC,
                         selected_functions=selected_functions)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

        self.active = False

    def get_default_shape(self):
        i = self.matter_type.value
        shape = np.array([
            [[i, i]]
        ])

        return shape

    def validate_functions(self, selected_functions):
        if Function.POWERED in selected_functions and Function.TASKED in selected_functions:
            return True
        else:
            return False

    def define_functions(self, selected_functions):
        if Function.POWERED:
            powered = Powered(self)
            powered.power_inputs.append(PowerInput(self))
            powered.power_outputs.append(PowerOutput(self))
            powered.input_power_ratings.extend(Switch.default_consume_power_ratings)
            self.functions[Function.POWERED] = powered

        if Function.TASKED:
            self.functions[Function.TASKED] = SwitchTasked(self)


class SwitchTasked(Tasked):
    tasks = [
        TaskName.GET_SYSTEM_INFO,
        TaskName.ACTIVE,
        TaskName.DEACTIVATE,
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

        if self.entity.active and task.level == TaskLevel.ENTITY:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.SYSTEM:
            if task.name == TaskName.GET_SYSTEM_INFO:
                system_info = get_info()
                system_info['active'] = self.entity.active
                task_response = TaskResponse(status=Status.OK, value={'system_info': system_info})
            elif task.name == TaskName.ACTIVE:
                self.entity.active = True

                if self.entity.has_function(Function.POWERED):
                    powered = self.entity.get_function(Function.POWERED)
                    for i in powered.power_outputs:
                        i.set_power(powered.power_inputs[0].get_power())

                task_response = TaskResponse(status=Status.OK, value=None)
            elif task.name == TaskName.DEACTIVATE:
                self.entity.active = False

                if self.entity.has_function(Function.POWERED):
                    powered = self.entity.get_function(Function.POWERED)
                    for i in powered.power_outputs:
                        i.set_power()

                task_response = TaskResponse(status=Status.OK, value=None)
            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.PROGRAM:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        else:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        return task_response
