# src/components/product_card.py

import customtkinter as ctk
from utils.session import add_to_cart
from components.scan_popup import RentValidationPopup

# REMOVED: from database.queries import get_product_availability_count 
# We do not want to import queries here to avoid lag

class ProductCard(ctk.CTkFrame):
    def __init__(self, parent, controller, product: dict):
        super().__init__(parent)
        self.controller = controller
        self.product = product
        
        self.nom = product.get("nom_materiel", "Inconnu")
        self.photo = product.get("photo_materiel", "default")

        self.stock_count = product.get("stock_dispo", 0)

        self.configure(corner_radius=10, border_width=1, fg_color="white", border_color="#D0D0D0", height=80)
        
        # --- Layout Configuration (Horizontal Row) ---
        self.grid_columnconfigure(0, weight=0) # Image
        self.grid_columnconfigure(1, weight=1) # Info (Expands)
        self.grid_columnconfigure(2, weight=0) # Buttons

        # 1. Image (Left)
        self.img_label = ctk.CTkLabel(
            self, 
            text="📷", 
            fg_color="#F0F0F0", 
            corner_radius=5,
            width=60, 
            height=60
        )
        self.img_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
        
        # 2. Info (Center)
        # Title
        self.title_lbl = ctk.CTkLabel(
            self, 
            text=self.nom, 
            font=("Helvetica", 16, "bold"),
            anchor="w"
        )
        self.title_lbl.grid(row=0, column=1, sticky="sw", padx=(0, 10), pady=(10, 0))

        # Stock Availability
        stock_color = "green" if self.stock_count > 0 else "red"
        stock_text = f"✅ {self.stock_count} disponible(s)" if self.stock_count > 0 else "❌ Rupture de stock"
        
        self.lbl_stock = ctk.CTkLabel(
            self, 
            text=stock_text, 
            text_color=stock_color, 
            font=("Helvetica", 12)
        )
        self.lbl_stock.grid(row=1, column=1, sticky="nw", padx=(0, 10), pady=(0, 10))

        # 3. Buttons (Right)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=0, column=2, rowspan=2, padx=15, pady=10)

        # Button: Details
        self.btn_see = ctk.CTkButton(
            self.btn_frame,
            text="Fiche Produit",
            fg_color="transparent",
            border_width=1,
            text_color="gray",
            width=100,
            command=self.open_product_page
        )
        self.btn_see.pack(side="left", padx=5)

        # Button: Rent (Triggers Scan Popup)
        self.btn_rent = ctk.CTkButton(
            self.btn_frame,
            text="Emprunter",
            fg_color="#B17457",
            hover_color="#9C6049",
            width=100,
            state="normal" if self.stock_count > 0 else "disabled",
            command=self.initiate_rent
        )
        self.btn_rent.pack(side="left", padx=5)

    def open_product_page(self):
        page = self.controller.pages["ProductPage"]
        page.set_product_name(self.nom)
        self.controller.show_page("ProductPage")

    def initiate_rent(self):
        # Open the Popup to scan the specific item
        RentValidationPopup(self, self.nom, self.confirm_rent)

    def confirm_rent(self, item):
        add_to_cart(item)
        self.controller.show_page("MainPage")