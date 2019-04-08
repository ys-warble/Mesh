from multiprocessing import Pipe, Process

from Mesh import settings
from Mesh.System.Entity.Function import BaseFunction, Function
from Mesh.System.Entity.Function.Tasked import Status, TaskName, ProgramTask


class Compute(BaseFunction):
    tasks = [
        TaskName.END
    ]

    def __init__(self, entity):
        super().__init__(entity)
        self.process = None
        self.p_task_pipe, self.c_task_pipe = Pipe()

    def eval(self):
        self.process = Process(target=self.run, args=(self.entity,))

    def is_computing(self):
        return self.process is not None

    def init(self):
        self.process.start()

    def terminate(self):
        if self.process.is_alive():
            self.entity.send_task(ProgramTask(TaskName.END))

    def run(self, entity):
        while True:
            if self.c_task_pipe.poll(settings.ENTITY_TASK_POLLING_DURATION):
                task = self.c_task_pipe.recv()
                task_resp = entity.get_function(Function.TASKED).handle(task)
                self.c_task_pipe.send(task_resp)

                if task_resp.status == Status.END:
                    break
