import unittest
import os
from db import *
from dotenv import load_dotenv
import os
import bcrypt
import random

load_dotenv(dotenv_path='./.env', verbose=True)

class TestDB(unittest.TestCase):
    def test_select(self):
        try:
            db = Adapter(sslmode=None,target_session_attrs="read-write",schema="prod_test_db",host=os.getenv("DB_HOST"),port=os.getenv("DB_PORT"),dbname=os.getenv("DB_NAME"),user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"))
            print(db.select_sth("*","users"))
            self.assertIsNotNone(db.select_sth("*","users"))
        except:
            print("Ошибка подключения")
            self.assertEqual(0,1)

    def test_insert(self):
        try:
            db = Adapter(sslmode=None,target_session_attrs="read-write",schema="prod_test_db",host=os.getenv("DB_HOST"),port=os.getenv("DB_PORT"),dbname=os.getenv("DB_NAME"),user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"))
            test_name = "".join(["qwertyuiopasdghjklzxcvbnm"[random.randint(0,25)]*random.randint(3,14)])
            db.insert(values=f"'{test_name}','qwe'",table="users",columns="name,password")
            self.assertIsNotNone(db.select_sth("*","users"))
        except:
            print("Ошибка подключения")
            self.assertEqual(0,1)

    def test_update(self):
        try:
            db = Adapter(sslmode=None,target_session_attrs="read-write",schema="prod_test_db",host=os.getenv("DB_HOST"),port=os.getenv("DB_PORT"),dbname=os.getenv("DB_NAME"),user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"))
            test_name = "".join(["qwertyuiopasdghjklzxcvbnm"[random.randint(0,25)]*random.randint(3,14)])
            db.update(table="users",request="name = 'changed'",id=1)
            self.assertNotEqual(db.select_sth("*","users")[0][-1],test_name)
        except:
            print("Ошибка подключения")
            self.assertEqual(0,1)



if __name__ == "__main__":
    unittest.main()