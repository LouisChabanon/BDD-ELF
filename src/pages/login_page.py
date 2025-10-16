import customtkinter as ctk
from components.bandeau_sup import Band_sup

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Ajout du bandeau supérieur
        self.bandeau = Band_sup(self, controller, username="Alain Etienne")
        self.bandeau.pack(fill="x", side="top")

        # Titre de la page
        self.label = ctk.CTkLabel(self, text="Connexion à la base de données ELF", font=("Helvetica", 24, "bold"))
        self.label.pack(pady=40)

        # Identifiant
        self.username_label = ctk.CTkLabel(self, text="Identifiant :", font=("Helvetica", 16))
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self, width=300, font=("Helvetica", 16))
        self.username_entry.pack(pady=10)

        # Bouton de connexion (aucune validation pour l'instant)
        self.login_button = ctk.CTkButton(self, text="Se connecter", font=("Helvetica", 16), command=self.login)
        self.login_button.pack(pady=20)

        # Message d'erreur
        self.error_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14), text_color="red")
        self.error_label.pack(pady=10)

        

    def login(self):
        username = self.username_entry.get().strip()

        print(f"Utilisateur '{username}' tente de se connecter.")
        self.controller.show_page("MainPage")