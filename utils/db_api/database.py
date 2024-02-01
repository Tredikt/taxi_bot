from sqlite3 import connect


class DataBase:
    def __init__(self, db_name):
        self.db = connect(database=db_name)