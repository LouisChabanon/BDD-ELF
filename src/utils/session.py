_current_user = None
_current_cart = []

def set_session(user):
    global _current_user
    _current_user = user
    print(f"Session démarrée pour l'utilisateur : {_current_user['id_personnel']}")

def get_session():
    global _current_user
    return _current_user

def clear_session():
    global _current_user
    global _current_cart
    _current_user = None
    _current_cart = []

def add_to_cart(product):
    global _current_cart
    if not any(p['id_exemplaire'] == product['id_exemplaire'] for p in _current_cart):
        _current_cart.append(product)
        print(f"Added {product.get('nom_materiel')} to cart")
    else:
        print("Item already in cart")

def get_cart():
    global _current_cart
    return _current_cart

def remove_from_cart(product):
    global _current_cart
    if product in _current_cart:
        _current_cart.remove(product)
    else:
        print("Product not in panier")