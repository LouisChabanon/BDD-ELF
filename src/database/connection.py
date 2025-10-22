import mysql.connector

connection = None

def init_db():
    global connection
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            port="3306",
            password="",
            database="Inventaire_PJT"
        )
    except mysql.connector.Error as err:
        raise Exception(f"Erreur de connexion à la base de données : {err}")

def get_db():
    return connection