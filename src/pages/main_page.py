import customtkinter as ctk
import tkinter as tk
from components.bandeau_sup import Band_sup
from components.panier import PanierFrame
from components.product_card import ProductCard
from database.queries import get_all_materiels, get_all_materiels_with_stock
from utils.session import get_session

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#F9F7F0")

        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True)

        # Panier 
        self.panier = PanierFrame(self.content, self.controller)
        self.panier.pack(side="right", fill="y", padx=10, pady=10)
        self.panier.configure(width=350)

        # Catalogue 
        self.catalog_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.catalog_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Bar de recherche
        self.search_bar = ctk.CTkEntry(self.catalog_frame, placeholder_text="Rechercher ou scanner...", width=300)
        self.search_bar.pack(anchor="w", pady=(0, 20))
        self.search_bar.bind("<Return>", self.handle_search)

        # Scrollable List Container
        self.scroll_container = ctk.CTkScrollableFrame(self.catalog_frame, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True)
        
        self.all_products = []
        self.load_catalog()

    def load_catalog(self):
        self.all_products = get_all_materiels_with_stock()
        self.render_list(self.all_products)

    def render_list(self, products):
        # Clear existing
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        if not products:
            ctk.CTkLabel(self.scroll_container, text="Aucun produit trouvé.").pack(pady=20)
            return

        # Render Rows
        for product in products:
            card = ProductCard(self.scroll_container, self.controller, product)
            card.pack(fill="x", pady=5, padx=5)

    def handle_search(self, event):
        query = self.search_bar.get().strip().lower()
        if not query:
            self.render_list(self.all_products)
            return

        target_name = None
        if query.isdigit():
            from database.queries import get_product_name_by_exemplaire_id
            found_name = get_product_name_by_exemplaire_id(query)
            if found_name:
                target_name = found_name.lower()
        
        filtered = []
        for p in self.all_products:
            p_name = p['nom_materiel'].lower()
            if query in p_name or (target_name and target_name == p_name):
                filtered.append(p)
        
        self.render_list(filtered)

    def refresh(self, args=None):
        if not get_session():
            self.controller.show_page("LoginPage")
        self.bandeau.refresh()
        self.panier.refresh()
        self.load_catalog()