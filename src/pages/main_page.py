import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from components.bandeau_sup import Band_sup
from components.product_card import ProductCard
from utils.session import get_session, clear_session
from database.queries import get_all_products_with_category

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
        
        # Recherche (alignée en haut à gauche)
        # Frame qui occupe la largeur en haut, puis un conteneur à gauche
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(fill="x", side="top", pady=10, padx=20)

        # Conteneur aligné à gauche pour le label et l'entry côte à côte
        self.search_container = ctk.CTkFrame(self.search_frame)
        self.search_container.pack(side="left")

        # Label et champ de recherche côte à côte
        self.label = ctk.CTkLabel(self.search_container, text="Rechercher un produit ou scanner le code-barre :", font=("Helvetica", 16, "bold"))
        self.label.pack(side="left", padx=(0, 10))

        self.search_product_entry = ctk.CTkEntry(self.search_container, width=300, font=("Helvetica", 16))
        self.search_product_entry.pack(side="left")

        # Cadre pour les cartes de produits (scrollable)
        # Container qui prendra l'espace restant
        self.products_container = ctk.CTkFrame(self)
        self.products_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))


        
        self._canvas = tk.Canvas(self.products_container, highlightthickness=0)
        self._vscroll = ttk.Scrollbar(self.products_container, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._vscroll.set)

        self._vscroll.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        # Inner frame inside the canvas where product cards will be placed
        self._inner_frame = ctk.CTkFrame(self._canvas)
        self._inner_id = self._canvas.create_window((0, 0), window=self._inner_frame, anchor="nw")

        def _on_frame_config(event):
            # Update scrollregion to match inner frame size
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))

        def _on_canvas_config(event):
            # Make inner frame width match canvas width
            canvas_width = event.width
            try:
                self._canvas.itemconfig(self._inner_id, width=canvas_width)
            except Exception:
                pass

        self._inner_frame.bind("<Configure>", _on_frame_config)
        self._canvas.bind("<Configure>", _on_canvas_config)

        # Mousewheel support (Windows)
        def _on_mousewheel(event):
            # event.delta is multiple of 120 on Windows
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self._canvas.bind_all("<MouseWheel>", _on_mousewheel)

        products_parent = self._inner_frame

        # Récupération et ajout des cartes dans la frame scrollable
        self.products = get_all_products_with_category()
        print(f"Produits récupérés : {self.products}")

        for product in self.products:
            product_card = ProductCard(products_parent, controller=self.controller, product=product)
            product_card.pack(padx=20, pady=10, fill="x")


        self.refresh()

        
    def refresh(self, args=None):
        # Vérifier la session utilisateur
        if get_session() is None:
            print("Aucun utilisateur connecté, redirection vers la page de connexion.")
            self.controller.show_page("LoginPage")
        self.bandeau.refresh()

        