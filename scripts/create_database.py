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
    # Ajout Date fin réservation
    # Ajout motif à historique
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
		CREATE TABLE Materiel(
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
		CREATE TABLE Exemplaire(
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
		CREATE TABLE Emprunt(
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
		CREATE TABLE Historique(
          id_historique INT PRIMARY KEY AUTO_INCREMENT,
          date_rendu TEXT,
          motif TEXT,
          id_exemplaire INT,
          id_personnel INT,
          FOREIGN KEY (id_personnel) REFERENCES Personnel(id_personnel),
          FOREIGN KEY (id_exemplaire) REFERENCES Exemplaire(id_exemplaire)
            )
		""",
        """
		CREATE TABLE Reservation(
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
		CREATE TABLE Kit_Materiel(
          id_kit_materiel INT PRIMARY KEY AUTO_INCREMENT,
          nom_kit VARCHAR(100),
          nom_materiel VARCHAR(100),
          FOREIGN KEY (nom_kit) REFERENCES Kit(nom_kit),
          FOREIGN KEY (nom_materiel) REFERENCES Materiel(nom_materiel)
        )
		"""
    ]
    
    print("Implémentation des tables...")
    execute_queries(db_cursor, table_queries)
    
	# -----------------------------------------------------
    # --- AJOUT DES DONNÉES INITIALES (SEEDING) ---
    # -----------------------------------------------------
    print("Ajout des données initiales (seeding)...")
    
    try:
        # 1. Personnel
        query_personnel = "INSERT INTO Personnel (id_personnel, mail, type_personnel, nom, prenom) VALUES (%s, %s, %s, %s, %s)"
        data_personnel = [
           (164, 'chloe.duffau@ensam.eu', 'doctorant', 'Duffau', 'Chloe'),
           (94165, 'zoe.hautreux@ensam.eu', 'doctorant', 'Hautreux', 'Zoé'), 
           (16852, 'adrien.ungemuth@ensam.eu', 'doctorant', 'Ungemuth', 'Adrien'), 
           (24, 'louis.chabanon@ensam.eu', 'doctorant', 'Chabanon', 'Louis'),
             (35, 'rayen.nouri@ensam.eu', 'doctorant', 'Nouri', 'Rayen')
        ]
        db_cursor.executemany(query_personnel, data_personnel)
        print(f"  -> {len(data_personnel)} utilisateurs ajoutés.")

        # 2. Rangement
        query_rangement = "INSERT INTO Rangement (lieu_rangement) VALUES (%s)"
        data_rangement = [
            ('placard',), ('frigo',), ('garage',)
        ]
        db_cursor.executemany(query_rangement, data_rangement)
        print(f"  -> {len(data_rangement)} lieux de rangement ajoutés.")

        # 3. Materiel (Modèles de matériel)
        query_materiel = "INSERT INTO Materiel (nom_materiel, photo_materiel, frequence_entretient, notice_materiel) VALUES (%s, %s, %s, %s)"
        data_materiel = [('mascarpone', 'photo_mascarpone',1, 'notice_mascarpone' ) 
            ,('boudoirs', 'photo_boudoirs' ,2,  'notice_boudoirs')
            ,('café', 'photo_café' , 1, 'notice_café')
            ,( 'chocolat' , 'photo_chocolat' , 1 , 'notice_chocolat' )
            ,( 'sucre', 'photo_sucre', 2, 'notice_sucre')
            ,( 'œufs', 'photo_oeufs', 1 , 'notice_oeufs' )
            ,( 'poireaux' , 'photo_poireaux', 3, 'notice_poireaux')
            ,( 'patate' , 'photo_patate', 6, 'notice_patate')
            ,('sel' , 'photo_sel', 6, 'notice_sel' )
            , ('carotte' , 'photo_carotte', 1, 'notice_carotte')       
        ]
        db_cursor.executemany(query_materiel, data_materiel)
        print(f"  -> {len(data_materiel)} modèles (Materiel) ajoutés.")
        
        # 4. Exemplaire (Instances spécifiques)
        query_exemplaire = "INSERT INTO Exemplaire (id_exemplaire, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel, lieu_rangement) VALUES (%s, %s, %s, %s, %s, %s)"
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
            (10011, '01_01_2026' , '01_09_2025' , 'garage', 'oeufs', 'frigo'),
            (10012, '01_01_2026', '01_09_2025', 'garage', 'oeufs', 'frigo'),
            (10013, '01_01_2026', '01_09_2025', 'garage', 'oeufs', 'frigo'),
            (10014, '01_01_2026' , '01_09_2025' , 'garage', 'oeufs', 'frigo')
        ]
        db_cursor.executemany(query_exemplaire, data_exemplaire)
        print(f"  -> {len(data_exemplaire)} instances (Exemplaire) ajoutées.")

        # 5. Kit
        query_kit = "INSERT INTO Kit (nom_kit) VALUES (%s)"
        data_kit = [('tiramisu',), ('mousse_au_chocolat',), ('soupe',)]
        db_cursor.executemany(query_kit, data_kit)
        print(f"  -> {len(data_kit)} kits ajoutés.")

        # 6. Kit_Materiel (Lien)
        query_kit_mat = "INSERT INTO Kit_Materiel (nom_kit, nom_materiel) VALUES (%s, %s)"
        data_kit_mat = [
            ('tiramisu', 'mascarpone'),
            ('tiramisu', 'oeufs'),
            ('tiramisu', 'sucre'),
            ('tiramisu', 'cafe'),
            ('tiramisu', 'boudoirs'),
            ('mousse_au_chocolat','oeufs'),
            ('mousse_au_chocolat', 'chocolat'),
            ('soupe' , 'poireaux'),
            ('soupe' , 'patate'),
            ('soupe' , 'sel' ),
            ('soupe' , 'carotte')
        ]
        db_cursor.executemany(query_kit_mat, data_kit_mat)
        print(f"  -> {len(data_kit_mat)} liens kit-Exemplaire ajoutés.")

        # 7. Reservation
        query_res = "INSERT INTO Reservation (date_reservation, date_fin_reservation, id_personnel, id_exemplaire) VALUES (%s, %s, %s, %s)"
        data_res = [
            ('01_12_2025', '07_12_2025', 164, 10001) 
        ]
        db_cursor.executemany(query_res, data_res)
        print(f"  -> {len(data_res)} réservations ajoutées.")

        # 8. Emprunt
        query_emp = "INSERT INTO Emprunt (motif, date_emprunt, id_exemplaire, id_personnel) VALUES (%s, %s, %s, %s)"
        data_emp = [
            ("J'invite des amis", '05_12_2025', 10002, 94165) 
        ]
        db_cursor.executemany(query_emp, data_emp)
        print(f"  -> {len(data_emp)} emprunts ajoutés.")

        # Valider toutes les insertions
        db_connection.commit()
        print("\nDonnées initiales ajoutées et validées (commit).")

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout des données initiales : {err}")
        db_connection.rollback()
        print("Annulation des modifications (rollback).")


    print("\nBase de données et tables créées avec succès.")


except mysql.connector.Error as e:
     print(f"Erreur MySQL : {e}")
finally:
     if 'db_connection' in locals() and db_connection.is_connected():
          db_cursor.close()
          db_connection.close()
          print("Connexion MySQL fermée")

    
