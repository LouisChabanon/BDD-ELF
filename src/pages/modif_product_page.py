import customtkinter as ctk
from tkinter import filedialog, messagebox
from components.bandeau_sup import Band_sup
from database.queries import get_product_by_id, update_product
from utils.session import get_session
import os


class ModifierProduitPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product_id = None
        self.product_data = None

        # --- Fond principal ---
        self.configure(fg_color="#F9F7F0")

        # --- Bandeau supérieur ---
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # --- Conteneur principal ---
        self.main_frame = ctk.CTkFrame(self, fg_color="#F9F7F0")
        self.main_frame.pack(fill="both", expand=True, padx=60, pady=40)

        # --- Titre ---
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Modifier la fiche produit",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=(0, 20))

        # --- Zone du formulaire ---
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF", corner_radius=15)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Nom du matériel
        self.nom_label = ctk.CTkLabel(self.form_frame, text="Nom du matériel :", font=("Helvetica", 16))
        self.nom_label.grid(row=0, column=0, padx=20, pady=15, sticky="e")
        self.nom_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.nom_entry.grid(row=0, column=1, padx=20, pady=15)

        # Fréquence d’entretien
        self.freq_label = ctk.CTkLabel(self.form_frame, text="Fréquence d’entretien :", font=("Helvetica", 16))
        self.freq_label.grid(row=1, column=0, padx=20, pady=15, sticky="e")
        self.freq_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.freq_entry.grid(row=1, column=1, padx=20, pady=15)

        # Date du dernier entretien
        self.date_label = ctk.CTkLabel(self.form_frame, text="Dernier entretien :", font=("Helvetica", 16))
        self.date_label.grid(row=2, column=0, padx=20, pady=15, sticky="e")
        self.date_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.date_entry.grid(row=2, column=1, padx=20, pady=15)

        # PDF associé
        self.pdf_label = ctk.CTkLabel(self.form_frame, text="Notice / PDF associé :", font=("Helvetica", 16))
        self.pdf_label.grid(row=3, column=0, padx=20, pady=15, sticky="e")

        self.pdf_path_var = ctk.StringVar()
        self.pdf_entry = ctk.CTkEntry(self.form_frame, textvariable=self.pdf_path_var, width=300)
        self.pdf_entry.grid(row=3, column=1, padx=20, pady=15)

        self.pdf_button = ctk.CTkButton(
            self.form_frame,
            text="Choisir un fichier PDF",
            command=self.select_pdf
        )
        self.pdf_button.grid(row=3, column=2, padx=10)

        # --- Boutons bas de page ---
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="#F9F7F0")
        self.button_frame.pack(fill="x", pady=20)

        self.save_button = ctk.CTkButton(
            self.button_frame,
            text="💾 Enregistrer les modifications",
            font=("Helvetica", 16, "bold"),
            command=self.save_changes
        )
        self.save_button.pack(side="left", padx=30)

        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Annuler",
            font=("Helvetica", 16),
            command=lambda: controller.show_page("ProductPage")
        )
        self.cancel_button.pack(side="right", padx=30)

    # --- Sélection du fichier PDF ---
    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Choisir un fichier PDF",
            filetypes=[("Fichiers PDF", "*.pdf")]
        )
        if file_path:
            self.pdf_path_var.set(file_path)

    # --- Chargement des données du produit ---
    def refresh(self):
        if get_session() is None:
            self.controller.show_page("LoginPage")
            return

        self.bandeau.refresh()

        if self.product_id:
            self.product_data = get_product_by_id(self.product_id)
            if self.product_data:
                self.nom_entry.delete(0, "end")
                self.nom_entry.insert(0, self.product_data.get("nom_materiel", ""))

                self.freq_entry.delete(0, "end")
                self.freq_entry.insert(0, self.product_data.get("frequence_entretient", ""))

                self.date_entry.delete(0, "end")
                self.date_entry.insert(0, self.product_data.get("date_dernier_entretient", ""))

                self.pdf_path_var.set(self.product_data.get("notice_materiel", ""))
            else:
                messagebox.showerror("Erreur", "Produit introuvable.")
        else:
            messagebox.showwarning("Attention", "Aucun produit sélectionné.")

    # --- Définit quel produit est en cours d’édition ---
    def set_product_id(self, product_id: int):
        self.product_id = product_id
        self.product_data = None

    # --- Enregistre les changements dans la BDD ---
    def save_changes(self):
        if not self.product_id:
            messagebox.showerror("Erreur", "Aucun produit sélectionné.")
            return

        new_data = {
            "nom_materiel": self.nom_entry.get().strip(),
            "frequence_entretient": self.freq_entry.get().strip(),
            "date_dernier_entretient": self.date_entry.get().strip(),
            "pdf_path": self.pdf_path_var.get().strip()
        }

        # Validation basique
        if not new_data["nom_materiel"]:
            messagebox.showwarning("Champ manquant", "Le nom du matériel ne peut pas être vide.")
            return

        try:
            update_product(self.product_id, new_data)
            messagebox.showinfo("Succès", "Les modifications ont été enregistrées avec succès.")
            self.controller.show_page("ProductPage")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d’enregistrer les changements : {e}")