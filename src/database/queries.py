from database.connection import get_db

def get_all_products():
    cursor = get_db().cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()

def get_all_users():
    cursor = get_db().cursor(dictionary=True)
    cursor.execute("SELECT id_personnel, mail FROM Personnel")
    return cursor.fetchall()

def get_user_by_id(user_id: str):
    cursor = get_db().cursor(dictionary=True)
    query = "SELECT * FROM Personnel WHERE Personnel.id_personnel = '%s'" % str(user_id)
    cursor.execute(query)
    return cursor.fetchone()

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

    cursor = get_db().cursor()
    query = "INSERT INTO Personnel (id_personnel, mail, type_personnel, nom, prenom) VALUES ('%s', '%s', '%s', '%s', '%s')" % (id_personnel, mail, type_personnel, nom, prenom)
    cursor.execute(query)
    get_db().commit()
    
def add_material(id_materiel, date_garantie, date_dernier_entretient, derniere_localisation):
    
    #verifier le format des données avant insertion
    if not isinstance(id_materiel, int):
        raise ValueError("id_materiel doit être un entier.")
    if not isinstance(date_garantie, str):
        raise ValueError("date_garantie doit être une chaine de caractères.")
    if not isinstance(date_dernier_entretient, str):
        raise ValueError("date_dernier_entretient doit être une chaine de caractères.")
    if not isinstance(derniere_localisation, str):
        raise ValueError("dernière_localisation doit être une chaîne de caractères.")

    cursor = get_db().cursor()
    query = "INSERT INTO Materiel (id_materiel, date_garantie, date_dernier_entretient, derniere_localisation) VALUES ('%s', '%s', '%s', '%s')" % (id_materiel, date_garantie, date_dernier_entretient, derniere_localisation)
    
def add_matos(nom_materiel, photo_materiel, frequence_entretient):
    
    #verifier le format des données avant insertion
    if not isinstance(nom_materiel, str):
        raise ValueError("nom_materiel doit être une chaine de caractères.")
    if not isinstance(photo_materiel, str):
        raise ValueError("photo_materiel doit être une chaine de caractères.")
    if not isinstance(frequence_entretient, str):
        raise ValueError("frequence_entretient doit être une chaine de caractères.")


    cursor = get_db().cursor()
    query = "INSERT INTO Matos (nom_materiel, photo_materiel, frequence_entretient) VALUES ('%s', '%s', '%s')" % (nom_materiel, photo_materiel, frequence_entretient)