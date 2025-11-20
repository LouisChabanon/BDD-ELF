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
        self.configure(fg_color="#F9F7F0")

        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Scrollable Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header Info Section
        self.header_frame = ctk.CTkFrame(self.scroll_frame, fg_color="white", corner_radius=10)
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.img_label = ctk.CTkLabel(self.header_frame, text="[IMAGE]", width=100, height=100, fg_color="#eee")
        self.img_label.pack(side="left", padx=20, pady=20)
        
        self.info_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.info_container.pack(side="left", fill="both", expand=True, pady=10)
        
        self.lbl_title = ctk.CTkLabel(self.info_container, text="...", font=("Helvetica", 24, "bold"), anchor="w")
        self.lbl_title.pack(fill="x")
        
        self.lbl_maint = ctk.CTkLabel(self.info_container, text="", font=("Helvetica", 14), anchor="w")
        self.lbl_maint.pack(fill="x", pady=5)

        self.btn_pdf = ctk.CTkButton(self.info_container, text="📄 Notice PDF", width=100, command=self.open_pdf)
        self.btn_pdf.pack(anchor="w", pady=5)

        self.btn_back = ctk.CTkButton(self.header_frame, text="Retour", fg_color="gray", width=100, command=lambda: controller.show_page("MainPage"))
        self.btn_back.pack(side="right", padx=20, anchor="n", pady=20)

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
            ctk.CTkLabel(self.list_container, text="Aucun stock.").pack(pady=20)
            return

        for item in items:
            row = ctk.CTkFrame(self.list_container, fg_color="white", corner_radius=5)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=f"#{item['id_exemplaire']}", font=("Courier", 14, "bold"), width=80).pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(row, text=item.get('lieu_rangement', 'N/A'), width=150).pack(side="left", padx=10)
            
            is_avail = item['is_available']
            status_text = "DISPONIBLE" if is_avail else "EMPRUNTÉ"
            status_color = "#8FBC8F" if is_avail else "#C94C3E"
            
            ctk.CTkLabel(row, text=status_text, text_color=status_color, font=("Helvetica", 12, "bold"), width=100).pack(side="left", padx=10)

            if is_avail:
                # BUTTON CLICK -> OPEN POPUP
                ctk.CTkButton(
                    row, 
                    text="Ajouter au panier", 
                    fg_color="#B17457", 
                    command=lambda i=item: self.initiate_add_to_cart(i)
                ).pack(side="right", padx=20)
            else:
                ctk.CTkButton(row, text="Historique", fg_color="gray", state="disabled").pack(side="right", padx=20)

    def initiate_add_to_cart(self, item):
        # This opens the modal. The item is ONLY added if the modal succeeds.
        RentValidationPopup(self, item['id_exemplaire'], lambda: self.confirm_add_to_cart(item))

    def confirm_add_to_cart(self, item):
        item['nom_materiel'] = self.product_name 
        add_to_cart(item)
        messagebox.showinfo("Succès", f"Exemplaire #{item['id_exemplaire']} ajouté au panier.")

    def handle_spontaneous_scan(self, event):
        code = self.search_entry.get().strip()
        if not code:
            return

        # 1. Check if it matches a generic product name
        details = get_product_details(code) # Attempt by name
        if details:
            self.set_product_name(details['nom_materiel'])
            return

        name_from_id = get_product_name_by_exemplaire_id(code)
        if name_from_id:
            # Redirect to that page
            self.set_product_name(name_from_id)
            # Optional: Highlight the specific row? For now, just showing the list is sufficient per prompt.
        else:
            messagebox.showerror("Erreur", f"Aucun produit ou exemplaire trouvé pour : {code}")

    def open_pdf(self):
        if self.pdf_path: webbrowser.open_new(self.pdf_path)