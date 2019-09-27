import numpy as np

import Mesh.System.SpaceFactor as SpaceFactor
from Mesh.System.Entity.Concrete import Concrete
from Mesh.System.Entity.Function import Function
from Mesh.System.Entity.Function.Actuate import Actuate
from Mesh.System.Entity.Function.Compute import Compute
from Mesh.System.Entity.Function.Powered import PowerInput, Powered, ElectricPower
from Mesh.System.Entity.Function.Tasked import TaskLevel, TaskName, Status, TaskResponse, \
    Tasked
from Mesh.System.SpaceFactor import MatterType


class Light(Concrete):
    identifier = 'light'
    default_dimension = (3, 3, 3)
    default_orientation = (0, 1, 0)

    default_consume_power_ratings = [ElectricPower(110)]

    default_hue = 208
    default_saturation = 100
    default_brightness = 90

    default_wattage = 15

    default_temperature_raise = 5  # Kelvin

    def __init__(self, uuid, dimension_x=(1, 1, 1),
                 selected_functions=(Function.POWERED, Function.TASKED, Function.COMPUTE, Function.ACTUATE),
                 hue=default_hue, saturation=default_saturation, brightness=default_brightness,
                 wattage=default_wattage,
                 temperature_raise=default_temperature_raise):
        self.active = False
        self.hue = hue
        self.saturation = saturation
        self.brightness = brightness
        self.wattage = wattage
        self.temperature_raise = temperature_raise
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.GLASS,
                         selected_functions=selected_functions)

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
            self.functions[Function.COMPUTE] = Compute(self)

        if Function.ACTUATE in selected_functions:
            self.functions[Function.ACTUATE] = LightActuate(self)


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
                power = task.value['power']
                powered.get_power_input().power = power
                if power not in powered.input_power_ratings:
                    self.entity.active = False
                task_response = TaskResponse(status=Status.OK, value=None)
            elif task.name == TaskName.ACTUATE:
                space_factor_patch = self.entity.get_function(Function.ACTUATE).actuate(**task.value, active=(power in powered.input_power_ratings))
                task_response = TaskResponse(status=Status.OK, value=space_factor_patch)
            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        elif task.level == TaskLevel.PROGRAM:
            if task.name == TaskName.END:
                task_response = self.handle_end()
            else:
                task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        else:
            task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})

        return task_response


class LightActuate(Actuate):
    def __init__(self, entity):
        super().__init__(entity)
        self.space = None
        self.location = None
        self.orientation = None
        self.space_factors = None

    def actuate(self, space, location, orientation, active=True):
        def _calc_brightness(i, j, k):
            return brightness / (((center[0] - i) / resolution) ** 2 + ((center[1] - j) / resolution) ** 2 + (
                    (center[2] - k) / resolution) ** 2 + 1) ** (2 / wattage)

        def _calc_temperature(i, j, k):
            return temperature_raise / (((center[0] - i) / resolution) ** 2 + ((center[1] - j) / resolution) ** 2 + (
                    (center[2] - k) / resolution) ** 2 + 1) ** (2 / wattage)

        self.space_factors = dict()

        if active:
            center = [location[i] + int(self.entity.dimension[i] / 2) for i in range(len(location))]
            brightness = self.entity.brightness
            temperature_raise = self.entity.temperature_raise
            resolution = space.resolution
            wattage = self.entity.wattage

            # Luminosity
            self.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY] = dict()
            self.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.HUE] = \
                np.full(tuple([i * space.resolution for i in space.dimension]), fill_value=self.entity.hue)
            self.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.SATURATION] = \
                np.full(tuple([i * space.resolution for i in space.dimension]), fill_value=self.entity.saturation)
            self.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS] = \
                np.fromfunction(_calc_brightness,
                                tuple([i * space.resolution for i in space.dimension]), dtype=int)
            self.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS] = \
                self.space_factors[SpaceFactor.SpaceFactor.LUMINOSITY][SpaceFactor.Luminosity.BRIGHTNESS].astype(int)

            # Temperature
            self.space_factors[SpaceFactor.SpaceFactor.TEMPERATURE] = dict()
            self.space_factors[SpaceFactor.SpaceFactor.TEMPERATURE][SpaceFactor.Temperature.TEMPERATURE] = \
                np.fromfunction(_calc_temperature,
                                tuple([i * space.resolution for i in space.dimension]), dtype=int)
            self.space_factors[SpaceFactor.SpaceFactor.TEMPERATURE][SpaceFactor.Temperature.TEMPERATURE] = \
                self.space_factors[SpaceFactor.SpaceFactor.TEMPERATURE][SpaceFactor.Temperature.TEMPERATURE].astype(int)

            return self.space_factors

        else:
            return self.space_factors
