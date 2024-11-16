import psycopg2
from dotenv import load_dotenv
import os
import uuid

class Adapter:
    def __init__(self, host=None, port=None, sslmode=None, dbname=None, user=None, password=None, target_session_attrs=None):
        load_dotenv(dotenv_path='./.env', verbose=True)
        self.host = host or os.getenv('DB_HOST')
        self.port = port or os.getenv('DB_PORT')
        self.sslmode = sslmode or "verify-full"
        self.dbname = dbname or os.getenv('DB_NAME')
        self.user = user or os.getenv('DB_USER')
        self.password = password or os.getenv('DB_PASSWORD')
        self.target_session_attrs = target_session_attrs or "read-write"
        self.conn = None
        self.cursor = None
        self.connect()

    def __del__(self):
        if self.conn:
            self.conn.close()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                target_session_attrs=self.target_session_attrs
            )
            self.cursor = self.conn.cursor()
        except Exception as error:
            print(f'connection error: {error}')
            exit(0)

    def select_sth_by_uuid(self, sth, table, uuid):
        request = f"SELECT {sth} FROM {table} WHERE uuid='{uuid}'"
        self.cursor.execute(request)
        data = self.cursor.fetchall()
        return data

    def select_sth(self, sth, table):
        request = f"""SELECT {sth} FROM {table}"""
        self.cursor.execute(request)
        data = self.cursor.fetchall()
        return data

    def update(self, table, request, uuid):
        print(f"Updating {table} with {request} where uuid={uuid}")
        request_update = f"UPDATE {table} SET {request} WHERE uuid='{uuid}'"
        self.cursor.execute(request_update)
        self.conn.commit()

    def insert(self, table, columns, values):
        request_insert = f"""INSERT INTO {table} ({columns}) VALUES ({values})"""
        self.cursor.execute(request_insert)
        self.conn.commit()

    def delete_by_uuid(self, table, uuid):
        request_delete = f"DELETE FROM {table} WHERE uuid='{uuid}'"
        self.cursor.execute(request_delete)
        self.conn.commit()

    def sel_userdata_by_email(self, email):
        request = "SELECT * FROM users WHERE email = %s"
        self.cursor.execute(request, (email,))
        data = self.cursor.fetchone()
        if data:
            column_names = [desc[0] for desc in self.cursor.description]
            data = dict(zip(column_names, data))
        return data

    def insert_userdata_inDB(self, username, hashed_password, email, is_active, activation_key):
        user_uuid = str(uuid.uuid4())
        request_insert = f"""INSERT INTO users (uuid, username, password, email, is_active, activation_key) 
                             VALUES ('{user_uuid}', '{username}', '{hashed_password}', '{email}', {is_active}, '{activation_key}')"""
        print(f"Executing query: {request_insert}")
        self.cursor.execute(request_insert)
        self.conn.commit()

    def sel_userdata_by_activation_key(self, email, activation_key):
        request_select = f"SELECT * FROM users WHERE email='{email}' AND activation_key='{activation_key}'"
        self.cursor.execute(request_select)
        data = self.cursor.fetchone()
        if data:
            column_names = [desc[0] for desc in self.cursor.description]
            data = dict(zip(column_names, data))
        return data