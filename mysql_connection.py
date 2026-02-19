import mysql.connector

class MySQLConnection:
    def __init__(self):
        self.conn=None
        self.cursor=None

    def setup_connection(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",  # your MySQL username
            password="Root@123",  # your MySQL password
            database="mysql"  # your database name
        )

        self.cursor = self.conn.cursor()

    def execute_query(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()