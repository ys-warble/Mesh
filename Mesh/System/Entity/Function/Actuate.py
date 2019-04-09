from Mesh.System.Entity.Function import BaseFunction
from Mesh.System.Entity.Function.Tasked import TaskName


class Actuate(BaseFunction):
    tasks = [
        TaskName.ACTUATE
    ]

    def __init__(self, entity):
        super().__init__(entity)

    def eval(self):
        pass

    def init(self):
        pass

    def terminate(self):
        pass

    def actuate(self, space, location, orientation):
        raise NotImplementedError
