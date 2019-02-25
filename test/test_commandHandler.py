from unittest import TestCase

from src import CommandInputThread


class TestCommandHandler(TestCase):
    def test_command_parse(self):
        ch = CommandInputThread.CommandInputThread()

        cases = list()

        # System
        ans = dict((key, None) for key in ch.commandKeys)
        cases.append({'Q': 'create system --name myhome',
                      'A': {'command': ['create', 'system'], 'name': 'myhome', 'size': None, 'location': None,
                            'scale': None, 'timestamp': None}})
        cases.append({'Q': 'save system --name myhome',
                      'A': {'command': ['save', 'system'], 'name': 'myhome', 'size': None, 'location': None,
                            'scale': None, 'timestamp': None}})
        cases.append({'Q': 'load system --name myhome',
                      'A': {'command': ['load', 'system'], 'name': 'myhome', 'size': None, 'location': None,
                            'scale': None, 'timestamp': None}})
        cases.append({'Q': 'set system --name myhome',
                      'A': {'command': ['set', 'system'], 'name': 'myhome', 'size': None, 'location': None,
                            'scale': None, 'timestamp': None}})
        cases.append({'Q': 'clear system',
                      'A': {'command': ['clear', 'system'], 'name': None, 'size': None, 'location': None,
                            'scale': None, 'timestamp': None}})
        cases.append({'Q': 'system',
                      'A': {'command': ['system'], 'name': None, 'size': None, 'location': None, 'scale': None,
                            'timestamp': None}})
        # Space
        cases.append({'Q': 'space',
                      'A': {'command': ['space'], 'name': None, 'size': None, 'location': None, 'scale': None,
                            'timestamp': None}})
        cases.append({'Q': 'list space',
                      'A': {'command': ['list', 'space'], 'name': None, 'size': None, 'location': None, 'scale': None,
                            'timestamp': None}})
        cases.append({'Q': 'create space --size 100,100,100',
                      'A': {'command': ['create', 'space'], 'name': None, 'size': '100,100,100', 'location': None,
                            'scale': None, 'timestamp': None}})
        # Thing
        cases.append({'Q': 'list thing',
                      'A': {'command': ['list', 'thing'], 'name': None, 'size': None, 'location': None, 'scale': None,
                            'timestamp': None}})
        cases.append({'Q': 'create thing --name mything',
                      'A': {'command': ['create', 'thing'], 'name': 'mything', 'size': None, 'location': None,
                            'scale': None, 'timestamp': None}})
        cases.append({'Q': 'move thing --name mything --location 1,1,1',
                      'A': {'command': ['move', 'thing'], 'name': 'mything', 'size': None, 'location': '1,1,1',
                            'scale': None, 'timestamp': None}})
        # Time
        cases.append({'Q': 'time',
                      'A': {'command': ['time'], 'name': None, 'size': None, 'location': None, 'scale': None,
                            'timestamp': None}})
        cases.append({'Q': 'fw',
                      'A': {'command': ['fw'], 'name': None, 'size': None, 'location': None, 'scale': None,
                            'timestamp': None}})
        cases.append({'Q': 'bw',
                      'A': {'command': ['bw'], 'name': None, 'size': None, 'location': None, 'scale': None,
                            'timestamp': None}})
        cases.append({'Q': 'stop',
                      'A': {'command': ['stop'], 'name': None, 'size': None, 'location': None, 'scale': None,
                            'timestamp': None}})
        cases.append({'Q': 'run --scale 0.5 --timestamp 100',
                      'A': {'command': ['run'], 'name': None, 'size': None, 'location': None, 'scale': 0.5,
                            'timestamp': 100}})

        for case in cases:
            self.assertDictEqual(
                case['A'],
                vars(ch.command_parse(case['Q']))
            )
