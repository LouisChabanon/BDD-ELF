import customtkinter as ctk
from components.bandeau_sup import Band_sup

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.pack(fill="both", expand=True)
        
        # Ajout du bandeau supérieur
        self.bandeau = Band_sup(self, controller, username="Alain Etienne")
        self.bandeau.pack(fill="x", side="top")
        
        # Titre de la page principale
        self.label = ctk.CTkLabel(self, text="Bienvenue dans la base de données ELF", font=("Helvetica", 24, "bold"))
        self.label.pack(pady=40)

        # Bouton de déconnexion
        self.logout_button = ctk.CTkButton(self, text="Se déconnecter", font=("Helvetica", 16), command=self.logout)
        self.logout_button.pack(pady=20)

        


    def logout(self):
        print("Utilisateur se déconnecte.")
        self.controller.show_page("LoginPage")