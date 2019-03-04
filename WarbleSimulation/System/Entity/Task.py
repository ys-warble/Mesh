from enum import Enum


class Command(Enum):
    START = 0
    END = 1

    ACTIVE = 101
    DEACTIVATE = 102

    GET_INFO = 201


class Task:
    def __init__(self, command, *args, **kwargs):
        self.command = command


class TaskResponse:
    def __init__(self, status, value):
        self.status = status
        self.value = value
