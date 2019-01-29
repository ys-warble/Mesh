"""
@created: 01/28/2019
@author: Yosef Saputra
"""
import argparse


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


class CommandHandler:
    def __init__(self):
        self.identifier = "CommandHandler"
        self.commandParser, self.commandKeys = _build_command_parser()

    def command_parse(self, userInput):
        '''
        Calling parse_args of argparse.ArgumentParser()
        :param userInput: String
        :return: Namespace()
        '''
        return self.commandParser.parse_args(userInput.split())

    def execute(self):
        '''
        Main execution function in indefinite loop
        :return:
        '''
        while True:
            userInput = input()

            if len(userInput) == 0:
                continue

            command = self.command_parse(userInput)
