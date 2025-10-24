import customtkinter as ctk
from components.bandeau_sup import Band_sup
from utils.session import get_session, clear_session

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.pack(fill="both", expand=True)
        
        # Couleur de fond principale
        self.configure(fg_color="#F9F7F0")

        # Ajout du bandeau supérieur
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")
        
        # Titre de la page principale
        self.label = ctk.CTkLabel(self, text="Bienvenue dans la base de données ELF", font=("Helvetica", 24, "bold"),text_color="#4A4947")
        self.label.pack(pady=40)

        # Bouton de déconnexion
        self.logout_button = ctk.CTkButton(self, text="Se déconnecter", font=("Helvetica", 16), command=self.logout)
        self.logout_button.pack(pady=20)

        self.refresh()

        
    def refresh(self):
        # Vérifier la session utilisateur
        if get_session() is None:
            print("Aucun utilisateur connecté, redirection vers la page de connexion.")
            self.controller.show_page("LoginPage")

        self.bandeau.refresh()


    def logout(self):
        print("Utilisateur se déconnecte.")
        clear_session()
        self.controller.show_page("LoginPage")