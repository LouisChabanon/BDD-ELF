from database.connection import get_db
import mysql.connector


def execute_query(query, params=None, fetch_one=False, fetch_all=False, is_commit=False, dictionary_cursor=False):
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
        print(f"Erreur SQL : {err}\nQuery: {query}\nParams: {params}")
        if is_commit:
            connection.rollback()
        return None
    finally:
        cursor.close()

def get_all_materiels_with_stock():
    query = """
        SELECT 
            m.nom_materiel, 
            m.photo_materiel, 
            m.frequence_entretient, 
            m.notice_materiel,
            
            -- Calculate Total Copies
            COUNT(e.id_exemplaire) as total_copies,
            
            -- Calculate Unavailable Copies (Currently in Emprunt with no return date)
            (
                SELECT COUNT(*)
                FROM Emprunt emp
                JOIN Exemplaire ex_emp ON emp.id_exemplaire = ex_emp.id_exemplaire
                WHERE ex_emp.nom_materiel = m.nom_materiel
                AND (emp.date_rendu IS NULL OR emp.date_rendu = '')
            ) as borrowed_count
            
        FROM Materiel m
        LEFT JOIN Exemplaire e ON m.nom_materiel = e.nom_materiel
        GROUP BY m.nom_materiel, m.photo_materiel, m.frequence_entretient, m.notice_materiel
    """
    
    results = execute_query(query, fetch_all=True, dictionary_cursor=True)
    
    # Post-process to calculate simple 'stock_dispo' for the UI
    if results:
        for row in results:
            total = row['total_copies']
            borrowed = row['borrowed_count']
            row['stock_dispo'] = total - borrowed
            
    return results


def get_user_by_id(user_id: str):
    query = "SELECT * FROM Personnel WHERE Personnel.id_personnel = %s"
    params = (user_id,)
    return execute_query(query, params, fetch_one=True, dictionary_cursor=True)

def get_all_users():
    query = "SELECT id_personnel, mail FROM Personnel"
    return execute_query(query, fetch_all=True, dictionary_cursor=True)

def get_all_materiels():
    query = """
        SELECT
            nom_materiel,
            photo_materiel,
            frequence_entretient,
            notice_materiel
        FROM
            Materiel
    """
    return execute_query(query, fetch_all=True, dictionary_cursor=True)

def get_product_by_name(nom_produit: str):
    query = """
        SELECT 
            m.nom_materiel, m.photo_materiel, m.frequence_entretient, m.notice_materiel
        FROM 
            Materiel m
        WHERE 
            m.nom_materiel = %s
    """
    params = (nom_produit,)
    return execute_query(query, params, fetch_one=True, dictionary_cursor=True) # Changed to fetch_one

