from enum import Enum


class Command(Enum):
    START = 0
    END = 1

    ACTIVE = 101
    DEACTIVATE = 102

    GET_INFO = 201


class Status(Enum):
    OK = 0
    ERROR = 1


class Task:
    def __init__(self, command, *args, **kwargs):
        self.command = command

    def set_command(self, command):
        self.command = command

    def __str__(self):
        return "Task(%s)" % self.command


class TaskResponse:
    def __init__(self, status, value):
        self.status = status
        self.value = value

    def __str__(self):
        return "TaskResponse(%s, %s)" % (self.status, self.value)
