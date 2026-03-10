import customtkinter as ctk
import tkinter as tk
from components.bandeau_sup import Band_sup
from components.panier import PanierFrame
from components.product_card import ProductCard
from database.queries import get_all_materiels_with_stock
from utils.session import get_session

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#F9F7F0")

        # --- VARIABLES DE CONTRÔLE ---
        # Utilisation d'une StringVar pour surveiller la saisie en temps réel
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search_change)
        self._search_after_id = None # Pour le système de "debounce" (délai)

        # --- BANDEAU SUPÉRIEUR ---
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # --- CONTENEUR PRINCIPAL ---
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True)

        # --- PANIER (Droite) ---
        self.panier = PanierFrame(self.content, self.controller)
        self.panier.pack(side="right", fill="y", padx=10, pady=10)
        self.panier.configure(width=350)

        # --- CATALOGUE (Gauche) ---
        self.catalog_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.catalog_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Barre de recherche (liée à self.search_var)
        self.search_bar = ctk.CTkEntry(
            self.catalog_frame, 
            placeholder_text="Rechercher ou scanner...", 
            width=300,
            textvariable=self.search_var
        )
        self.search_bar.pack(anchor="w", pady=(0, 20))

        # Zone de défilement pour les cartes produits
        self.scroll_container = ctk.CTkScrollableFrame(self.catalog_frame, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True)
        
        self.all_products = []
        
        # Premier chargement au lancement
        self.load_catalog()

    def on_search_change(self, *args):
        """
        Méthode appelée à chaque modification du texte dans la barre de recherche.
        Inclut un délai (debounce) pour éviter de recalculer l'affichage trop souvent.
        """
        # Annule l'exécution prévue si l'utilisateur tape une nouvelle touche rapidement
        if self._search_after_id:
            self.after_cancel(self._search_after_id)
        
        # Planifie la recherche dans 200ms
        self._search_after_id = self.after(200, self.handle_search)

    def load_catalog(self):
        """Récupère les données fraîches de la BDD."""
        self.all_products = get_all_materiels_with_stock()
        self.render_list(self.all_products)

    def render_list(self, products):
        """Efface les anciennes cartes et affiche les nouvelles."""
        # 1. On vide le conteneur
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        # 2. Cas vide
        if not products:
            ctk.CTkLabel(
                self.scroll_container, 
                text="Aucun produit trouvé.", 
                font=("Helvetica", 14)
            ).pack(pady=20)
            return

        # 3. Création des cartes produits
        for product in products:
            card = ProductCard(self.scroll_container, self.controller, product)
            card.pack(fill="x", pady=5, padx=5)

    def handle_search(self, event=None):
        """Logique de filtrage basée sur la saisie actuelle."""
        query = self.search_var.get().strip().lower()
        
        # Si vide, on réaffiche tout le catalogue stocké en mémoire
        if not query:
            self.render_list(self.all_products)
            return

        target_name = None
        # Recherche par ID d'exemplaire (si numérique)
        if query.isdigit():
            from database.queries import get_product_name_by_exemplaire_id
            found_name = get_product_name_by_exemplaire_id(query)
            if found_name:
                target_name = found_name.lower()
        
        # Filtrage de la liste locale (plus rapide qu'une requête SQL)
        filtered = []
        for p in self.all_products:
            p_name = p['nom_materiel'].lower()
            # On vérifie si la recherche est dans le nom OU si l'ID scanné correspond au produit
            if query in p_name or (target_name and target_name == p_name):
                filtered.append(p)
        
        self.render_list(filtered)

    def refresh(self, args=None):
        """Synchronisation appelée à chaque affichage de la page."""
        if not get_session():
            self.controller.show_page("LoginPage")
            return

        self.bandeau.refresh()
        self.panier.refresh()
        
        # Recharger les données (cas où le stock a changé ailleurs)
        self.load_catalog()
        
        # Nettoyer la barre de recherche (optionnel, selon ton besoin ergonomique)
        self.search_var.set("")