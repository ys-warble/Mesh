import sqlite3


class SqliteHandler:
    def __init__(self, conn):
        """
        Constructor
        :param conn: (Connection) database connection object
        """
        self.conn = conn

    def execute_db_cmd(self, db_cmd):
        try:
            c = self.conn.cursor()
            c.execute(db_cmd)
            return c
        except sqlite3.IntegrityError as e:
            print(e)

    def create_table(self, name, columns):
        """

        :param name: (str) table name
        :param columns: (dict) with keys: name, type, pk (for primary key)
        :return:
        """

        db_cmd = 'CREATE TABLE {name} ('.format(name=name)
        for col in columns:
            db_cmd += ' '.join([col['name'], col['type']])
            if col['pk']:
                db_cmd += ' PRIMARY KEY'
            db_cmd += ', '
        db_cmd = db_cmd[:-2] + ')'

        return self.execute_db_cmd(db_cmd)

    def insert_into(self, name, columns, values):
        """

        :param name: (str) table name
        :param columns: (list) column names
        :param values: (list) column values
        :return:
        """

        db_cmd = 'INSERT INTO {name} '.format(name=name)
        db_cmd += '(' + ','.join(columns) + ')'
        db_cmd += ' VALUES '
        db_cmd += '(' + ','.join(values) + ')'

        return self.execute_db_cmd(db_cmd)

    def select(self, name, columns):
        """

        :param name:
        :param columns:
        :return:
        """

        db_cmd = 'SELECT {columns} FROM {name}'.format(columns=columns, name=name)
        return self.execute_db_cmd(db_cmd)
