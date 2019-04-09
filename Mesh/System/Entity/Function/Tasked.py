from enum import Enum

from Mesh.System.Entity.Function import BaseFunction, Function


class TaskLevel(Enum):
    PROGRAM = 0
    SYSTEM = 100
    ENTITY = 200


class TaskName(Enum):
    END = 1

    GET_SYSTEM_INFO = 101
    SET_POWER = 102
    ACTIVE = 103
    DEACTIVATE = 104
    ACTUATE = 105
    SENSE = 106

    GET_INFO = 201


class Status(Enum):
    OK = 0
    ERROR = 1
    END = -1


class BaseTask:
    def __init__(self, level, name, value=None, *args, **kwargs):
        self.level = level
        self.name = name
        self.value = value

    def __str__(self):
        return "Task(%s,%s)" % (self.level, self.name)

    def __eq__(self, other):
        return type(self) == type(other) and self.level == other.level and self.name == other.name


class ProgramTask(BaseTask):
    def __init__(self, name, value=None, *args, **kwargs):
        super().__init__(TaskLevel.PROGRAM, name, value, args, kwargs)


class SystemTask(BaseTask):
    def __init__(self, name, value=None, *args, **kwargs):
        super().__init__(TaskLevel.SYSTEM, name, value, args, kwargs)


class Task(BaseTask):
    def __init__(self, name, value=None, *args, **kwargs):
        super().__init__(TaskLevel.ENTITY, name, value, args, kwargs)


class TaskResponse:
    def __init__(self, status, value=None):
        self.status = status
        self.value = value

    def __str__(self):
        return "TaskResponse(%s, %s)" % (self.status, self.value)

    def __eq__(self, other):
        return self.status == other.status and self.value == self.value


class Tasked(BaseFunction):
    tasks = []

    def __init__(self, entity):
        super().__init__(entity)
        self.last_task = None
        self.last_task_response = None

        self.supported_tasks = None

    def eval(self):
        self.supported_tasks = list()
        for key, val in self.entity.functions.items():
            try:
                self.supported_tasks.extend(type(val).tasks)
            except AttributeError:
                pass

    def init(self):
        pass

    def terminate(self):
        pass

    def validate(self, task):
        if self.supported_tasks is None:
            self.eval()

        return True if (task.name in self.supported_tasks and task.level.value == int(
            task.name.value / 100) * 100) else False

    def send(self, task):
        self.last_task = task

        if not self.validate(task):
            self.last_task_response = TaskResponse(Status.ERROR, {'error': 'Not Implemented'})
        else:
            if self.entity.has_function(Function.COMPUTE):
                compute = self.entity.get_function(Function.COMPUTE)
                compute.p_task_pipe.send(task)
                self.last_task_response = self.entity.get_function(Function.COMPUTE).p_task_pipe.recv()
            else:
                self.last_task_response = self.handle(task)

    def recv(self):
        # if self.entity.has_function(Function.COMPUTE):
        #     self.last_task_response = self.entity.get_function(Function.COMPUTE).p_task_pipe.recv()

        temp = self.last_task_response
        self.last_task_response = None
        return temp

    def handle(self, task):
        raise NotImplementedError

    def handle_end(self):
        return TaskResponse(Status.END, value=None)
