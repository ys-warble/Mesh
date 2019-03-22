from enum import Enum
from multiprocessing import Process

from WarbleSimulation.System.Entity.Function import BaseFunction, Function


class TaskLevel(Enum):
    PROGRAM = 0
    SYSTEM = 100
    ENTITY = 200


class TaskName(Enum):
    START = 0
    END = 1

    GET_SYSTEM_INFO = 101
    ACTIVE = 102
    DEACTIVATE = 103

    GET_INFO = 201


class Status(Enum):
    OK = 0
    ERROR = 1


class BaseTask:
    def __init__(self, level, name, *args, **kwargs):
        self.level = level
        self.name = name

    def __str__(self):
        return "Task(%s,%s)" % (self.level, self.name)

    def __eq__(self, other):
        return type(self) == type(other) and self.level == other.level and self.name == other.name


class ProgramTask(BaseTask):
    def __init__(self, name, *args, **kwargs):
        super().__init__(TaskLevel.PROGRAM, name, args, kwargs)


class SystemTask(BaseTask):
    def __init__(self, name, *args, **kwargs):
        super().__init__(TaskLevel.SYSTEM, name, args, kwargs)


class Task(BaseTask):
    def __init__(self, name, *args, **kwargs):
        super().__init__(TaskLevel.ENTITY, name, args, kwargs)


class TaskResponse:
    def __init__(self, status, value):
        self.status = status
        self.value = value

    def __str__(self):
        return "TaskResponse(%s, %s)" % (self.status, self.value)

    def __eq__(self, other):
        return self.status == other.status and self.value == self.value


class Tasked(BaseFunction):
    tasks = [
        TaskName.GET_SYSTEM_INFO,
        TaskName.ACTIVE,
        TaskName.DEACTIVATE,

        TaskName.GET_INFO,
    ]

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

    def validate(self, task):
        if self.supported_tasks is None:
            self.eval()

        return True if (task.name in self.supported_tasks and task.level.value == int(
            task.name.value / 100) * 100) else False

    def send(self, task):
        def send_basic(t_task):
            return self.main_handle(t_task)

        self.last_task = task
        if self.entity.has_function(Function.COMPUTE):
            compute = self.entity.get_function(Function.COMPUTE)
            if task == ProgramTask(TaskName.START) and not compute.is_computing():
                compute.process = Process(target=compute.run)
                compute.process.start()
                self.last_task_response = TaskResponse(status=Status.OK, value=None)
            elif task == ProgramTask(TaskName.END) and compute.is_computing():
                compute.p_task_pipe.send(task)
                compute.process.join()
                compute.process = None
                self.last_task_response = TaskResponse(status=Status.OK, value=None)
            elif not compute.is_computing():
                self.last_task_response = send_basic(task)
            elif compute.is_computing():
                compute.p_task_pipe.send(task)
        else:
            self.last_task_response = send_basic(task)

    def recv(self):
        if self.entity.has_function(Function.COMPUTE) and self.entity.get_function(Function.COMPUTE).is_computing():
            if self.last_task != ProgramTask(TaskName.START):
                self.last_task_response = self.entity.get_function(Function.COMPUTE).p_task_pipe.recv()

        temp = self.last_task_response
        self.last_task_response = None
        return temp

    def main_handle(self, task):
        if not self.validate(task):
            return TaskResponse(Status.ERROR, {'error': 'Not Implemented'})
        else:
            return self.handle(task)

    def handle(self, task):
        raise NotImplementedError
