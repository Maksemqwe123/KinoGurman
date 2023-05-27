from KinoGurman.config import *


class MyDBPostgres:
    def __init__(self):
        self.conn = connection
        self.cursor = connection.cursor()

        self._create_table_db_dessert()
        self._create_table_db_kinogo()

    def _create_table_db_dessert(self):
        sql_table = """CREATE TABLE IF NOT EXISTS db_dessert (
        ID SERIAL PRIMARY KEY NOT NULL,
        USER_ID BIGINT,
        USERNAME VARCHAR(30),
        NAME_DESSERT VARCHAR(30),
        ENTRY_DATE TIMESTAMP
        );
        """

        with self.conn:
            self.cursor.execute(sql_table)

    def _create_table_db_kinogo(self):
        sql_table = """CREATE TABLE IF NOT EXISTS db_kinogo (
        ID SERIAL PRIMARY KEY NOT NULL,
        USER_ID BIGINT,
        USERNAME VARCHAR(30),
        GENRE_FILM VARCHAR(30),
        ENTRY_DATE TIMESTAMP
        );
        """

        with self.conn:
            self.cursor.execute(sql_table)

    def insert_table_db_kinogo(self, user_id, username, entry_date):
        insert_sql_table = "INSERT INTO db_kinogo (user_id, username, entry_date) VALUES (%s, %s, %s)"

        with self.conn:
            self.cursor.execute(insert_sql_table, (user_id, username, entry_date))

    def insert_table_db_dessert(self, user_id, username, entry_date):
        insert_sql_table = "INSERT INTO db_dessert (user_id, username, entry_date) VALUES (%s, %s, %s)"

        with self.conn:
            self.cursor.execute(insert_sql_table, (user_id, username, entry_date))

    def update_db_kinogo(self, user_id, genre_film):
        sql_update = 'UPDATE db_kinogo SET genre_film = (%s) WHERE user_id = (%s)'

        with self.conn:
            self.cursor.execute(sql_update, (genre_film, user_id))

    def update_db_dessert(self, user_id, name_dessert):
        sql_update = 'UPDATE db_dessert SET name_dessert = (%s) WHERE user_id = (%s)'

        with self.conn:
            self.cursor.execute(sql_update, (name_dessert, user_id))

    def select_table(self, name_table, user_id):
        select_sql = 'SELECT user_id FROM ' + name_table + ' WHERE user_id =  ' + str(user_id)

        with self.conn:
            self.cursor.execute(select_sql)
        result = self.cursor.fetchall()
        return result

