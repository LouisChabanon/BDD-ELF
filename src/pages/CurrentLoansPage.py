import customtkinter as ctk
from database.queries import get_currently_borrowed_items
from components.borrowed_product_card import BorrowedProductCard
from components.bandeau_sup import Band_sup

class CurrentLoansPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- BANDEAU SUPÉRIEUR ---
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Titre de la page
        self.title_label = ctk.CTkLabel(
            self,
            text="Emprunts Actuels",
            font=("Helvetica", 20, "bold")
        )
        self.title_label.pack(pady=20)


        # Frame scrollable pour contenir toutes les cartes
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Liste des cartes pour référence si besoin
        self.cards = []

    def refresh(self):
        """Rafraîchit la liste des emprunts actuels"""
        # 1. Supprime toutes les cartes existantes
        for card in self.cards:
            card.destroy()
        self.cards.clear()

        # 2. Récupère tous les emprunts en cours
        borrowed_items = get_currently_borrowed_items()

        # 3. Crée une carte pour chaque emprunt
        for item in borrowed_items:
            card = BorrowedProductCard(self.scrollable_frame, self.controller, item)
            card.pack(fill="x", pady=5)
            self.cards.append(card)