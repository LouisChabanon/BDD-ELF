

# Simple session management

_current_user = None

def set_session(user):
    global _current_user
    _current_user = user
    print(f"Session démarrée pour l'utilisateur : {_current_user['id_personnel']}")

def get_session():
    global _current_user
    return _current_user

def clear_session():
    global _current_user
    _current_user = None