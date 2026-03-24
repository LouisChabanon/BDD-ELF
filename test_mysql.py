import os
from dotenv import load_dotenv
import mysql.connector

# Charger le .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "Inventaire_PJT")

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        use_pure=True  # force TCP/IP et évite le named pipe
    )
    print(f"[OK] Connexion MySQL réussie à '{DB_NAME}' !")
    conn.close()
except Exception as e:
    print(f"[ERREUR] Impossible de se connecter : {e}")