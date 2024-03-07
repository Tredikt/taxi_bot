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

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS drivers(
                tg_id INTEGER PRIMARY KEY,
                fio TEXT,
                dli TEXT,
                arc TEXT,
                auto TEXT,
                brand TEXT,
                status TEXT
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS orders(
                customer_id INTEGER,
                order_text TEXT
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS order_message(
                customer_id INTEGER,
                driver_id INTEGER,
                m_id INTEGER
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS bunches(
                customer_id INTEGER,
                driver_id INTEGER
            )
            """
        )

        self.conn.commit()

    def get_users(self):
        users_id = self.cur.execute(
            """
            SELECT tg_id FROM users
            """
        ).fetchall()

        return [elem[0] for elem in users_id] if users_id else []

    def add_user(self, tg_id: int, username: str, fullname: str):
        self.cur.execute(
            """
            INSERT OR REPLACE INTO users
            (tg_id, username, fullname)
            VALUES
            (?, ?, ?)
            """,
            (tg_id, username, fullname)
        )

        self.conn.commit()

    def get_user(self, tg_id: int):
        user_info = self.cur.execute(
            """
            SELECT username, fullname FROM users
            WHERE tg_id = ?
            """,
            (tg_id,)
        ).fetchone()

        return user_info if user_info else ()

    def add_driver(self, tg_id: int, fio: str, dli: str, arc: str, auto: str, brand: str, status: str):
        self.cur.execute(
            """
            INSERT OR REPLACE INTO drivers
            (tg_id, fio, dli, arc, auto, brand, status)
            VALUES
            (?, ?, ?, ?, ?, ?, ?)
            """,
            (tg_id, fio, dli, arc, auto, brand, status)
        )

        self.conn.commit()

    def approve_driver(self, tg_id: int):
        self.cur.execute(
            """
            UPDATE drivers
            SET status = 'approved'
            WHERE tg_id = ?
            """,
            (tg_id,)
        )

        self.conn.commit()

    def get_car_brand(self, driver_id: int):
        car_brand = self.cur.execute(
            """
            SELECT brand FROM drivers
            WHERE tg_id = ?
            """,
            (driver_id,)
        ).fetchone()

        return car_brand[0] if car_brand else ""


    def decline_driver(self, tg_id: int):
        self.cur.execute(
            """
            UPDATE drivers
            SET status = 'declined'
            WHERE tg_id = ?
            """,
            (tg_id,)
        )

        self.conn.commit()

    def get_approved_drivers(self):
        drivers_id = self.cur.execute(
            """
            SELECT tg_id FROM drivers
            WHERE status = 'approved'
            """
        ).fetchall()

        return [elem[0] for elem in drivers_id] if drivers_id else []

    def add_order(self, customer_id: int, order_text: str):
        self.cur.execute(
            """
            INSERT INTO orders
            (customer_id, order_text)
            VALUES
            (?, ?)
            """,
            (customer_id, order_text)
        )

        self.conn.commit()

    def get_order_text(self, customer_id: int):
        text = self.cur.execute(
            """
            SELECT order_text FROM orders
            WHERE customer_id = ?
            """,
            (customer_id, )
        ).fetchone()

        return text[0] if text else ""

    def delete_order_text(self, customer_id: int):
        self.cur.execute(
            """
            DELETE FROM orders
            WHERE customer_id = ?
            """,
            (customer_id,)
        )

        self.conn.commit()

    def add_order_message(self, customer_id: int, driver_id: int, m_id: int):
        self.cur.execute(
            """
            INSERT INTO order_message
            (customer_id, driver_id, m_id)
            VALUES
            (?, ?, ?)
            """,
            (customer_id, driver_id, m_id)
        )

        self.conn.commit()

    def get_order_message(self, customer_id: int, driver_id: int):
        m_id = self.cur.execute(
            """
            SELECT m_id FROM order_message
            WHERE customer_id = ?
            AND driver_id = ?
            """,
            (customer_id, driver_id)
        ).fetchone()

        return m_id[0] if m_id else 0

    def delete_order_message(self, customer_id: int):
        self.cur.execute(
            """
            DELETE FROM order_message
            WHERE customer_id = ?
            """,
            (customer_id,)
        )

        self.conn.commit()

    def add_bunch(self, customer_id: int, driver_id: int):
        self.cur.execute(
            """
            INSERT INTO bunches
            (customer_id, driver_id)
            VALUES
            (?, ?)
            """,
            (customer_id, driver_id)
        )

        self.conn.commit()

    def get_customer_bunch(self, driver_id: int):
        customer_id = self.cur.execute(
            """
            SELECT customer_id FROM bunches
            WHERE driver_id = ?
            """,
            (driver_id,)
        ).fetchone()

        return customer_id[0] if customer_id else 0

    def get_driver_bunch(self, customer_id: int):
        driver_id = self.cur.execute(
            """
            SELECT driver_id FROM bunches
            WHERE customer_id = ?
            """,
            (customer_id,)
        ).fetchone()

        return driver_id[0] if driver_id else 0

    def delete_bunch(self, driver_id: int):
        self.cur.execute(
            """
            DELETE FROM bunches
            WHERE driver_id = ?
            """,
            (driver_id,)
        )

        self.conn.commit()
