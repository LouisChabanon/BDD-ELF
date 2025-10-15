import mysql.connector

connection = None

def init_db():
    global connection
    connection = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="elf_database"
    )

    def get_db():
        return connection