import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
connection = None

def init_db():
    global connection
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            port=os.getenv("DB_PORT"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    except mysql.connector.Error as err:
        raise Exception(f"Erreur de connexion à la base de données : {err}")

def get_db():
    return connection