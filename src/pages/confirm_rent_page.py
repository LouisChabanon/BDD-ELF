import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from components.bandeau_sup import Band_sup
from utils.session import get_cart, get_session, clear_session
from database.queries import add_loan

class ConfirmRentPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#F9F7F0")

        # Bandeau
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Container Principal
        self.main_container = ctk.CTkFrame(self, fg_color="#F9F7F0")
        self.main_container.pack(fill="both", expand=True, padx=40, pady=20)

        # Titre
        ctk.CTkLabel(
            self.main_container, 
            text="Confirmation de l'emprunt", 
            font=("Helvetica", 24, "bold"), 
            text_color="#4A4947"
        ).pack(pady=(10, 30))

        # --- Zone Gauche : Liste des articles ---
        self.left_frame = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=10)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=10)
        
        ctk.CTkLabel(self.left_frame, text="Articles à emprunter :", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        self.items_scroll = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent")
        self.items_scroll.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Zone Droite : Formulaire ---
        self.right_frame = ctk.CTkFrame(self.main_container, fg_color="#F2EDE4", corner_radius=10)
        self.right_frame.pack(side="right", fill="y", padx=0, pady=10, ipadx=20)

        ctk.CTkLabel(self.right_frame, text="Détails de l'emprunt", font=("Helvetica", 18, "bold")).pack(pady=(20, 20))

        # Motif
        ctk.CTkLabel(self.right_frame, text="Motif de l'emprunt :", font=("Helvetica", 14)).pack(anchor="w", padx=20, pady=(10, 0))
        self.motif_entry = ctk.CTkEntry(self.right_frame, width=300, placeholder_text="Ex: TP Électronique, Projet 2A...")
        self.motif_entry.pack(padx=20, pady=(5, 15))

        # Date de retour prévue
        # Note: Sans tkcalendar, on utilise un champ texte simple avec validation basique
        ctk.CTkLabel(self.right_frame, text="Date de retour prévue (JJ/MM/AAAA) :", font=("Helvetica", 14)).pack(anchor="w", padx=20, pady=(10, 0))
        self.date_entry = ctk.CTkEntry(self.right_frame, width=300, placeholder_text=datetime.now().strftime("%d/%m/%Y"))
        self.date_entry.pack(padx=20, pady=(5, 20))

        # Boutons
        self.btn_confirm = ctk.CTkButton(
            self.right_frame, 
            text="✅ Valider l'emprunt", 
            font=("Helvetica", 16, "bold"),
            height=45,
            command=self.validate_loan
        )
        self.btn_confirm.pack(padx=20, pady=(20, 10), fill="x")

        self.btn_cancel = ctk.CTkButton(
            self.right_frame, 
            text="Annuler", 
            fg_color="transparent", 
            border_width=2, 
            text_color="#B17457",
            hover_color="#EEE",
            command=lambda: controller.show_page("MainPage")
        )
        self.btn_cancel.pack(padx=20, pady=10, fill="x")

    def refresh(self):
        """Charge les items du panier au moment d'afficher la page."""
        self.bandeau.refresh()
        
        # Nettoyer la liste visuelle
        for widget in self.items_scroll.winfo_children():
            widget.destroy()

        cart = get_cart()
        if not cart:
            ctk.CTkLabel(self.items_scroll, text="Votre panier est vide.", text_color="gray").pack(pady=20)
            self.btn_confirm.configure(state="disabled")
        else:
            self.btn_confirm.configure(state="normal")
            for item in cart:
                row = ctk.CTkFrame(self.items_scroll, fg_color="#F9F7F0", corner_radius=6)
                row.pack(fill="x", pady=5)
                
                info = f"{item['nom_materiel']} (#{item['id_exemplaire']})"
                ctk.CTkLabel(row, text=info, font=("Helvetica", 14)).pack(side="left", padx=10, pady=10)
                ctk.CTkLabel(row, text=item.get('lieu_rangement', ''), text_color="gray").pack(side="right", padx=10)

    def validate_loan(self):
        cart = get_cart()
        user = get_session()

        if not user:
            messagebox.showerror("Erreur", "Vous devez être connecté.")
            self.controller.show_page("LoginPage")
            return

        if not cart:
            messagebox.showwarning("Attention", "Le panier est vide.")
            return

        motif = self.motif_entry.get().strip()
        date_fin = self.date_entry.get().strip()

        if not motif:
            messagebox.showwarning("Champs manquants", "Veuillez indiquer un motif.")
            return
        
        if not date_fin:
            messagebox.showwarning("Champs manquants", "Veuillez indiquer une date de retour.")
            return

        # Construction du motif complet pour la BDD (puisque la BDD Emprunt n'a pas de colonne date_fin explicite)
        motif_complet = f"{motif} [Retour prévu: {date_fin}]"
        date_emprunt = datetime.now().strftime("%d_%m_%Y") # Format compatible BDD existante

        success_count = 0
        try:
            for item in cart:
                add_loan(
                    motif=motif_complet,
                    date_emprunt=date_emprunt,
                    id_exemplaire=item['id_exemplaire'],
                    id_personnel=user['id_personnel']
                )
                success_count += 1
            
            # Si tout s'est bien passé
            clear_session() # Vide le panier
            messagebox.showinfo("Succès", f"{success_count} article(s) emprunté(s) avec succès !")
            
            # Nettoyer les champs
            self.motif_entry.delete(0, 'end')
            self.date_entry.delete(0, 'end')
            
            self.controller.show_page("MainPage")

        except Exception as e:
            messagebox.showerror("Erreur BDD", f"Une erreur est survenue lors de l'enregistrement : {e}")