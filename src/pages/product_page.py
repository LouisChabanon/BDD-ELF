import customtkinter as ctk
import os
import webbrowser
from components.bandeau_sup import Band_sup
from database.queries import get_product_by_id
from utils.session import get_session


class ProductPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product_id = None
        self.product = None

        # Couleur de fond principale
        self.configure(fg_color="#F9F7F0")

        # Bandeau supérieur
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Contenu principal
        self.main_frame = ctk.CTkFrame(self,fg_color="#F9F7F0")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=(20, 80))

        # --- Section photos ---
        self.photo_frame = ctk.CTkFrame(self.main_frame)
        self.photo_frame.pack(side="left", padx=20, pady=20)

        self.photo_label = ctk.CTkLabel(self.photo_frame, text="Photos du matériel", font=("Helvetica", 18, "bold"))
        self.photo_label.pack(pady=(0, 10))

        self.photo = ctk.CTkLabel(self.photo_frame, width=200, height=200, corner_radius=10, fg_color="gray20")
        self.photo.pack()

        # --- Section infos produit ---
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(side="left", fill="both", expand=True, padx=40, pady=20)

        nom = "Nom du matériel"
        type_ = "Type inconnu"
        freq = "Non spécifiée"
        dernier = "Inconnu"

        self.nom_label = ctk.CTkLabel(self.info_frame, text=nom, font=("Helvetica", 22, "bold"))
        self.nom_label.pack(pady=(0, 10), anchor="w")

        self.type_label = ctk.CTkLabel(self.info_frame, text=f"Type : {type_}", font=("Helvetica", 16))
        self.type_label.pack(anchor="w", pady=5)

        self.freq_label = ctk.CTkLabel(self.info_frame, text=f"Fréquence d’entretien : {freq}", font=("Helvetica", 16))
        self.freq_label.pack(anchor="w", pady=5)

        self.dernier_label = ctk.CTkLabel(self.info_frame, text=f"Dernier entretien : {dernier}", font=("Helvetica", 16))
        self.dernier_label.pack(anchor="w", pady=5)

        # --- Bouton pour ouvrir le PDF ---
        self.pdf_button = ctk.CTkButton(
            self.info_frame,
            text="📄 Ouvrir le PDF de la fiche produit",
            font=("Helvetica", 16),
            command=self.open_pdf
        )
        self.pdf_button.pack(pady=20, anchor="w")

        # --- Boutons bas de page ---
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(side="bottom", fill="x", pady=20, padx=20)

        self.modifier_button = ctk.CTkButton(
            self.bottom_frame,
            text="Modifier la fiche produit",
            font=("Helvetica", 16),
            command=self.goto_modifier_page
        )
        self.modifier_button.pack(side="left", padx=20)

        self.retour_button = ctk.CTkButton(
            self.bottom_frame,
            text="Retour",
            font=("Helvetica", 16),
            command=lambda: controller.show_page("MainPage")
        )
        self.retour_button.pack(side="right", padx=20)



    def refresh(self):
        """Actualise le bandeau et charge les données du produit."""
        # Vérifier la session
        if get_session() is None:
            self.controller.show_page("LoginPage")
            return
            
        self.bandeau.refresh()
        
        # Charger les données du produit si l'ID est défini
        if self.product_id:
            print(f"Chargement des données pour le produit ID: {self.product_id}")
            self.product_data = get_product_by_id(self.product_id)
            
            if self.product_data:
                self.nom_label.configure(text=self.product_data.get("nom_materiel", "Nom inconnu"))
                # Note: "Type" n'est pas dans la BDD, on utilise nom_materiel
                self.type_label.configure(text=f"Type : {self.product_data.get('nom_materiel', 'N/A')}")
                self.freq_label.configure(text=f"Fréquence d’entretien : {self.product_data.get('frequence_entretient', 'N/A')}")
                self.dernier_label.configure(text=f"Dernier entretien : {self.product_data.get('date_dernier_entretient', 'N/A')}")
                #self.loc_label.configure(text=f"Localisation : {self.product_data.get('lieu_rangement', 'N/A')}")
            else:
                print(f"Erreur: Impossible de trouver le produit avec l'ID {self.product_id}")
                self.nom_label.configure(text="Erreur : Produit non trouvé")
                self.type_label.configure(text="Type : N/A")
                self.freq_label.configure(text="Fréquence d’entretien : N/A")
                self.dernier_label.configure(text="Dernier entretien : N/A")
                #self.loc_label.configure(text="Localisation : N/A")
        else:
            self.nom_label.configure(text="Aucun produit sélectionné")

    def set_product_id(self, product_id: int):
        self.product_id = product_id
        self.product_data = None


    # --- Méthode pour aller à la page de modification ---
    def goto_modifier_page(self):
        self.controller.show_page("ModifierProduitPage")




    # --- Ouvrir le PDF associé ---
    def open_pdf(self):
        if not self.produit or not self.produit.get("pdf_path"):
            print("Aucun fichier PDF associé.")
            return

        pdf_path = self.produit["pdf_path"]

        if not os.path.exists(pdf_path):
            print("Le fichier PDF n’existe pas :", pdf_path)
            return

        webbrowser.open_new(pdf_path)