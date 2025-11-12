import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from components.bandeau_sup import Band_sup
from components.panier import PanierFrame
from components.product_card import ProductCard
from utils.session import get_session, clear_session
from database.queries import get_all_products_with_category

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#F9F7F0")

        # Bandeau supérieur
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Zone principale : produits à gauche + panier à droite
        self.main_container = ctk.CTkFrame(self, fg_color="#F9F7F0")
        self.main_container.pack(fill="both", expand=True)

        # Partie gauche : produits
        self.left_frame = ctk.CTkFrame(self.main_container, fg_color="#F9F7F0")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=10)

        # Partie droite : panier
        self.panier = PanierFrame(self.main_container, self.controller)
        self.panier.pack(side="right", fill="y", padx=(0, 20), pady=10)
        self.panier.configure(width=400)  # Environ 1/3 de la page

        # Barre de recherche
        self.search_frame = ctk.CTkFrame(self.left_frame)
        self.search_frame.pack(fill="x", pady=10, padx=10)

        self.label = ctk.CTkLabel(self.search_frame, text="Rechercher un produit :", font=("Helvetica", 16, "bold"))
        self.label.pack(side="left", padx=(0, 10))

        self.search_product_entry = ctk.CTkEntry(self.search_frame, width=300, font=("Helvetica", 16))
        self.search_product_entry.pack(side="left")

        # Zone produits scrollable
        self.products_container = ctk.CTkFrame(self.left_frame)
        self.products_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self._canvas = tk.Canvas(self.products_container, highlightthickness=0)
        self._vscroll = ttk.Scrollbar(self.products_container, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._vscroll.set)
        self._vscroll.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._inner_frame = ctk.CTkFrame(self._canvas)
        self._inner_id = self._canvas.create_window((0, 0), window=self._inner_frame, anchor="nw")

        def _on_frame_config(event):
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))

        def _on_canvas_config(event):
            self._canvas.itemconfig(self._inner_id, width=event.width)

        self._inner_frame.bind("<Configure>", _on_frame_config)
        self._canvas.bind("<Configure>", _on_canvas_config)

        # Chargement des produits
        self.products = get_all_products_with_category()
        for product in self.products:
            product_card = ProductCard(self._inner_frame, controller=self.controller, product=product)
            product_card.pack(padx=20, pady=10, fill="x")

        self.refresh()

    def refresh(self, args=None):
        if get_session() is None:
            self.controller.show_page("LoginPage")
        self.bandeau.refresh()
        self.panier.refresh()

        

