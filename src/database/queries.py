from database.connection import get_db
import mysql.connector

def execute_query(query, params=None, fetch_one=False, fetch_all=False, is_commit=False, dictionary_cursor=False):
    """
    Exécute une requête de manière sécurisée avec gestion des curseurs.
    """
    connection = get_db()
    if not connection or not connection.is_connected():
        raise Exception("Database is not connected.")
        
    cursor = connection.cursor(dictionary=dictionary_cursor)
    try:
        cursor.execute(query, params)
        
        if is_commit:
            connection.commit()
            return cursor.lastrowid
            
        if fetch_one:
            return cursor.fetchone()
            
        if fetch_all:
            return cursor.fetchall()
            
    except mysql.connector.Error as err:
        print(f"Erreur SQL : {err}")
        if is_commit:
            connection.rollback() # Annuler les changements en cas d'erreur
        return None
    finally:
        cursor.close()

def get_user_by_email(email: str):
    query = "SELECT * FROM Personnel WHERE mail = %s"
    params = (email,)
    return execute_query(query, params, fetch_one=True, dictionary_cursor=True)

def get_user_by_id(user_id: str):
    query = "SELECT * FROM Personnel WHERE Personnel.id_personnel = %s"
    params = (user_id,)
    return execute_query(query, params, fetch_one=True, dictionary_cursor=True)

def get_all_users():
    query = "SELECT id_personnel, mail FROM Personnel"
    return execute_query(query, fetch_all=True, dictionary_cursor=True)

def get_all_products_with_category():
    query = """
        SELECT
            m.id_materiel, m.derniere_localisation, m.nom_materiel, m.lieu_rangement, t.photo_materiel
        FROM
            Materiel m
        JOIN
            Matos t ON m.nom_materiel = t.nom_materiel
    """
    return execute_query(query, fetch_all=True, dictionary_cursor=True)


def get_product_by_id(produit_id: int):
    query = """
        SELECT
            m.id_materiel, m.date_garantie, m.date_dernier_entretient, m.derniere_localisation, m.nom_materiel, m.lieu_rangement, t.photo_materiel, t.frequence_entretient, t.notice_materiel
        FROM 
            Materiel m
        JOIN
            Matos t ON m.nom_materiel = t.nom_materiel
        WHERE
            m.id_materiel = %s
    """
    params = (produit_id,)
    return execute_query(query, params, fetch_one=True, dictionary_cursor=True)



def add_user(id_personnel, mail, type_personnel, nom, prenom):    
    # Verifier le format des données avant insertion
    if not isinstance(id_personnel, int):
        raise ValueError("id_personnel doit être un entier.")
    if not isinstance(mail, str) or "@" not in mail:
        raise ValueError("mail doit être une chaîne de caractères valide.")
    if not isinstance(type_personnel, str):
        raise ValueError("type_personnel doit être une chaîne de caractères.")
    if not isinstance(nom, str):
        raise ValueError("nom doit être une chaîne de caractères.")
    if not isinstance(prenom, str):
        raise ValueError("prenom doit être une chaîne de caractères.")

    query = "INSERT INTO Personnel (id_personnel, mail, type_personnel, nom, prenom) VALUES ('%s', '%s', '%s', '%s', '%s')"
    params = (id_personnel, mail, type_personnel, nom, prenom)
    

    
def add_material(id_materiel, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel):
    
    #verifier le format des données avant insertion
    if not isinstance(id_materiel, int):
        raise ValueError("id_materiel doit être un entier.")
    if not isinstance(date_garantie, str):
        raise ValueError("date_garantie doit être une chaine de caractères.")
    if not isinstance(date_dernier_entretient, str):
        raise ValueError("date_dernier_entretient doit être une chaine de caractères.")
    if not isinstance(derniere_localisation, str):
        raise ValueError("dernière_localisation doit être une chaîne de caractères.")
    if not isinstance(nom_materiel, str):
        raise ValueError("nom_materiel doit être une chaîne de caractères.")

    query = "INSERT INTO Materiel (id_materiel, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel) VALUES ('%s', '%s', '%s', '%s', '%s')"
    params = (id_materiel, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel)
    return execute_query(query, params, is_commit=True)

    
def add_matos(nom_materiel, photo_materiel, frequence_entretient, notice_materiel):
    
    #verifier le format des données avant insertion
    if not isinstance(nom_materiel, str):
        raise ValueError("nom_materiel doit être une chaine de caractères.")
    if not isinstance(photo_materiel, str):
        raise ValueError("photo_materiel doit être une chaine de caractères.")
    if not isinstance(frequence_entretient, str):
        raise ValueError("frequence_entretient doit être une chaine de caractères.")
    if not isinstance(notice_materiel, str):
        raise ValueError("notice_materiel doit être une chaine de caractère.")
   
    query = "INSERT INTO Matos (nom_materiel, photo_materiel, frequence_entretient, nom_materiel) VALUES ('%s', '%s', '%s', '%s')"
    params = (nom_materiel, photo_materiel, frequence_entretient, notice_materiel)
    return execute_query(query, params, is_commit=True)
 
    
