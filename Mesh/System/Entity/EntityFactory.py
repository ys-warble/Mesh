import uuid

from Mesh.System.Entity.Concrete.AirConditioner import AirConditioner
from Mesh.System.Entity.Concrete.Chair import Chair
from Mesh.System.Entity.Concrete.Human import Human
from Mesh.System.Entity.Concrete.Light import Light
from Mesh.System.Entity.Concrete.PowerSupply import PowerSupply
from Mesh.System.Entity.Concrete.SmokeDetector import SmokeDetector
from Mesh.System.Entity.Concrete.Switch import Switch
from Mesh.System.Entity.Concrete.Table import Table
from Mesh.System.Entity.Concrete.Thermostat import Thermostat
from Mesh.System.Entity.Concrete.Wall import Wall
from Mesh.System.Entity.Concrete.Wardrobe import Wardrobe


class EntityFactory:
    entity_lib = {
        AirConditioner.identifier: AirConditioner,
        Chair.identifier: Chair,
        Human.identifier: Human,
        Light.identifier: Light,
        PowerSupply.identifier: PowerSupply,
        SmokeDetector.identifier: SmokeDetector,
        Switch.identifier: Switch,
        Table.identifier: Table,
        Thermostat.identifier: Thermostat,
        Wall.identifier: Wall,
        Wardrobe.identifier: Wardrobe,
    }

    def get_entity(self, entity, **kwargs):
        if entity not in EntityFactory.entity_lib:
            raise AttributeError
        else:
            if 'uuid' not in kwargs:
                kwargs['uuid'] = uuid.uuid4()
            return EntityFactory.entity_lib[entity](**kwargs)
