import customtkinter as ctk
import sqlite3
import os
import webbrowser
from components.bandeau_sup import Band_sup


class ProductPage(ctk.CTkFrame):
    def __init__(self, parent, controller, produit_id=None):
        super().__init__(parent)
        self.controller = controller
        self.produit_id = produit_id
        self.produit = None

        # Charger les infos du produit depuis la base
        if produit_id is not None:
            self.produit = self.get_produit_from_db(produit_id)

        # Couleur de fond principale
        self.configure(fg_color="#F9F7F0")

        # Bandeau supérieur
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Contenu principal
        self.main_frame = ctk.CTkFrame(self)
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

        nom = self.produit.get("nom", "Nom du matériel") if self.produit else "Nom du matériel"
        type_ = self.produit.get("type", "Type inconnu") if self.produit else "Type inconnu"
        freq = self.produit.get("frequence_entretien", "Non spécifiée") if self.produit else "Non spécifiée"
        dernier = self.produit.get("dernier_entretien", "Inconnu") if self.produit else "Inconnu"

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


    # --- Méthode pour aller à la page de modification ---
    def goto_modifier_page(self):
        self.controller.show_page("ModifierProduitPage")


    # --- Récupérer les infos du matériel depuis la BDD ---
    def get_produit_from_db(self, produit_id):
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nom, type, frequence_entretien, dernier_entretien, pdf_path 
                FROM materiels WHERE id = ?
            """, (produit_id,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    "nom": row[0],
                    "type": row[1],
                    "frequence_entretien": row[2],
                    "dernier_entretien": row[3],
                    "pdf_path": row[4]
                }
            else:
                return {}
        except Exception as e:
            print("Erreur SQL :", e)
            return {}


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