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
            m.id_exemplaire, m.derniere_localisation, m.nom_materiel, m.lieu_rangement, t.photo_materiel
        FROM
            Exemplaire m
        JOIN
            Materiel t ON m.nom_materiel = t.nom_materiel
    """
    return execute_query(query, fetch_all=True, dictionary_cursor=True)


def get_product_by_name(nom_produit: int):
    query = """
        SELECT
            m.nom_materiel, m.photo_materiel, m.frequence_entretient, m.notice_materiel
        FROM
            Materiel m
        WHERE
            m.nom_materiel = %s
    """
    params = (nom_produit,)
    return execute_query(query, params, fetch_all=True, dictionary_cursor=True)


def get_exemplaires_by_product_id(produit_id: int):
    query = """
        SELECT
            m.id_exemplaire, m.date_garantie, m.date_dernier_entretient, m.derniere_localisation, m.nom_materiel, m.lieu_rangement, t.photo_materiel, t.frequence_entretient, t.notice_materiel
        FROM 
            Exemplaire m
        JOIN
            Materiel t ON m.nom_materiel = t.nom_materiel
        WHERE
            m.id_exemplaire = %s
    """
    params = (produit_id,)
    return execute_query(query, params, fetch_one=True, dictionary_cursor=True)


def get_exemplaire_history(id: int):
    query = """
    SELECT
        e.id_emprunt, e.motif, e.date_emprunt, e.date_rendu
    FROM
        Emprunt e
    JOIN
        Personnel p ON e.#id_personnel = p.id_personnel
    JOIN
        Materiel t ON m.#nom_materiel = t.nom_materiel 
    WHERE e.id_exemplaire = %s
    ORDER BY
        e.date_rendu DESC
    """
    params = (id,)
    return execute_query(query, params, fetch_all=True, dictionary_cursor=True)


def update_username(id_personnel: int, new_id: int):
    if not isinstance(new_id, int):
        raise ValueError("new_id doit être un entier")
    if not isinstance(id_personnel, int):
        raise ValueError("id_personnel doit être un entier")
    
    if get_user_by_id(new_id):
        print("Erreur : un utilisateur ayant cet identifiant existe déjà")
        return
    else:
        query = "UPDATE Personnel SET Personnel.id_personnel = %s WHERE Personnel.id_personnel = %s"
        params = (new_id, id_personnel)
        return execute_query(query, params, is_commit=True)
    
def update_email(id_personnel: int, new_mail: str):
    if not isinstance(new_mail, str):
        raise ValueError("new_id doit être un entier")
    if not isinstance(id_personnel, int):
        raise ValueError("id_personnel doit être un entier")
    
    if get_user_by_email(new_mail):
        print("Erreur : un utilisateur ayant cet email existe déjà")
        return
    else:
        query = "UPDATE Personnel SET Personnel.mail = %s WHERE Personnel.id_personnel = %s"
        params = (new_mail, id_personnel)
        return execute_query(query, params, is_commit=True)




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
    return execute_query(query, params, is_commit=True)
    

    
def add_material(id_exemplaire, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel):
    
    #verifier le format des données avant insertion
    if not isinstance(id_exemplaire, int):
        raise ValueError("id_exemplaire doit être un entier.")
    if not isinstance(date_garantie, str):
        raise ValueError("date_garantie doit être une chaine de caractères.")
    if not isinstance(date_dernier_entretient, str):
        raise ValueError("date_dernier_entretient doit être une chaine de caractères.")
    if not isinstance(derniere_localisation, str):
        raise ValueError("dernière_localisation doit être une chaîne de caractères.")
    if not isinstance(nom_materiel, str):
        raise ValueError("nom_materiel doit être une chaîne de caractères.")

    query = "INSERT INTO Exemplaire (id_exemplaire, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel) VALUES ('%s', '%s', '%s', '%s', '%s')"
    params = (id_exemplaire, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel)
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
   
    query = "INSERT INTO Materiel (nom_materiel, photo_materiel, frequence_entretient, nom_materiel) VALUES ('%s', '%s', '%s', '%s')"
    params = (nom_materiel, photo_materiel, frequence_entretient, notice_materiel)
    return execute_query(query, params, is_commit=True)
 
    
def add_loan(id_emprunt, motif, date_emprunt, id_exemplaire, id_personnel):
    
    #verifier le format des données avant insertion
    if not isinstance(id_emprunt, int):
        raise ValueError("id_emprunt doit être un entier.")
    if not isinstance(motif, str):
        raise ValueError("motif doit être une chaine de caractères.")
    if not isinstance(date_emprunt, str):
        raise ValueError("date_emprunt doit être une chaine de caractères.")
    if not isinstance(id_exemplaire, int):
        raise ValueError("id_exemplaire doit être un entier.")
    if not isinstance(id_personnel, int):
        raise ValueError("id_personnel doit être un entier.")

    query = "INSERT INTO Emprunt (id_emprunt, motif, date_emprunt, id_exemplaire, id_personnel) VALUES ('%s', '%s', '%s','%s', '%s')"
    params = (id_emprunt, motif, date_emprunt, id_exemplaire, id_personnel)
    return execute_query(query, params, is_commit=True)

    
def add_instructions(notice_materiel):
    
    #verifier le format des données avant insertion
    if not isinstance(notice_materiel, str):
        raise ValueError("notice_materiel doit être une chaine de caractère.")

    query = "INSERT INTO Notice (notice_materiel) VALUES ('%s')"
    params =  (notice_materiel,)
    return execute_query(query, params, is_commit=True)
 
    
def add_storage(id_exemplaire, lieu_rangement):
    
    #verifier le format des données avant insertion
    if not isinstance(id_exemplaire, int):
        raise ValueError("id_exemplaire doit être un entier.")
    if not isinstance(lieu_rangement, str):
        raise ValueError("lieu_rangement doit être une chaine de caractère.")

    cursor = get_db().cursor()
    query = "INSERT INTO Rangement (id_exemplaire, lieu_rangement) VALUES ('%s', '%s')" % (id_exemplaire, lieu_rangement)
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
    
def add_history(date_rendue, id_exemplaire, id_personnel):
    
    #verifier le format des données avant insertion
    if not isinstance(date_rendue, str):
        raise ValueError("date_rendue doit être une chaine de caractère.")
    if not isinstance(id_exemplaire, int):
        raise ValueError("id_exemplaire doit être un entier.")
    if not isinstance(id_personnel, int):
        raise ValueError("id_personnel doit être un entier.")

    cursor = get_db().cursor()
    query = "INSERT INTO Historique (date_rendue, id_exemplaire, id_personnel) VALUES ('%s', '%s', '%s'')" % (date_rendue, id_exemplaire, id_personnel)
    cursor.execute(query)
    get_db().commit()
    
    
def add_reservation(date_reservation, id_personnel, id_exemplaire):
    
    #verifier le format des données avant insertion
    if not isinstance(date_reservation, str):
        raise ValueError("date_reservation doit être une chaine de caractère.")
    if not isinstance(id_personnel, int):
        raise ValueError("id_personnel doit être un entier.")
    if not isinstance(id_exemplaire, int):
        raise ValueError("id_exemplaire doit être un entier.")
    
    cursor = get_db().cursor()
    query = "INSERT INTO Reservation (date_reservation, id_personnel, id_exemplaire) VALUES ('%s', '%s', '%s'')" % (date_reservation, id_personnel, id_exemplaire)
    cursor.execute(query)
    get_db().commit()

def update_materiel(product_name: str, data: dict):
    """
    Met à jour les informations d'un produit dans les tables Materiel et Matos.
    data peut contenir :
        - frequence_entretient
        - date_dernier_entretient
        - notice_materiel (PDF)
    """

    if not isinstance(product_name, str):
        raise ValueError("product_name doit être une chaine de caractére.")

    # Récupérer les valeurs
    frequence_entretient = data.get("frequence_entretient")
    date_dernier_entretient = data.get("date_dernier_entretient")
    notice_materiel = data.get("pdf_path")  # correspond au champ PDF
    photo_materiel = data.get("photo_materiel")

    # --- Mise à jour table Materiel ---
    query_materiel = """
        UPDATE Materiel
        SET date_dernier_entretient = %s, notice_materiel = %s, photo_materiel = %s
        WHERE nom_materiel = %s
    """
    params_materiel = (date_dernier_entretient, notice_materiel, photo_materiel, product_name)
    execute_query(query_materiel, params_materiel, is_commit=True)


    
def delete_emprunt(id_materiel, id_personnel):
    query = """
            DELETE FROM Emprunt
            WHERE id_materiel = %s AND id_personnel = %s
            """
    params = (id_materiel, id_personnel)
    execute_query(query, params, is_commit=True)