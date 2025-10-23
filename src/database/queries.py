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
    cursor.execute(query)
    get_db().commit()

    
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
    cursor.execute(query)
    get_db().commit()
 
    
def add_loan(id_emprunt, motif, date_emprunt):
    
    #verifier le format des données avant insertion
    if not isinstance(id_emprunt, int):
        raise ValueError("id_emprunt doit être un entier.")
    if not isinstance(motif, str):
        raise ValueError("motif doit être une chaine de caractères.")
    if not isinstance(date_emprunt, str):
        raise ValueError("date_emprunt doit être une chaine de caractères.")

    cursor = get_db().cursor()
    query = "INSERT INTO Emprunt (id_emprunt, motif, date_emprunt) VALUES ('%s', '%s', '%s')" % (id_emprunt, motif, date_emprunt)
    cursor.execute(query)
    get_db().commit()

    
def add_instructions(notice_materiel):
    
    #verifier le format des données avant insertion
    if not isinstance(notice_materiel, str):
        raise ValueError("notice_materiel doit être une chaine de caractère.")

    cursor = get_db().cursor()
    query = "INSERT INTO Notice (notice_materiel) VALUES ('%s')" % (notice_materiel)
    cursor.execute(query)
    get_db().commit()
 
    
def add_storage(lieu_rangement):
    
    #verifier le format des données avant insertion
    if not isinstance(lieu_rangement, str):
        raise ValueError("lieu_rangement doit être une chaine de caractère.")

    cursor = get_db().cursor()
    query = "INSERT INTO Rangement (lieu_rangement) VALUES ('%s')" % (lieu_rangement)
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
  
    
def add_history(date_rendue):
    
    #verifier le format des données avant insertion
    if not isinstance(date_rendue, str):
        raise ValueError("date_rendue doit être une chaine de caractère.")

    cursor = get_db().cursor()
    query = "INSERT INTO Historique (date_rendue) VALUES ('%s')" % (date_rendue)
    cursor.execute(query)
    get_db().commit()
    
    
def add_reservation(date_reservation):
    
    #verifier le format des données avant insertion
    if not isinstance(date_reservation, str):
        raise ValueError("date_reservation doit être une chaine de caractère.")

    cursor = get_db().cursor()
    query = "INSERT INTO Reservation (date_reservation) VALUES ('%s')" % (date_reservation)
    cursor.execute(query)
    get_db().commit()