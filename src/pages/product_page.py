import customtkinter as ctk
import webbrowser
from tkinter import messagebox
from components.bandeau_sup import Band_sup
from database.queries import get_product_by_id, get_exemplaires_by_product_id
from utils.session import get_session


class ProductPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product_id = None
        self.product_data = None
        self.exemplaires = []

        # --- Fond principal ---
        self.configure(fg_color="#F9F7F0")

        # --- Bandeau supérieur ---
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # --- Conteneur principal ---
        self.main_frame = ctk.CTkFrame(self, fg_color="#F9F7F0")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=(20, 80))

        # --- Section photo ---
        self.photo_frame = ctk.CTkFrame(self.main_frame, fg_color="#F9F7F0")
        self.photo_frame.pack(side="left", padx=20, pady=20)

        self.photo_label = ctk.CTkLabel(self.photo_frame, text="Photos du matériel", font=("Helvetica", 18, "bold"))
        self.photo_label.pack(pady=(0, 10))

        self.photo = ctk.CTkLabel(self.photo_frame, width=200, height=200, corner_radius=10, fg_color="gray20")
        self.photo.pack()

        # --- Section infos produit ---
        self.info_frame = ctk.CTkFrame(self.main_frame, fg_color="#F9F7F0")
        self.info_frame.pack(side="left", fill="both", expand=True, padx=40, pady=20)

        self.nom_label = ctk.CTkLabel(self.info_frame, text="Nom du matériel", font=("Helvetica", 22, "bold"))
        self.nom_label.pack(pady=(0, 10), anchor="w")

        self.freq_label = ctk.CTkLabel(self.info_frame, text="Fréquence d’entretien : ", font=("Helvetica", 16))
        self.freq_label.pack(anchor="w", pady=5)

        self.pdf_button = ctk.CTkButton(
            self.info_frame,
            text="📄 Ouvrir le PDF de la fiche produit",
            font=("Helvetica", 16),
            command=self.open_pdf
        )
        self.pdf_button.pack(pady=20, anchor="w")

        # --- Section exemplaires ---
        self.exemplaire_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        self.exemplaire_frame.pack(fill="both", expand=True, padx=60, pady=(0, 60))

        self.exemplaire_title = ctk.CTkLabel(
            self.exemplaire_frame,
            text="Exemplaires disponibles",
            font=("Helvetica", 20, "bold")
        )
        self.exemplaire_title.pack(pady=20)

        # Conteneur pour les lignes d’exemplaires
        self.table_frame = ctk.CTkFrame(self.exemplaire_frame, fg_color="#F9F7F0", corner_radius=10)
        self.table_frame.pack(fill="x", padx=20, pady=10)

        # En-têtes de colonne
        headers = ["Identifiant", "Dernier entretien", "Salle de rangement", "Historique"]
        for i, header in enumerate(headers):
            lbl = ctk.CTkLabel(self.table_frame, text=header, font=("Helvetica", 16, "bold"))
            lbl.grid(row=0, column=i, padx=20, pady=10)

        # --- Boutons bas de page ---
        self.bottom_frame = ctk.CTkFrame(self, fg_color="#F9F7F0")
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


    # --- Rafraîchissement général ---
    def refresh(self):
        if get_session() is None:
            self.controller.show_page("LoginPage")
            return

        self.bandeau.refresh()

        if self.product_id:
            self.product_data = get_product_by_id(self.product_id)
            self.exemplaires = get_exemplaires_by_product_id(self.product_id)

            if self.product_data:
                self.nom_label.configure(text=self.product_data.get("nom_materiel", "Nom inconnu"))
                self.freq_label.configure(
                    text=f"Fréquence d’entretien : {self.product_data.get('frequence_entretient', 'N/A')}"
                )
            else:
                self.nom_label.configure(text="Erreur : produit non trouvé")

            self.display_exemplaires()
        else:
            self.nom_label.configure(text="Aucun produit sélectionné")
            self.clear_exemplaires()


    # --- Affiche les lignes d’exemplaires ---
    def display_exemplaires(self):
        # Supprimer les anciennes lignes (si on refresh)
        for widget in self.table_frame.winfo_children()[len(["Identifiant", "Dernier entretien", "Salle de rangement", "Historique"]):]:
            widget.destroy()

        for row_idx, exemplaire in enumerate(self.exemplaires, start=1):
            ctk.CTkLabel(self.table_frame, text=exemplaire["id_exemplaire"], font=("Helvetica", 15)).grid(row=row_idx, column=0, padx=20, pady=8)
            ctk.CTkLabel(self.table_frame, text=exemplaire["date_dernier_entretient"], font=("Helvetica", 15)).grid(row=row_idx, column=1, padx=20, pady=8)
            ctk.CTkLabel(self.table_frame, text=exemplaire["salle_rangement"], font=("Helvetica", 15)).grid(row=row_idx, column=2, padx=20, pady=8)

            btn = ctk.CTkButton(
                self.table_frame,
                text="📜 Historique",
                width=120,
                command=lambda eid=exemplaire["id_exemplaire"]: self.open_history(eid)
            )
            btn.grid(row=row_idx, column=3, padx=20, pady=8)


    def clear_exemplaires(self):
        for widget in self.table_frame.winfo_children()[len(["Identifiant", "Dernier entretien", "Salle de rangement", "Historique"]):]:
            widget.destroy()


    # --- Méthode : ouvrir la page historique ---
    def open_history(self, exemplaire_id):
        page = self.controller.pages["ProductHistoryPage"]
        page.set_product_id(exemplaire_id)
        page.refresh()
        self.controller.show_page("ProductHistoryPage")


    def goto_modifier_page(self):
        page = self.controller.pages["ModifierProduitPage"]
        page.set_product_id(self.product_id)
        page.refresh()
        self.controller.show_page("ModifierProduitPage")


    def open_pdf(self):
        if not self.product_data:
            messagebox.showwarning("Avertissement", "Aucun produit sélectionné.")
            return

        pdf_path = self.product_data.get("pdf_path")

        if not pdf_path:
            messagebox.showwarning("Avertissement", "Aucun fichier PDF associé à ce produit.")
            return

        # Vérifie si c’est une URL
        if pdf_path.startswith("http://") or pdf_path.startswith("https://"):
            webbrowser.open_new(pdf_path)
        else:
            import os
            if not os.path.exists(pdf_path):
                messagebox.showerror("Erreur", f"Le fichier PDF n’existe pas :\n{pdf_path}")
            else:
                webbrowser.open_new(pdf_path)


    def set_product_id(self, product_id: int):
        self.product_id = product_id
        self.product_data = None