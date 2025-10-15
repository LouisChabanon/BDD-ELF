from .connection import get_db

def get_all_products():
    cursor = get_db().cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()

