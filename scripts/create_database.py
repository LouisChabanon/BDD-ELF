import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def execute_queries(cursor, queries):
    for query in queries:
        try:
            cursor.execute(query)
            print(f"Execution success: {query.strip().splitlines()[0]}...")
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")

try:
    # 1. Initial Connection (to create DB if missing)
    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "3306"),
        user=os.getenv("DB_USER", "root"),
        passwd=os.getenv("DB_PASSWORD", "")
    )
    db_cursor = db_connection.cursor()

    DB_NAME = os.getenv("DB_NAME", "Inventaire_PJT")

    # Check/Create Database safely
    print(f"Checking database '{DB_NAME}'...")
    db_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    
    db_cursor.close()
    db_connection.close()

    # 2. Reconnection to the specific Database
    print(f"Connecting to '{DB_NAME}'...")
    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "3306"),
        user=os.getenv("DB_USER", "root"),
        passwd=os.getenv("DB_PASSWORD", ""),
        database=DB_NAME
    )
    db_cursor = db_connection.cursor()

    # 3. Table Creation
    table_queries = [
        """
        CREATE TABLE IF NOT EXISTS Notice(
            notice_materiel VARCHAR(100) PRIMARY KEY
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Personnel(
            id_personnel INT PRIMARY KEY,
            mail TEXT,
            nom TEXT,
            prenom TEXT,
            type_personnel TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Rangement(
            lieu_rangement VARCHAR(100) PRIMARY KEY
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Materiel(
            nom_materiel VARCHAR(100) PRIMARY KEY,
            photo_materiel TEXT,
            frequence_entretient TEXT,
            notice_materiel VARCHAR(100),
            FOREIGN KEY (notice_materiel) REFERENCES Notice(notice_materiel)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Kit(
            nom_kit VARCHAR(100) PRIMARY KEY
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Exemplaire(
            id_exemplaire INT PRIMARY KEY,
            date_garantie TEXT,
            date_dernier_entretient TEXT,
            derniere_localisation TEXT,
            nom_materiel VARCHAR(100),
            lieu_rangement VARCHAR(100),
            FOREIGN KEY (nom_materiel) REFERENCES Materiel(nom_materiel),
            FOREIGN KEY (lieu_rangement) REFERENCES Rangement(lieu_rangement)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Emprunt(
            id_emprunt INT PRIMARY KEY AUTO_INCREMENT,
            motif TEXT,
            date_emprunt TEXT,
            id_personnel INT,
            id_exemplaire INT,
            FOREIGN KEY (id_personnel) REFERENCES Personnel(id_personnel),
            FOREIGN KEY (id_exemplaire) REFERENCES Exemplaire(id_exemplaire)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Reservation(
            id_reservation INT PRIMARY KEY AUTO_INCREMENT,
            date_reservation TEXT,
            date_fin_reservation TEXT,
            id_personnel INT,
            id_exemplaire INT,
            FOREIGN KEY (id_personnel) REFERENCES Personnel(id_personnel),
            FOREIGN KEY (id_exemplaire) REFERENCES Exemplaire(id_exemplaire)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Kit_Materiel(
            id_kit_materiel INT PRIMARY KEY AUTO_INCREMENT,
            nom_kit VARCHAR(100),
            nom_materiel VARCHAR(100),
            FOREIGN KEY (nom_kit) REFERENCES Kit(nom_kit),
            FOREIGN KEY (nom_materiel) REFERENCES Materiel(nom_materiel)
        )
        """
    ]
    
    print("Updating tables structure...")
    execute_queries(db_cursor, table_queries)
    
    print("Seeding data (skipping duplicates)...")
    
    try:
        # 0. Notice (Must be first because Materiel needs it)
        query_notice = "INSERT IGNORE INTO Notice (notice_materiel) VALUES (%s)"
        data_notice = [
            ('notice_mascarpone',), ('notice_boudoirs',), ('notice_café',), 
            ('notice_chocolat',), ('notice_sucre',), ('notice_oeufs',),
            ('notice_poireaux',), ('notice_patate',), ('notice_sel',), ('notice_carotte',)
        ]
        db_cursor.executemany(query_notice, data_notice)
        print(f"  -> Notices checked/added.")

        # 1. Personnel
        query_personnel = "INSERT IGNORE INTO Personnel (id_personnel, mail, type_personnel, nom, prenom) VALUES (%s, %s, %s, %s, %s)"
        data_personnel = [
           (164, 'chloe.duffau@ensam.eu', 'doctorant', 'Dufau', 'Chloe'),
           (94165, 'zoe.hautreux@ensam.eu', 'doctorant', 'Hautreux', 'Zoé'), 
           (16852, 'adrien.ungemuth@ensam.eu', 'doctorant', 'Ungemuth', 'Adrien'), 
           (24, 'louis.chabanon@ensam.eu', 'doctorant', 'Chabanon', 'Louis'),
           (35, 'rayen.nouri@ensam.eu', 'doctorant', 'Nouri', 'Rayen')
        ]
        db_cursor.executemany(query_personnel, data_personnel)
        print(f"  -> Personnel checked/added.")

        # 2. Rangement
        query_rangement = "INSERT IGNORE INTO Rangement (lieu_rangement) VALUES (%s)"
        data_rangement = [
            ('placard',), ('frigo',), ('garage',)
        ]
        db_cursor.executemany(query_rangement, data_rangement)
        print(f"  -> Rangement checked/added.")

        # 3. Materiel
        query_materiel = "INSERT IGNORE INTO Materiel (nom_materiel, photo_materiel, frequence_entretient, notice_materiel) VALUES (%s, %s, %s, %s)"
        data_materiel = [
            ('mascarpone', 'photo_mascarpone', '1', 'notice_mascarpone'),
            ('boudoirs', 'photo_boudoirs', '2', 'notice_boudoirs'),
            ('café', 'photo_café', '1', 'notice_café'),
            ('chocolat', 'photo_chocolat', '1', 'notice_chocolat'),
            ('sucre', 'photo_sucre', '2', 'notice_sucre'),
            ('oeufs', 'photo_oeufs', '1', 'notice_oeufs'),
            ('poireaux', 'photo_poireaux', '3', 'notice_poireaux'),
            ('patate', 'photo_patate', '6', 'notice_patate'),
            ('sel', 'photo_sel', '6', 'notice_sel'),
            ('carotte', 'photo_carotte', '1', 'notice_carotte')       
        ]
        db_cursor.executemany(query_materiel, data_materiel)
        print(f"  -> Materiel checked/added.")
        
        # 4. Exemplaire
        query_exemplaire = "INSERT IGNORE INTO Exemplaire (id_exemplaire, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel, lieu_rangement) VALUES (%s, %s, %s, %s, %s, %s)"
        data_exemplaire = [
            (10001, '01_01_2026', '01_09_2025', 'garage', 'mascarpone', 'frigo'), 
            (10002, '01_01_2026', '01_09_2025', 'garage', 'boudoirs', 'garage'),
            (10003, '01_01_2026', '01_09_2025', 'garage', 'boudoirs', 'garage'),
            (10004, '01_01_2026', '01_09_2025', 'garage', 'boudoirs', 'garage'),
            (10005, '01_01_2026', '01_09_2025', 'garage', 'café', 'frigo'),
            (10006, '01_01_2026', '01_09_2025', 'garage', 'café', 'frigo'),
            (10007, '01_01_2026', '01_09_2025', 'garage', 'chocolat', 'placard'),
            (10008, '01_01_2026', '01_09_2025', 'garage', 'sucre', 'placard'),
            (10009, '01_01_2026', '01_09_2025', 'garage', 'oeufs', 'frigo'),
            (10010, '01_01_2026', '01_09_2025', 'garage', 'oeufs', 'frigo'),
            (10011, '01_01_2026', '01_09_2025', 'garage', 'oeufs', 'frigo'),
            (10012, '01_01_2026', '01_09_2025', 'garage', 'oeufs', 'frigo'),
            (10013, '01_01_2026', '01_09_2025', 'garage', 'oeufs', 'frigo'),
            (10014, '01_01_2026', '01_09_2025', 'garage', 'oeufs', 'frigo')
        ]
        db_cursor.executemany(query_exemplaire, data_exemplaire)
        print(f"  -> Exemplaires checked/added.")

        # 5. Kit
        query_kit = "INSERT IGNORE INTO Kit (nom_kit) VALUES (%s)"
        data_kit = [('tiramisu',), ('mousse_au_chocolat',), ('soupe',)]
        db_cursor.executemany(query_kit, data_kit)
        print(f"  -> Kits checked/added.")

        # 6. Kit_Materiel
        query_kit_mat = "INSERT IGNORE INTO Kit_Materiel (nom_kit, nom_materiel) VALUES (%s, %s)"
        data_kit_mat = [
            ('tiramisu', 'mascarpone'),
            ('tiramisu', 'oeufs'),
            ('tiramisu', 'sucre'),
            ('tiramisu', 'café'),
            ('tiramisu', 'boudoirs'),
            ('mousse_au_chocolat','oeufs'),
            ('mousse_au_chocolat', 'chocolat'),
            ('soupe' , 'poireaux'),
            ('soupe' , 'patate'),
            ('soupe' , 'sel' ),
            ('soupe' , 'carotte')
        ]
        db_cursor.executemany(query_kit_mat, data_kit_mat)
        print(f"  -> Kit_Materiel links checked/added.")

        # 7. Reservation
        query_res = "INSERT IGNORE INTO Reservation (date_reservation, date_fin_reservation, id_personnel, id_exemplaire) VALUES (%s, %s, %s, %s)"
        data_res = [
            ('01_12_2025', '07_12_2025', 164, 10001) 
        ]
        db_cursor.executemany(query_res, data_res)
        print(f"  -> Reservations checked/added.")

        # 8. Emprunt
        query_emp = "INSERT IGNORE INTO Emprunt (motif, date_emprunt, id_exemplaire, id_personnel) VALUES (%s, %s, %s, %s)"
        data_emp = [
            ("J'invite des amis", '05_12_2025', 10002, 94165) 
        ]
        db_cursor.executemany(query_emp, data_emp)
        print(f"  -> Emprunts checked/added.")

        db_connection.commit()
        print("\nSeeding complete.")

    except mysql.connector.Error as err:
        print(f"Error during seeding: {err}")
        db_connection.rollback()

    print("\nDatabase check/setup finished successfully.")

except mysql.connector.Error as e:
     print(f"Critical MySQL Error: {e}")
finally:
     if 'db_connection' in locals() and db_connection.is_connected():
          db_cursor.close()
          db_connection.close()
          print("MySQL connection closed.")