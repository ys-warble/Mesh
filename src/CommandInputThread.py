"""
@created: 01/28/2019
@author: Yosef Saputra
"""
import argparse
import sqlite3
import threading

import run
from src.SqliteHandler import SqliteHandler


def _build_command_parser():
    parser = argparse.ArgumentParser()
    keys = list()

    parser.add_argument('command', nargs='+', type=str, help="command")
    keys.append('command')
    parser.add_argument('-n', '--name', help='name')
    keys.append('name')
    parser.add_argument('-s', '--size', help='size')
    keys.append('size')
    parser.add_argument('-l', '--location', help='location')
    keys.append('location')
    parser.add_argument('-r', '--scale', type=float, help='time scale')
    keys.append('scale')
    parser.add_argument('-t', '--timestamp', type=int, help='timestamp')
    keys.append('timestamp')

    return parser, keys


class CommandInputThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stopEvent = threading.Event()
        self.commandParser, self.commandKeys = _build_command_parser()

    def command_parse(self, user_input):
        """
        Calling parse_args of argparse.ArgumentParser()
        :param user_input: String
        :return: Namespace()
        """
        return self.commandParser.parse_args(user_input.split())

    def run(self):
        """
        Main execution function in indefinite loop
        :return:
        """
        while not self.stopEvent.is_set():
            user_input = input('>> ')

            if len(user_input) == 0:
                continue
            else:
                full_command = vars(self.command_parse(user_input))
                self.handle_command(full_command)

    def join(self, th_cmd='stop'):
        if th_cmd == 'stop':
            self.stopEvent.set()
        else:
            pass

    def handle_command(self, full_command):
        if any(cmd in full_command['command'] for cmd in ['quit', 'exit']):
            self.stopEvent.set()

        elif full_command['command'] == ['list', 'system']:
            conn = sqlite3.connect(run.db_file_path)

            sqlite_handler = SqliteHandler(conn)
            c = sqlite_handler.select(run.system_table_name, '*')

            res = []
            if c is not None:
                res = c.fetchall()

            print(('+' + '-' * 25) * len(run.system_fields) + '+')

            string = ''
            for j in range(len(run.system_fields)):
                string += '| %23s ' % [d['name'] for d in run.system_fields][j]
            print(string + '|')

            print(('+' + '-' * 25) * len(run.system_fields) + '+')

            for i in range(len(res)):
                string = ''
                for j in range(len(run.system_fields)):
                    string += '| %23s ' % res[i][j]
                print(string + '|')

            print(('+' + '-' * 25) * len(run.system_fields) + '+')

        else:
            print('Invalid Command: %s' % full_command)
