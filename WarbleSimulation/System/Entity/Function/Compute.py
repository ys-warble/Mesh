from multiprocessing import Pipe

from WarbleSimulation.System.Entity.Function import BaseFunction
from WarbleSimulation.System.Entity.Function.Tasked import TaskName


class Compute(BaseFunction):
    tasks = [
        TaskName.START,
        TaskName.END,
    ]

    def __init__(self, entity):
        super().__init__(entity)
        self.process = None
        self.p_task_pipe, self.c_task_pipe = Pipe()

    def eval(self):
        pass

    def is_computing(self):
        return self.process is not None

    def run(self):
        raise NotImplementedError
