import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.Entity.Function import Function
from WarbleSimulation.System.Entity.Function.Powered import PowerOutput, Powered, ElectricPower
from WarbleSimulation.System.Entity.Function.Tasked import TaskLevel, TaskName, Status, TaskResponse, Tasked
from WarbleSimulation.System.SpaceFactor import MatterType


class PowerSupply(Concrete):
    identifier = 'PowerSupply'
    default_dimension = (1, 1, 1)
    default_orientation = (0, 1, 0)

    default_supply_power_ratings = [ElectricPower(110)]

    def __init__(self, uuid, dimension_x=(1, 1, 1), selected_functions=(Function.POWERED, Function.TASKED)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.METAL,
                         selected_functions=selected_functions)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

        self.active = False

    def get_default_shape(self):
        i = self.matter_type.value
        shape = np.array([[[i]]])

        return shape

    def validate_functions(self, selected_functions):
        if Function.POWERED in selected_functions and Function.TASKED in selected_functions:
            return True
        else:
            return False

    def define_functions(self, selected_functions):
        if Function.POWERED in selected_functions:
            powered = Powered(self)
            powered.power_outputs.append(PowerOutput(self))
            powered.output_power_ratings.extend(PowerSupply.default_supply_power_ratings)
            self.functions[Function.POWERED] = powered

        if Function.TASKED in selected_functions:
            self.functions[Function.TASKED] = PowerSupplyTasked(self)


class PowerSupplyTasked(Tasked):
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

        if task.level == TaskLevel.ENTITY:
            if task.name == TaskName.GET_INFO:
                task_response = TaskResponse(Status.OK, {'info': get_info()})
            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.SYSTEM:
            if task.name == TaskName.ACTIVE:
                self.entity.active = True

                if self.entity.has_function(Function.POWERED):
                    powered = self.entity.get_function(Function.POWERED)
                    for i in powered.power_outputs:
                        i.set_power(powered.output_power_ratings[0])

                task_response = TaskResponse(status=Status.OK, value=None)

            elif task.name == TaskName.DEACTIVATE:
                self.entity.active = False
                task_response = TaskResponse(status=Status.OK, value=None)

            elif task.name == TaskName.GET_SYSTEM_INFO:
                info = get_info()
                info['active'] = self.entity.active
                task_response = TaskResponse(status=Status.OK, value={'system_info': info})

            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        else:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        return task_response
