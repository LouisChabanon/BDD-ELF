import os
import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def execute_queries(cursor, queries):
    for query in queries:
        try:
            cursor.execute(query)
            print(f"Execution: {query[:60]}...")
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution: {query[:60]}...")
            print(f"MySQL Error: {err}")

try:
    # Connexion initiale pour créer la base
    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD")
    )
    db_cursor = db_connection.cursor()

    DB_NAME = os.getenv("DB_NAME", "Inventaire_PJT")
    
    print(f"Suppression de l'ancienne base '{DB_NAME}' si elle existe.")
    db_cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    print(f"Création de la base '{DB_NAME}'.")
    db_cursor.execute(f"CREATE DATABASE {DB_NAME}")
    
    db_cursor.close()
    db_connection.close()

    # Reconnexion à la base de données spécifique
    print(f"Reconnexion à '{DB_NAME}'.")
    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        database=DB_NAME
    )
    db_cursor = db_connection.cursor()

    # Probleme avec emprunt : ne correspond pas à l'architecture: ne peux pas emprunter n produits
    # Ajout id_historique parce que plus simple
    table_queries = [
		"""
		CREATE TABLE Personnel(
          id_personnel INT PRIMARY KEY,
          mail TEXT,
          nom TEXT,
          prenom TEXT,
          type_personnel TEXT
            )
		""",
        """
		CREATE TABLE Matos(
          nom_materiel VARCHAR(100) PRIMARY KEY,
          photo_materiel TEXT,
          frequence_entretient TEXT,
          notice_materiel TEXT
            )
        """,
        """
        CREATE TABLE Rangement(
          lieu_rangement VARCHAR(100) PRIMARY KEY
            )
		""",
        """
		CREATE TABLE Kit(
          nom_kit VARCHAR(100) PRIMARY KEY
            )
		""",
        """
		CREATE TABLE Materiel(
          id_materiel INT PRIMARY KEY,
          date_garantie TEXT,
          date_dernier_entretient TEXT,
          derniere_localisation TEXT,
          nom_materiel VARCHAR(100),
          lieu_rangement VARCHAR(100),
          FOREIGN KEY (nom_materiel) REFERENCES Matos(nom_materiel),
          FOREIGN KEY (lieu_rangement) REFERENCES Rangement(lieu_rangement)
            )
		""",
        """
		CREATE TABLE Emprunt(
          id_emprunt INT PRIMARY KEY AUTO_INCREMENT,
          motif TEXT,
          date_emprunt TEXT,
          id_personnel INT,
          id_materiel INT,
          FOREIGN KEY (id_personnel) REFERENCES Personnel(id_personnel),
          FOREIGN KEY (id_materiel) REFERENCES Materiel(id_materiel)
            )
		""",
        """
		CREATE TABLE Historique(
          id_historique INT PRIMARY KEY AUTO_INCREMENT,
          date_rendu TEXT,
          id_materiel INT,
          id_personnel INT,
          FOREIGN KEY (id_personnel) REFERENCES Personnel(id_personnel),
          FOREIGN KEY (id_materiel) REFERENCES Materiel(id_materiel)
            )
		""",
        """
		CREATE TABLE Reservation(
          id_reservation INT PRIMARY KEY AUTO_INCREMENT,
          date_reservation TEXT,
          id_personnel INT,
          id_materiel INT,
          FOREIGN KEY (id_personnel) REFERENCES Personnel(id_personnel),
          FOREIGN KEY (id_materiel) REFERENCES Materiel(id_materiel)
            )
		""",
        """
		CREATE TABLE Kit_Materiel(
          id_kit_materiel INT PRIMARY KEY AUTO_INCREMENT,
          nom_kit VARCHAR(100),
          id_materiel INT,
          FOREIGN KEY (nom_kit) REFERENCES Kit(nom_kit),
          FOREIGN KEY (id_materiel) REFERENCES Materiel(id_materiel)
        )
		"""
    ]
    
    print("Implémentation des tables...")
    execute_queries(db_cursor, table_queries)
    
    print("Base de données et tables créees avec succès.")

except mysql.connector.Error as e:
     print(f"Erreur MySQL : {e}")
finally:
     if 'db_connection' in locals() and db_connection.is_connected():
          db_cursor.close()
          db_connection.close()
          print("Connexion MySQL fermée")

    
