import customtkinter as ctk
from components.bandeau_sup import Band_sup
from utils.session import set_session
from utils.session import get_session
from database.queries import get_user_by_id
from database.queries import get_booked_items

class ReservationsPage(ctk.CTkFrame):
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
        self.label = ctk.CTkLabel(self, text="Mes réservations", font=("Helvetica", 24, "bold"), text_color="#4A4947")
        self.label.pack(pady=40)

        # Identifiant
        self.username_label = ctk.CTkLabel(self, text="", font=("Helvetica", 16), text_color="#4A4947")
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self, width=300, font=("Helvetica", 16))
        self.username_entry.pack(pady=10)

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=20, pady=20)