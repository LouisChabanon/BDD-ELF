import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from components.bandeau_sup import Band_sup
from components.product_card import ProductCard
from utils.session import get_session
from database.queries import get_all_products_with_category


class PanierFrame(ctk.CTkFrame):
    """Panneau latéral droit pour le panier."""
    def __init__(self, parent):
        super().__init__(parent, fg_color="white", corner_radius=10)
        
        self.pack_propagate(False)

        title = ctk.CTkLabel(self, text="🛒 Panier", font=("Helvetica", 20, "bold"))
        title.pack(pady=(15, 10))

        # Conteneur scrollable pour les objets du panier
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10)
        self.scrollbar.pack(side="right", fill="y")

        # Exemple d’objets dans le panier
        for i in range(3):
            item = ctk.CTkFrame(self.scrollable_frame, fg_color="#F6F6F6", corner_radius=8)
            item.pack(fill="x", padx=5, pady=8)

            ctk.CTkLabel(item, text="Catégorie", font=("Helvetica", 12)).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(item, text="Nom objet", font=("Helvetica", 14, "bold")).pack(anchor="w", padx=10)
            ctk.CTkButton(item, text="Fiche produit", width=100, fg_color="#E1E1E1", text_color="black").pack(anchor="w", padx=10, pady=(5, 5))
            ctk.CTkLabel(item, text="B164", font=("Helvetica", 13)).pack(anchor="w", padx=10)

        # Bouton final
        validate_btn = ctk.CTkButton(self, text="Valider mes emprunts", fg_color="#222222", hover_color="#333333")
        validate_btn.pack(side="bottom", pady=20, padx=20)