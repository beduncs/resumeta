import sqlite3
import argparse
from sqlite3 import Error
from pathlib import Path

class DBConnection:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            self.create_database(self.db_path)
        self.connection = self.create_connection(self.db_path)
        self.cursor = self.create_cursor(self.connection)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def create_database(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_cursor(self, conn):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            cursor = conn.cursor()
            return cursor
        except Error as e:
            print(e)

    def execute_sql_statement(self, sql_statement):
        try:
            sql_return = self.cursor.execute(sql_statement)
            return sql_return
        except Error as e:
            print(e)
        
    def execute_sql_file(self, sql_file_path):
        # Open and read the file as a single buffer
        with open(sql_file_path, 'r') as open_file:
            sql_file = open_file.read()

        # all SQL commands (split on ';')
        sql_commands = sql_file.split(';')

        # Execute every command from the input file
        for command in sql_commands:
            self.execute_sql_statement(command)

class DBOperator:
    def __init__(self, db_conn: DBConnection):
        self.db_conn = db_conn

    def insert_job(self, title, begin_date, end_date, job_workplace):
        sql_statement = f'''
        INSERT INTO job (title, begin_date, end_date, job_workplace)
        VALUES( '{title}', '{begin_date}', '{end_date}', '{job_workplace}');
        '''
        self.db_conn.execute_sql_statement(sql_statement)
