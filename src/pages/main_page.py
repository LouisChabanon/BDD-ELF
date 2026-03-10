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

        # Barre de recherche
        self.search_bar = ctk.CTkEntry(self.catalog_frame, placeholder_text="Rechercher ou scanner...", width=300)
        self.search_bar.pack(anchor="w", pady=(0, 20))
        self.search_bar.bind("<Return>", self.handle_search)

        # Zone de défilement pour les cartes produits
        self.scroll_container = ctk.CTkScrollableFrame(self.catalog_frame, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True)
        
        self.all_products = []
        
        # Premier chargement au lancement
        self.load_catalog()

    def load_catalog(self):
        """
        Récupère les données fraîches de la base de données 
        et demande la reconstruction de la liste visuelle.
        """
        # On refait la requête SQL pour avoir les stocks à jour (ex: après un rendu ou un emprunt)
        self.all_products = get_all_materiels_with_stock()
        self.render_list(self.all_products)

    def render_list(self, products):
        """
        Efface les anciennes cartes et affiche les nouvelles.
        """
        # 1. On vide le conteneur actuel pour éviter de superposer les anciennes cartes
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        # 2. Cas où la recherche ne donne rien ou stock vide
        if not products:
            ctk.CTkLabel(self.scroll_container, text="Aucun produit trouvé.", font=("Helvetica", 14)).pack(pady=20)
            return

        # 3. Création des cartes produits
        # Chaque carte recevra le nouveau 'stock_dispo' issu de load_catalog()
        for product in products:
            # On crée l'instance de ProductCard (ton nouveau code avec update_stock_display)
            card = ProductCard(self.scroll_container, self.controller, product)
            card.pack(fill="x", pady=5, padx=5)

    def handle_search(self, event):
        """Logique de filtrage pour la barre de recherche"""
        query = self.search_bar.get().strip().lower()
        if not query:
            self.render_list(self.all_products)
            return

        target_name = None
        # Si c'est un chiffre, on cherche par ID d'exemplaire
        if query.isdigit():
            from database.queries import get_product_name_by_exemplaire_id
            found_name = get_product_name_by_exemplaire_id(query)
            if found_name:
                target_name = found_name.lower()
        
        # Filtrage de la liste stockée en mémoire
        filtered = []
        for p in self.all_products:
            p_name = p['nom_materiel'].lower()
            if query in p_name or (target_name and target_name == p_name):
                filtered.append(p)
        
        self.render_list(filtered)

    def refresh(self, args=None):
        """
        CETTE MÉTHODE EST APPELÉE PAR LE CONTROLLER À CHAQUE AFFICHAGE DE PAGE.
        Elle garantit que les données sont synchronisées avec la BDD.
        """
        # 1. Vérification de la session (sécurité)
        if not get_session():
            self.controller.show_page("LoginPage")
            return

        # 2. Rafraîchir les composants fixes
        self.bandeau.refresh()
        self.panier.refresh()
        
        # 3. Recharger le catalogue depuis la base de données
        # Cela va vider la liste et recréer les ProductCards avec le bon stock
        self.load_catalog()
        
        # 4. Nettoyer la barre de recherche au cas où
        self.search_bar.delete(0, tk.END)