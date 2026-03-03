import customtkinter as ctk
from components.bandeau_sup import Band_sup
from utils.session import set_session
from database.queries import get_user_by_id


class SeeLoanPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Couleur de fond principale
        self.configure(fg_color="#F9F7F0")

        # Ajout du bandeau supérieur (commun à toutes les pages)
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")
        self.bandeau.refresh()

        # Conteneur principal pour le contenu
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True)
