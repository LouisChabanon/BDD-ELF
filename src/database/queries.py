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