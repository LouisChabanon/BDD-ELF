import customtkinter as ctk
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
        
        # Recherche (alignée en haut à droite)
        # Frame qui occupe la largeur en haut, puis un conteneur à droite
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(fill="x", side="top", pady=10, padx=20)

        # Conteneur aligné à droite pour le label et l'entry côte à côte
        self.search_container = ctk.CTkFrame(self.search_frame)
        self.search_container.pack(side="right")

        # Label et champ de recherche côte à côte
        self.label = ctk.CTkLabel(self.search_container, text="Rechercher un produit ou scanner le code-barre :", font=("Helvetica", 16, "bold"))
        self.label.pack(side="left", padx=(0, 10))

        self.search_product_entry = ctk.CTkEntry(self.search_container, width=300, font=("Helvetica", 16))
        self.search_product_entry.pack(side="left")

        # Cadre pour les cartes de produits
        self.products = get_all_products_with_category()
        print(f"Produits récupérés : {self.products}")

        for product in self.products:
            self.productCard = ProductCard(self, nom=product[4], categorie="test", disponible=True, code="123234")
            self.productCard.pack(padx=20, pady=10, fill="x")

        # Bouton de déconnexion
        self.logout_button = ctk.CTkButton(self, text="Se déconnecter", font=("Helvetica", 16), command=self.logout)
        self.logout_button.pack(pady=20)

        self.refresh()

        
    def refresh(self):
        # Vérifier la session utilisateur
        if get_session() is None:
            print("Aucun utilisateur connecté, redirection vers la page de connexion.")
            self.controller.show_page("LoginPage")
        self.bandeau.refresh()

        

        



    def logout(self):
        print("Utilisateur se déconnecte.")
        clear_session()
        self.controller.show_page("LoginPage")