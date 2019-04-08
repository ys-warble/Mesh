import json

from Mesh.System.Entity.Channel.ChannelFactory import ChannelFactory
from Mesh.System.Entity.EntityFactory import EntityFactory
from Mesh.System.Entity.Function import Function
from Mesh.System.Entity.Function.Tasked import SystemTask, TaskName
from Mesh.System.SpaceFactor import SpaceFactor
from Mesh.System.System import System


def load_system_file(file):
    content = json.load(file)

    # system
    o_system = None
    if 'system' in content:
        o_system = System(**(content['system']))

    # space
    if 'space' in content:
        if 'space_factor_types' in content['space']:
            content['space']['space_factor_types'] = [SpaceFactor[s] for s in content['space']['space_factor_types']]
        o_system.put_space(**(content['space']))

    # entities
    if 'entities' in content:
        ef = EntityFactory()
        for row in content['entities']:
            if 'selected_functions' in row:
                row['selected_functions'] = [Function[s] for s in row['selected_functions']]
            entity = ef.get_entity(**{x: row[x] for x in row if x not in ['location']})
            o_system.put_entity(entity, row['location'])

    # channels
    if 'channels' in content:
        cf = ChannelFactory()
        for row in content['channels']:
            kwargs = {x: row[x] for x in row if x not in ['channel']}
            kwargs['_from'] = o_system.get_entity(kwargs['_from'])
            kwargs['_to'] = o_system.get_entity(kwargs['_to'])
            cf.get_channel(row['channel'], **kwargs)

    return o_system


if __name__ == '__main__':
    system = None

    with open('../resources/examples/example_1/system.json', 'r') as system_file:
        system = load_system_file(system_file)

    print(system)

    system.get_entity(0).send_task(SystemTask(TaskName.ACTIVE))
    system.get_entity(1).send_task(SystemTask(TaskName.ACTIVE))
    system.get_entity(2).send_task(SystemTask(TaskName.ACTIVE))

    system.get_entity(2).send_task(SystemTask(TaskName.GET_SYSTEM_INFO))
    tr = system.get_entity(2).recv_task_resp()
    print(tr)

    system.destroy()
