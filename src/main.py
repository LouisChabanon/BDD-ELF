import customtkinter as ctk
from app_controller import AppController
from database.connection import init_db

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("src/assets/theme.json")
    
    try:
        init_db()
        print("Connexion à la base de données réussie.")
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        exit(1)


    app = AppController()
    app.mainloop()