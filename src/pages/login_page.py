import customtkinter as ctk
from components.bandeau_sup import Band_sup
from utils.session import set_session
from database.queries import get_user_by_id

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.pack(fill="both", expand=True)
        
        # Ajout du bandeau supérieur
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Titre de la page
        self.label = ctk.CTkLabel(self, text="Connexion à la base de données ELF", font=("Helvetica", 24, "bold"))
        self.label.pack(pady=40)

        # Identifiant
        self.username_label = ctk.CTkLabel(self, text="Scanner votre carte ou entrer votre identifiant ENSAM: ", font=("Helvetica", 16))
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self, width=300, font=("Helvetica", 16))
        self.username_entry.pack(pady=10)

        # Fonction pour gérer l'appui sur la touche "Entrée"
        self.username_entry.bind("<Return>", self.login)

        # Bouton de connexion (aucune validation pour l'instant)
        self.login_button = ctk.CTkButton(self, text="Se connecter", font=("Helvetica", 16), command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = ctk.CTkButton(self, text="Inscription", font=("Helvetica", 16), command=lambda: controller.show_page("RegisterPage"))
        self.register_button.pack(pady=10)

        # Message d'erreur
        self.error_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14), text_color="red")
        self.error_label.pack(pady=10)

        self.username_entry.focus_set()

    def login(self, manual=False):
        username = self.username_entry.get().strip()
        print(f"Utilisateur '{username}' tente de se connecter.")

        if not username:
            self.error_label.configure(text="Veuillez entrer un identifiant valide.")
            return
        
        user = get_user_by_id(username)
        if user is None:
            self.error_label.configure(text="Identifiant inconnu. Veuillez vous inscrire.")
            return
        
        print(f"Utilisateur '{username}' connecté avec succès.")
        set_session(user)
        self.controller.show_page("MainPage")
