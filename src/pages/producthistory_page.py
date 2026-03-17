import customtkinter as ctk
from components.bandeau_sup import Band_sup
from database.queries import get_exemplaire_history, get_product_name_by_exemplaire_id

class ProductHistoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.exemplaire_id = None
        self.configure(fg_color="#F9F7F0")

        # Bandeau
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Scrollable Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header Section
        self.header_frame = ctk.CTkFrame(self.scroll_frame, fg_color="white", corner_radius=10)
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="Historique d'emprunt", 
                                     font=("Helvetica", 24, "bold"), anchor="w")
        self.lbl_title.pack(side="left", padx=20, pady=20)

        # Bouton Retour (dynamique vers la page produit)
        self.btn_back = ctk.CTkButton(self.header_frame, text="Retour", fg_color="gray", 
                                      width=100, command=self.go_back)
        self.btn_back.pack(side="right", padx=20, pady=20)

        # Container pour la liste des emprunts
        self.list_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.list_container.pack(fill="x")

    def go_back(self):
        # On retourne à la page produit. 
        # Si on veut que la page produit se rafraîchisse sur le bon matériel :
        nom_mat = get_product_name_by_exemplaire_id(self.exemplaire_id)
        if nom_mat:
            self.controller.frames["ProductPage"].set_product_name(nom_mat)
        self.controller.show_page("ProductPage")

    def refresh(self):
        self.bandeau.refresh()
        if hasattr(self.controller, "shared_data"):
            self.exemplaire_id = self.controller.shared_data.get("selected_exemplaire")
        
        if self.exemplaire_id:
            self.lbl_title.configure(text=f"Historique : Exemplaire #{self.exemplaire_id}")
            self.render_history_list()

    def render_history_list(self):
        # On vide la liste actuelle
        for widget in self.list_container.winfo_children():
            widget.destroy()

        history = get_exemplaire_history(self.exemplaire_id)

        if not history:
            ctk.CTkLabel(self.list_container, text="Aucun historique d'emprunt pour cet exemplaire.", 
                         font=("Helvetica", 14, "italic")).pack(pady=40)
            return

        # Header de tableau
        table_head = ctk.CTkFrame(self.list_container, fg_color="#EBE8DE", corner_radius=5)
        table_head.pack(fill="x", pady=(0, 10))
        
        headers = [("Emprunteur", 200), ("Date Sortie", 150), ("Date Retour", 150), ("Statut", 100)]
        for txt, w in headers:
            ctk.CTkLabel(table_head, text=txt, width=w, font=("Helvetica", 12, "bold"), anchor="w").pack(side="left", padx=10)

        # Lignes de données
        for row_data in history:
            row = ctk.CTkFrame(self.list_container, fg_color="white", corner_radius=5)
            row.pack(fill="x", pady=2)

            nom_complet = f"{row_data['prenom']} {row_data['nom']}"
            date_e = row_data['date_emprunt']
            date_r = row_data['date_rendu']
            
            # Détermination du statut
            is_returned = date_r is not None and str(date_r).strip() != ""
            status_text = "RENDU" if is_returned else "EN COURS"
            status_color = "#8FBC8F" if is_returned else "#C94C3E"
            display_date_r = date_r if is_returned else "--"

            # Affichage des colonnes
            ctk.CTkLabel(row, text=nom_complet, width=200, anchor="w").pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(row, text=date_e, width=150, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=display_date_r, width=150, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=status_text, text_color=status_color, 
                         font=("Helvetica", 11, "bold"), width=100).pack(side="left", padx=10)
            
            # Petit bouton d'info pour voir le motif au survol ou clic (optionnel)
            if row_data['motif']:
                row.bind("<Button-1>", lambda e, m=row_data['motif']: self.show_motif(m))

    def show_motif(self, motif):
        from tkinter import messagebox
        messagebox.showinfo("Motif de l'emprunt", motif)