def add_loan(id_emprunt, motif, date_emprunt, id_materiel, id_personnel):
    
    #verifier le format des données avant insertion
    if not isinstance(id_emprunt, int):
        raise ValueError("id_emprunt doit être un entier.")
    if not isinstance(motif, str):
        raise ValueError("motif doit être une chaine de caractères.")
    if not isinstance(date_emprunt, str):
        raise ValueError("date_emprunt doit être une chaine de caractères.")
    if not isinstance(id_materiel, int):
        raise ValueError("id_materiel doit être un entier.")
    if not isinstance(id_personnel, int):
        raise ValueError("id_personnel doit être un entier.")

    query = "INSERT INTO Emprunt (id_emprunt, motif, date_emprunt, id_materiel, id_personnel) VALUES ('%s', '%s', '%s','%s', '%s')"
    params = (id_emprunt, motif, date_emprunt, id_materiel, id_personnel)
    return execute_query(query, params, is_commit=True)

    
def add_instructions(notice_materiel):
    
    #verifier le format des données avant insertion
    if not isinstance(notice_materiel, str):
        raise ValueError("notice_materiel doit être une chaine de caractère.")

    query = "INSERT INTO Notice (notice_materiel) VALUES ('%s')"
    params =  (notice_materiel,)
    return execute_query(query, params, is_commit=True)
 
    
def add_storage(id_materiel, lieu_rangement):
    
    #verifier le format des données avant insertion
    if not isinstance(id_materiel, int):
        raise ValueError("id_materiel doit être un entier.")
    if not isinstance(lieu_rangement, str):
        raise ValueError("lieu_rangement doit être une chaine de caractère.")

    cursor = get_db().cursor()
    query = "INSERT INTO Rangement (id_materiel, lieu_rangement) VALUES ('%s', '%s')" % (id_materiel, lieu_rangement)
    cursor.execute(query)
    get_db().commit()
    
    
def add_kit(nom_kit):
    
    #verifier le format des données avant insertion
    if not isinstance(nom_kit, str):
        raise ValueError("nom_kit doit être une chaine de caractère.")

    cursor = get_db().cursor()
    query = "INSERT INTO Kit (nom_kit) VALUES ('%s')" % (nom_kit)
    cursor.execute(query)
    get_db().commit()
  
    
def add_kit_de_materiel(nom_kit, nom_materiel):
    
    #verifier le format des données avant insertion
    if not isinstance(nom_kit, str):
        raise ValueError("nom_kit doit être une chaine de caractère.")
    if not isinstance(nom_materiel, str):
        raise ValueError("nom_materiel doit être une chaine de caractères.")

    cursor = get_db().cursor()
    query = "INSERT INTO Kit (nom_kit, nom_materiel) VALUES ('%s', '%s')" % (nom_kit, nom_materiel)
    cursor.execute(query)
    get_db().commit()
    
def add_history(date_rendue, id_materiel, id_personnel):
    
    #verifier le format des données avant insertion
    if not isinstance(date_rendue, str):
        raise ValueError("date_rendue doit être une chaine de caractère.")
    if not isinstance(id_materiel, int):
        raise ValueError("id_materiel doit être un entier.")
    if not isinstance(id_personnel, int):
        raise ValueError("id_personnel doit être un entier.")

    cursor = get_db().cursor()
    query = "INSERT INTO Historique (date_rendue, id_materiel, id_personnel) VALUES ('%s', '%s', '%s'')" % (date_rendue, id_materiel, id_personnel)
    cursor.execute(query)
    get_db().commit()
    
    
def add_reservation(date_reservation, id_personnel, id_materiel):
    
    #verifier le format des données avant insertion
    if not isinstance(date_reservation, str):
        raise ValueError("date_reservation doit être une chaine de caractère.")
    if not isinstance(id_personnel, int):
        raise ValueError("id_personnel doit être un entier.")
    if not isinstance(id_materiel, int):
        raise ValueError("id_materiel doit être un entier.")
    
    cursor = get_db().cursor()
    query = "INSERT INTO Reservation (date_reservation, id_personnel, id_materiel) VALUES ('%s', '%s', '%s'')" % (date_reservation, id_personnel, id_materiel)
    cursor.execute(query)
    get_db().commit()