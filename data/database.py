import pymysql
from data.config import *

class Database:
    def __init__(self, HOST, USER, PASSWORD, DBNAME):
        self.con = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DBNAME
        )
        self.cursor = self.con.cursor()

    def getTables(self):
        try:
            self.cursor.execute('show tables')
            return [x for (x, ) in self.cursor.fetchall()]
        except:
            raise

    def getDataFromTable(self, table_name):
        try:
            self.cursor.execute(f"describe {table_name}")
            labels = [x[0] for x in self.cursor.fetchall()]
            self.cursor.execute(f'select * from {table_name}')
            data = self.cursor.fetchall()
            return [labels, data]
        except:
            raise

    def getTableLabels(self, table_name):
        try:
            self.cursor.execute(f'describe {table_name}')
            return [x[0] for x in self.cursor.fetchall()]
        except:
            raise

    def updateDB(self, table, new_data, data_column, id_data, id_column):
        try:
            self.cursor.execute(f"update {table} set {data_column} = '{new_data}' "
                                f"where {id_column} = {id_data}")
            self.con.commit()
        except:
            raise

    def delRecord(self, table, record_id, id_column):
        try:
            self.cursor.execute(f"DELETE FROM {table} WHERE {id_column} = {record_id}")
            self.con.commit()
        except:
            raise

    def addRecord(self, table_name, columns, values):
        try:
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(values))


            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            self.cursor.execute(query, values)
            self.con.commit()
        except:
            raise

    def checkUser(self, login, password):
        try:
            self.cursor.execute(f"select roles.id from users "
                                f"inner join roles on roles.id = users.id_role "
                                f"where login = %s and password = %s", (login, password))
            role_id = self.cursor.fetchall()
            return role_id[0][0]
        except:
            raise

    def addNewEmployee(self, name, login, password, role):
        try:
            self.cursor.execute(f"insert into employees(name, login, password, role_id) "
                                f"values(%s, %s, %s, (select id from roles "
                                f"where role_name = %s))", (name, login, password, role))
            self.con.commit()
        except:
            raise
