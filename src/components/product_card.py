import customtkinter as ctk
from utils.session import get_cart, add_to_cart
from database.queries import get_product_history

class ProductCard(ctk.CTkFrame):
    def __init__(self, parent, controller, product: dict):
        super().__init__(parent)
        self.controller = controller
        
        self.product_data = product
        self.nom = product.get("nom_materiel", "N/A")
        self.categorie = product.get("nom_materiel", "N/A")
        self.code = product.get("id_exemplaire", "N/A")
        self.disponible = self.is_available()
        
        # Configuration de la grille principale
        self.grid_columnconfigure(1, weight=1)

        self.configure(corner_radius=15, border_width=2, fg_color="#FFFFFF")
        
        # Image à gauche
        self.image_label = ctk.CTkLabel(self, text="🖼️", width=150, height=150, fg_color="white", corner_radius=10)
        self.image_label.grid(row=0, column=0, rowspan=4, padx=15, pady=15)
        
        # Cadre gauche (tout ce qui est aligné : catégorie → fiche produit)
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=1, sticky="w", padx=(5, 20), pady=10)
        
        # Catégorie
        self.cat_label = ctk.CTkLabel(self.left_frame, text=f"{self.categorie}", text_color="gray")
        self.cat_label.grid(row=0, column=0, sticky="w")
        
        # Nom de l’objet
        self.nom_label = ctk.CTkLabel(self.left_frame, text=self.nom)
        self.nom_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        # État (Disponible / Indisponible)
        self.status_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.status_frame.grid(row=2, column=0, sticky="w", pady=5)
        
        self.status_dispo = ctk.CTkButton(
            self.status_frame,
            text="Disponible",
            fg_color="#8FBC8F",
            text_color="black",
            corner_radius=20,
            width=100,
            state="disabled"
        )
        
        self.status_indispo = ctk.CTkButton(
            self.status_frame,
            text="Indisponible",
            fg_color="#C94C3E",
            text_color="black",
            corner_radius=20,
            width=100,
            state="disabled"
        )

        self.update_status(self.disponible)
        
        # Fiche produit / Historique / Code
        self.actions_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.actions_frame.grid(row=3, column=0, sticky="w", pady=(10, 10))
        
        self.btn_fiche = ctk.CTkButton(self.actions_frame, text="Fiche produit", width=120, fg_color="white", text_color="black", command=self.open_product_page, border_width=2)
        self.btn_fiche.pack(side="left", padx=5)
        
        # Boutons à droite : Emprunter / Réserver
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=2, rowspan=4, padx=20, pady=15)
        
        self.btn_emprunter = ctk.CTkButton(self.right_frame, text="Emprunter", width=120, command=self.add_product_to_cart)
        self.btn_emprunter.pack(pady=(0, 15))
        
        self.btn_reserver = ctk.CTkButton(self.right_frame, text="Réserver", width=120)
        self.btn_reserver.pack()

    def open_product_page(self):
        if self.code != 'N/A':
            self.controller.show_product_page(self.code)
        else:
            print("Erreur : Impossible d'ouvrir la page, ID manquant")

    def open_history_page(self):
        if self.code != 'N/A':
            self.controller.show_product_history_page(self.code)
        else:
            print("Erreur : Impossible d'ouvrir la page, ID manquant")

    def add_product_to_cart(self):
        print(f"Adding {self.product_data} to cart", )
        items_in_panier = get_cart()
        if self.product_data not in items_in_panier:
            add_to_cart(self.product_data)
            self.controller.show_page("MainPage")

    def is_available(self):
        product_id = self.product_data["id_exemplaire"]
        product_history =  get_product_history(product_id)
        
        if(product_history == []):
            print(f"No product history for {product_id}")
            return True


    def update_status(self, is_available):

        self.status_dispo.pack_forget()
        self.status_indispo.pack_forget()

        if is_available:
            self.status_dispo.pack(side="left")
        else:
            self.status_dispo.pack(side="left")