def get_exemplaires_by_product_id(produit_id: int):
    """Récupère un exemplaire spécifique par son ID unique."""
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
        e.id_emprunt, e.motif, e.date_emprunt, 'En cours' as date_rendu, p.nom, p.prenom
    FROM 
        Emprunt e
    JOIN 
        Personnel p ON e.id_personnel = p.id_personnel
    JOIN 
        Exemplaire ex ON e.id_exemplaire = ex.id_exemplaire
    WHERE e.id_exemplaire = %s
    ORDER BY 
        e.date_emprunt DESC
    """
    params = (id,)
    return execute_query(query, params, fetch_all=True, dictionary_cursor=True)

def get_product_details(nom_materiel):
    """Get generic info for the top of the Product Page."""
    query = "SELECT * FROM Materiel WHERE nom_materiel = %s"
    return execute_query(query, (nom_materiel,), fetch_one=True, dictionary_cursor=True)

def get_product_name_by_exemplaire_id(exemplaire_id):
    """
    Finds the generic product name associated with a specific ID.
    Used when a user scans a barcode to find the product page.
    """
    query = "SELECT nom_materiel FROM Exemplaire WHERE id_exemplaire = %s"
    result = execute_query(query, (exemplaire_id,), fetch_one=True, dictionary_cursor=True)
    if result:
        return result['nom_materiel']
    return None

def get_exemplaire_availability(exemplaire_id: int):
    """
    Check availability based on the LATEST loan.
    Returns True if available, False if currently borrowed.
    """
    # 1. Query the database for the most recent loan of this specific item
    query = """
        SELECT date_rendu 
        FROM Emprunt 
        WHERE id_exemplaire = %s 
        ORDER BY id_emprunt DESC 
        LIMIT 1
    """
    params = (exemplaire_id,)
    last_loan = execute_query(query, params, fetch_one=True, dictionary_cursor=True)

    # 2. Logic Evaluation
    
    # Case A: The item has never been borrowed before.
    if last_loan is None:
        return True
        
    date_rendu = last_loan.get('date_rendu')
    
    # Case B: The item was borrowed, and 'date_rendu' is empty/None.
    # This means the item is currently OUT.
    if date_rendu is None or str(date_rendu).strip() == "":
        return False 
        
    # Case C: The item was borrowed, but has a 'date_rendu'.
    # This means it was returned.
    return True

def get_product_availability_count(nom_materiel):
    """
    Returns the number of available copies for a generic product.
    Used to Enable/Disable the Rent button on the main page.
    """
    # Get all IDs for this product
    query = "SELECT id_exemplaire FROM Exemplaire WHERE nom_materiel = %s"
    exemplaires = execute_query(query, (nom_materiel,), fetch_all=True, dictionary_cursor=True)
    
    available_count = 0
    for ex in exemplaires:
        # Reuse the availability logic (check latest date_rendu)
        if get_exemplaire_availability(ex['id_exemplaire']):
            available_count += 1
            
    return available_count

def validate_scan_match(scanned_id, required_product_name):
    """
    Verifies:
    1. Does this ID exist?
    2. Is it the correct product type (e.g., scanned a Drill ID while on Drill card)?
    3. Is it available?
    """
    # 1. Get details of scanned ID
    query = "SELECT nom_materiel FROM Exemplaire WHERE id_exemplaire = %s"
    result = execute_query(query, (scanned_id,), fetch_one=True, dictionary_cursor=True)
    
    if not result:
        return False, "Code barre inconnu."
    
    # 2. Check Type Match
    if result['nom_materiel'] != required_product_name:
        return False, f"Ce code correspond à : {result['nom_materiel']}"
    
    # 3. Check Availability
    if not get_exemplaire_availability(scanned_id):
        return False, "Cet exemplaire est déjà emprunté."
        
    return True, "OK"

def get_exemplaires_with_status(nom_materiel):
    """
    Returns all copies (exemplaires) of a specific product.
    Includes a subquery or join logic to determine if it is currently borrowed.
    """

    query = """
        SELECT 
            e.id_exemplaire, 
            e.lieu_rangement, 
            e.date_dernier_entretient,
            (
                SELECT date_rendu 
                FROM Emprunt emp 
                WHERE emp.id_exemplaire = e.id_exemplaire 
                ORDER BY id_emprunt DESC 
                LIMIT 1
            ) as last_return_date,
            (
                SELECT count(*) 
                FROM Emprunt emp2 
                WHERE emp2.id_exemplaire = e.id_exemplaire
            ) as total_loans
        FROM Exemplaire e
        WHERE e.nom_materiel = %s
    """
    items = execute_query(query, (nom_materiel,), fetch_all=True, dictionary_cursor=True)
    if not items: return None
    # Post-process status in Python for clarity
    results = []
    for item in items:
        is_available = True
        if item['total_loans'] > 0:
            d_rendu = item.get('last_return_date')
            if not d_rendu or str(d_rendu).strip() == "":
                is_available = False
        
        item['is_available'] = is_available
        results.append(item)
        
    return results

def update_username(id_personnel: int, new_id: int):
    query = "UPDATE Personnel SET Personnel.id_personnel = %s WHERE Personnel.id_personnel = %s"
    params = (new_id, id_personnel)
    return execute_query(query, params, is_commit=True)
    
def update_email(id_personnel: int, new_mail: str):
    query = "UPDATE Personnel SET Personnel.mail = %s WHERE Personnel.id_personnel = %s"
    params = (new_mail, id_personnel)
    return execute_query(query, params, is_commit=True)

def add_user(id_personnel, mail, type_personnel, nom, prenom):    
    query = "INSERT INTO Personnel (id_personnel, mail, type_personnel, nom, prenom) VALUES (%s, %s, %s, %s, %s)"
    params = (id_personnel, mail, type_personnel, nom, prenom)
    return execute_query(query, params, is_commit=True)
    
def add_material(id_exemplaire, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel):
    query = "INSERT INTO Exemplaire (id_exemplaire, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel) VALUES (%s, %s, %s, %s, %s)"
    params = (id_exemplaire, date_garantie, date_dernier_entretient, derniere_localisation, nom_materiel)
    return execute_query(query, params, is_commit=True)
    
def add_matos(nom_materiel, photo_materiel, frequence_entretient, notice_materiel):
    query = "INSERT INTO Materiel (nom_materiel, photo_materiel, frequence_entretient, notice_materiel) VALUES (%s, %s, %s, %s)"
    params = (nom_materiel, photo_materiel, frequence_entretient, notice_materiel)
    return execute_query(query, params, is_commit=True)
 
def add_loan(motif, date_emprunt, id_exemplaire, id_personnel):
    query = "INSERT INTO Emprunt (motif, date_emprunt, id_exemplaire, id_personnel) VALUES (%s, %s, %s, %s)"
    params = (motif, date_emprunt, id_exemplaire, id_personnel)
    return execute_query(query, params, is_commit=True)
    
def add_instructions(notice_materiel):
    query = "INSERT INTO Notice (notice_materiel) VALUES (%s)"
    params =  (notice_materiel,)
    return execute_query(query, params, is_commit=True)
 
def add_storage(lieu_rangement):
    query = "INSERT INTO Rangement (lieu_rangement) VALUES (%s)"
    params = (lieu_rangement,)
    return execute_query(query, params, is_commit=True)
    
def add_kit(nom_kit):
    query = "INSERT INTO Kit (nom_kit) VALUES (%s)"
    params = (nom_kit,)
    return execute_query(query, params, is_commit=True)
  
def add_kit_de_materiel(nom_kit, nom_materiel):
    query = "INSERT INTO Kit_Materiel (nom_kit, nom_materiel) VALUES (%s, %s)"
    params = (nom_kit, nom_materiel)
    return execute_query(query, params, is_commit=True)
    
def add_reservation(date_reservation, id_personnel, id_exemplaire):
    query = "INSERT INTO Reservation (date_reservation, id_personnel, id_exemplaire) VALUES (%s, %s, %s)"
    params = (date_reservation, id_personnel, id_exemplaire)
    return execute_query(query, params, is_commit=True)

def update_materiel(product_name: str, data: dict):
    frequence_entretient = data.get("frequence_entretient")
    date_dernier_entretient = data.get("date_dernier_entretient")
    notice_materiel = data.get("pdf_path")
    photo_materiel = data.get("photo_materiel")

    query_materiel = """
        UPDATE Materiel
        SET frequence_entretient = %s, notice_materiel = %s
        WHERE nom_materiel = %s
    """
    params_materiel = (frequence_entretient, notice_materiel, product_name)
    execute_query(query_materiel, params_materiel, is_commit=True)
    
def delete_emprunt(id_exemplaire, id_personnel):
    query = """
            DELETE FROM Emprunt
            WHERE id_exemplaire = %s AND id_personnel = %s
            """
    params = (id_exemplaire, id_personnel)
    execute_query(query, params, is_commit=True)

def return_product(id_exemplaire):
    query = """
        UPDATE Emprunt
        SET date_rendu = NOW()
        WHERE id_emprunt = (
            SELECT id_emprunt
            FROM (
                SELECT id_emprunt
                FROM Emprunt
                WHERE id_exemplaire = %s
                AND date_rendu IS NULL
                ORDER BY id_emprunt DESC
                LIMIT 1
            ) AS sub
        )
    """
    execute_query(query, (id_exemplaire,), commit=True)




def get_all_rangements():
    """Récupère la liste de tous les lieux de rangement."""
    query = "SELECT lieu_rangement FROM Rangement"
    results = execute_query(query, fetch_all=True, dictionary_cursor=True)
    
    # Retourne une liste simple des noms de rangement, car c'est ce que votre ComboBox semble attendre
    if results:
        return [r['lieu_rangement'] for r in results]
    return []

def materiel_exists(nom_materiel: str):
    """Vérifie si un matériel avec ce nom existe déjà."""
    query = "SELECT COUNT(*) FROM Materiel WHERE nom_materiel = %s"
    params = (nom_materiel,)
    result = execute_query(query, params, fetch_one=True)
    
    # execute_query retourne un tuple pour fetch_one sans dictionary_cursor
    # Nous vérifions si le COUNT est supérieur à 0
    return result is not None and result[0] > 0

def exemplaire_exists(id_exemplaire: int):
    """Vérifie si un exemplaire avec cet ID existe déjà."""
    query = "SELECT COUNT(*) FROM Exemplaire WHERE id_exemplaire = %s"
    params = (id_exemplaire,)
    result = execute_query(query, params, fetch_one=True)
    
    # execute_query retourne un tuple pour fetch_one sans dictionary_cursor
    # Nous vérifions si le COUNT est supérieur à 0
    return result is not None and result[0] > 0