from multiprocessing import Pipe

from WarbleSimulation.System.Entity.Function import BaseFunction


class Compute(BaseFunction):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.process = None
        self.p_task_pipe, self.c_task_pipe = Pipe()

    def run(self):
        raise NotImplementedError
