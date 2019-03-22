from multiprocessing import Pipe


class Compute:
    def __init__(self, entity):
        self.entity = entity
        self.process = None
        self.p_task_pipe, self.c_task_pipe = Pipe()

    def run(self):
        raise NotImplementedError

    def handle_task(self, task):
        raise NotImplementedError
