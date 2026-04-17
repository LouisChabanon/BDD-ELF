import customtkinter as ctk
from database.queries import get_currently_borrowed_items
from database.queries import get_all_users
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

        #Bouton pour obtenir tous les utilisateurs
        self.show_users_button = ctk.CTkButton(self,text="Voir tous les utilisateurs",command=self.open_users_popup)
        self.show_users_button.pack(pady=10)

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

    def open_users_popup(self):
        """Ouvre une fenêtre affichant tous les utilisateurs"""

        popup = ctk.CTkToplevel(self)
        popup.title("Liste des utilisateurs")
        popup.geometry("400x400")

        popup.lift()                  # met la fenêtre devant
        popup.attributes("-topmost", True)  # toujours au-dessus
        popup.after(100, lambda: popup.attributes("-topmost", False))  # optionnel : enlève le "always on top"
        popup.focus_force() 

        # Frame scrollable pour la liste
        scrollable = ctk.CTkScrollableFrame(popup)
        scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        users = get_all_users()

        if not users:
            label = ctk.CTkLabel(scrollable, text="Aucun utilisateur trouvé.")
            label.pack(pady=10)
            return

        for user in users:
            # adapte selon la structure de ton tuple/dict
            text = f"{user}"
            label = ctk.CTkLabel(scrollable, text=text, anchor="w")
            label.pack(fill="x", padx=5, pady=2)