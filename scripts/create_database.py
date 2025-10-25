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
          motif TEXT,
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
          date_fin_reservation TEXT,
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
    
	# -----------------------------------------------------
    # --- AJOUT DES DONNÉES INITIALES (SEEDING) ---
    # -----------------------------------------------------
    print("Ajout des données initiales (seeding)...")
    
    try:
        # 1. Personnel
        query_personnel = "INSERT INTO Personnel (id_personnel, mail, type_personnel, nom, prenom) VALUES (%s, %s, %s, %s, %s)"
        data_personnel = [
            (12345, 'test.user@ensam.eu', 'doctorant', 'User', 'Test'),
            (1001, 'admin.elf@ensam.eu', 'admin', 'Admin', 'Super'),
            (2001, 'jean.dupont@ensam.eu', 'etudiant', 'Dupont', 'Jean')
        ]
        db_cursor.executemany(query_personnel, data_personnel)
        print(f"  -> {len(data_personnel)} utilisateurs ajoutés.")

        # 2. Rangement
        query_rangement = "INSERT INTO Rangement (lieu_rangement) VALUES (%s)"
        data_rangement = [
            ('Armoire A, Etagere 1',),
            ('Salle B, Rack 2',),
            ('Reserve Labo',)
        ]
        db_cursor.executemany(query_rangement, data_rangement)
        print(f"  -> {len(data_rangement)} lieux de rangement ajoutés.")

        # 3. Matos (Modèles de matériel)
        query_matos = "INSERT INTO Matos (nom_materiel, photo_materiel, frequence_entretient, notice_materiel) VALUES (%s, %s, %s, %s)"
        data_matos = [
            ('Oscilloscope T-1000', 'src/assets/images/oscillo.png', 'Tous les 6 mois', 'src/assets/notices/oscillo_t1000.pdf'),
            ('Multimetre DMM-300', 'src/assets/images/multimetre.png', 'Tous les 12 mois', 'src/assets/notices/dmm_300.pdf'),
            ('Alimentation Labo PS-50', 'src/assets/images/alim.png', 'N/A', 'src/assets/notices/ps_50.pdf')
        ]
        db_cursor.executemany(query_matos, data_matos)
        print(f"  -> {len(data_matos)} modèles (Matos) ajoutés.")
        
        # 4. Materiel (Instances spécifiques)
        query_materiel = "INSERT INTO Materiel (id_materiel, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel, lieu_rangement) VALUES (%s, %s, %s, %s, %s, %s)"
        data_materiel = [
            (100001, '2025-01-01', '2025-07-01', 'Labo Principal', 'Oscilloscope T-1000', 'Armoire A, Etagere 1'),
            (100002, '2025-01-01', '2025-07-01', 'Labo Principal', 'Oscilloscope T-1000', 'Armoire A, Etagere 1'),
            (200001, '2024-06-01', '2025-06-01', 'Labo Principal', 'Multimetre DMM-300', 'Salle B, Rack 2'),
            (300001, '2023-01-01', 'N/A', 'Labo Principal', 'Alimentation Labo PS-50', 'Salle B, Rack 2')
        ]
        db_cursor.executemany(query_materiel, data_materiel)
        print(f"  -> {len(data_materiel)} instances (Materiel) ajoutées.")

        # 5. Kit
        query_kit = "INSERT INTO Kit (nom_kit) VALUES (%s)"
        data_kit = [('Kit Electronique Base',)]
        db_cursor.executemany(query_kit, data_kit)
        print(f"  -> {len(data_kit)} kits ajoutés.")

        # 6. Kit_Materiel (Lien)
        query_kit_mat = "INSERT INTO Kit_Materiel (nom_kit, id_materiel) VALUES (%s, %s)"
        data_kit_mat = [
            ('Kit Electronique Base', 200001), # Multimetre
            ('Kit Electronique Base', 300001)  # Alimentation
        ]
        db_cursor.executemany(query_kit_mat, data_kit_mat)
        print(f"  -> {len(data_kit_mat)} liens kit-materiel ajoutés.")

        # 7. Reservation
        query_res = "INSERT INTO Reservation (date_reservation, date_fin_reservation, id_personnel, id_materiel) VALUES (%s, %s, %s, %s)"
        data_res = [
            ('2025-10-26', '2025-10-27', 2001, 100001) # Jean Dupont réserve l'Oscillo 1
        ]
        db_cursor.executemany(query_res, data_res)
        print(f"  -> {len(data_res)} réservations ajoutées.")

        # 8. Emprunt
        query_emp = "INSERT INTO Emprunt (motif, date_emprunt, id_materiel, id_personnel) VALUES (%s, %s, %s, %s)"
        data_emp = [
            ('TP Electronique', '2025-10-20', 100002, 12345) # Test User a emprunté l'Oscillo 2
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

    
