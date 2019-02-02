"""
@created: 01/28/2019
@author: Yosef Saputra
"""
import os
import sqlite3
import sys

import settings
from settings import db_file_path
from src import CommandInputThread, SqliteHandler

# System Table
system_table_name = 'system'
system_fields = [
    {'name': 'system_name', 'type': 'TEXT', 'pk': True},
    {'name': 'date_created', 'type': 'DATETIME', 'pk': False},
    {'name': 'date_modified', 'type': 'DATETIME', 'pk': False},
]


def main(args=None):
    print('===== Welcome to Warble Simulator! =====')

    print('main() args: ', end='')
    if args is not None:
        print(args[1:])

    # initialization
    initialize()

    # CommandHandler Loop
    ch = CommandInputThread.CommandInputThread()
    ch.run()


def initialize():
    # workspace
    # check if it exists. If not, create
    if not os.path.isdir(settings.workspace_path):
        os.makedirs(settings.workspace_path)

    # SQLite Database
    # check if it exists. If not, create
    if not os.path.isfile(db_file_path):
        try:
            conn = sqlite3.connect(db_file_path)

            sqlite_handler = SqliteHandler.SqliteHandler(conn)
            sqlite_handler.create_table(system_table_name, system_fields)

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(e)
    # TODO: check if the table is formatted correctly


if __name__ == '__main__':
    main(sys.argv)
