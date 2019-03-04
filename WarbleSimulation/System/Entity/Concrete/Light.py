import time

import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.SpaceFactor import MatterType


class Light(Concrete):
    identifier = 'light'
    default_dimension = (3, 3, 3)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.GLASS)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

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

    # def run(self, task_queue=None):
    #     if task_queue is None or not isinstance(task_queue, Queue):
    #         return
    #
    #     while True:
    #         task = task_queue.get()
    #
    #         if task is None:
    #             print('Light \'%s\' quit. Bye!' % self.uuid)
    #             break
    #         else:
    #             print('Light \'%s\' executing task: %s ...' % (self.uuid, task))
    #             if task == 'wait':
    #                 time.sleep(3)
    #             elif task == 'uuid':
    #
    #             elif task == 'dimension':
    #                 pass
    #             print('Light \'%s\' task done' % self.uuid)

    def run(self, task_pipe=None):
        if task_pipe is None:
            return

        while True:
            task = task_pipe.recv()
            if task is None:
                print('Light \'%s\' quit. Bye!' % self.uuid)
                task_pipe.close()
                break
            else:
                print('Light \'%s\' executing task: %s ...' % (self.uuid, task))
                if task == 'wait':
                    time.sleep(3)
                elif task == 'uuid':
                    task_pipe.send(self.uuid)
                elif task == 'dimension':
                    task_pipe.send(self.dimension)
                print('Light \'%s\' task done' % self.uuid)
