
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
    _current_cart.append(product)
    print(f"Added {_current_cart[-1]} to cart")

def get_cart():
    global _current_cart
    return _current_cart

def remove_from_cart(product):
    global _current_cart
    for i in range(len(_current_cart)):
        if _current_cart[i] == product:
            _current_cart.pop(i)
            return
    print(f"Product not in panier")
    