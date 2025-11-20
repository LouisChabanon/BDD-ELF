import customtkinter as ctk
from components.bandeau_sup import Band_sup
from utils.session import set_session
from database.queries import get_user_by_id

class ReturnPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.pack(fill="both", expand=True)

        # Couleur de fond principale
        self.configure(fg_color="#F9F7F0")

        # Ajout du bandeau supérieur
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Titre de la page
        self.label = ctk.CTkLabel(self, text="Rendu du matériel", font=("Helvetica", 24, "bold"),text_color="#4A4947")
        self.label.pack(pady=40)

        # Identifiant
        self.username_label = ctk.CTkLabel(self, text="Scannez le code barre du matériel à rendre: ", font=("Helvetica", 16),text_color="#4A4947")
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self, width=300, font=("Helvetica", 16))
        self.username_entry.pack(pady=10)

        # Fonction pour gérer l'appui sur la touche "Entrée"
        self.username_entry.bind("<Return>", self.login)

        # Bouton de rendu (aucune validation pour l'instant)
        self.login_button = ctk.CTkButton(self, text="Rendre", font=("Helvetica", 16), command=self.login)
        self.login_button.pack(pady=20)

        # Message d'erreur
        self.error_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14), text_color="maroon")
        self.error_label.pack(pady=10)

        self.username_entry.focus_set()
