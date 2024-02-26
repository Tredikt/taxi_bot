from sqlite3 import connect


class DataBase:
    def __init__(self, db_name):
        self.conn = connect(database=db_name)
        self.cur = self.conn.cursor()

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                tg_id INTEGER PRIMARY KEY,
                username TEXT,
                fullname TEXT
            )
            """
        )

        self.conn.commit()