from enum import Enum

from WarbleSimulation.System.Entity.Function import BaseFunction


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
        super().__init__()

    def send(self, task):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError

    def handle(self, task):
        raise NotImplementedError
