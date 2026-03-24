import customtkinter as ctk
import webbrowser
from tkinter import messagebox
from components.bandeau_sup import Band_sup
from components.scan_popup import RentValidationPopup
from database.queries import get_product_details, get_exemplaires_with_status, get_product_name_by_exemplaire_id
from utils.session import get_session, add_to_cart

class ProductPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product_name = None
        self.pdf_path = None
        self.configure(fg_color="#F9F7F0")

        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- HEADER SECTION ---
        self.header_frame = ctk.CTkFrame(self.scroll_frame, fg_color="white", corner_radius=10)
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.img_label = ctk.CTkLabel(self.header_frame, text="📷", width=100, height=100, fg_color="#eee")
        self.img_label.pack(side="left", padx=20, pady=20)
        
        self.info_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.info_container.pack(side="left", fill="both", expand=True, pady=10)
        
        self.lbl_title = ctk.CTkLabel(self.info_container, text="...", font=("Helvetica", 24, "bold"), anchor="w")
        self.lbl_title.pack(fill="x")
        
        self.lbl_maint = ctk.CTkLabel(self.info_container, text="", font=("Helvetica", 14), anchor="w")
        self.lbl_maint.pack(fill="x", pady=5)

        self.btn_pdf = ctk.CTkButton(self.info_container, text="📄 Notice PDF", width=100, command=self.open_pdf)
        self.btn_pdf.pack(anchor="w", pady=5)

        # --- RENT BUTTON ---
        self.btn_rent = ctk.CTkButton(
            self.header_frame, 
            text="Emprunter ce produit", 
            fg_color="#B17457",
            hover_color="#9C6049",
            width=150,
            height=40,
            font=("Helvetica", 14, "bold"),
            command=self.initiate_general_rent
        )
        self.btn_rent.pack(side="right", padx=20)

        # List Section
        self.list_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.list_container.pack(fill="x")

    def set_product_name(self, name):
        self.product_name = name
        self.refresh()

    def refresh(self):
        if not get_session():
            self.controller.show_page("LoginPage")
            return
        self.bandeau.refresh()

        if not self.product_name:
            return

        details = get_product_details(self.product_name)
        if details:
            self.lbl_title.configure(text=details.get('nom_materiel'))
            self.lbl_maint.configure(text=f"Entretien : {details.get('frequence_entretient')} mois")
            self.pdf_path = details.get('notice_materiel')
        
        self.render_exemplaires_list()

    def render_exemplaires_list(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()

        items = get_exemplaires_with_status(self.product_name)
        
        if not items:
            self.btn_rent.configure(state="disabled") # Désactive si aucun stock du tout
            ctk.CTkLabel(self.list_container, text="Aucun exemplaire répertorié.").pack(pady=20)
            return

        # Vérifier si au moins un exemplaire est dispo pour activer le bouton global
        any_available = any(item['is_available'] for item in items)
        self.btn_rent.configure(state="normal" if any_available else "disabled")

        for item in items:
            row = ctk.CTkFrame(self.list_container, fg_color="white", corner_radius=5)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=f"#{item['id_exemplaire']}", font=("Courier", 14, "bold"), width=80).pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(row, text=item.get('lieu_rangement', 'N/A'), width=150).pack(side="left", padx=10)
            
            is_avail = item['is_available']
            status_text = "DISPONIBLE" if is_avail else "EMPRUNTÉ"
            status_color = "#8FBC8F" if is_avail else "#C94C3E"
            
            ctk.CTkLabel(row, text=status_text, text_color=status_color, font=("Helvetica", 12, "bold")).pack(side="left", padx=20)
            # NOTE : Les boutons individuels ont été supprimés ici pour nettoyer la vue.

    def initiate_general_rent(self):
        """Lance le scan. Ici on passe le nom du produit global"""
        # On demande à l'utilisateur de scanner l'ID de n'importe quel exemplaire de ce produit
        RentValidationPopup(self, self.product_name, self.confirm_general_rent)

    def confirm_general_rent(self, scanned_item_id):
        """
        Action après scan. 
        scanned_item_id est la valeur retournée par la popup (ex: l'ID scanné).
        """
        # Ici, on construit un mini-objet pour le panier
        item_to_add = {
            'id_exemplaire': scanned_item_id,
            'nom_materiel': self.product_name
        }
        add_to_cart(item_to_add)
        messagebox.showinfo("Succès", f"Produit {scanned_item_id} ajouté au panier.")
        self.refresh() # Rafraîchir la liste pour voir l'exemplaire passer en "Emprunté"

    def open_pdf(self):
        if self.pdf_path: 
            webbrowser.open_new(self.pdf_path)