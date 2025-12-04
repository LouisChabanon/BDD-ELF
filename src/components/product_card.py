import customtkinter as ctk
from utils.session import add_to_cart
from components.scan_popup import RentValidationPopup
import threading
import os
import io
import dotenv
from PIL import Image
import smbclient
import time

dotenv.load_dotenv()
SAMBA_SRV = os.getenv("SAMBA_SRV")
SAMBA_USER = os.getenv("SAMBA_USER")
SAMBA_PASSWORD = os.getenv("SAMBA_PASSWORD")

class ProductCard(ctk.CTkFrame):
    def __init__(self, parent, controller, product: dict):
        super().__init__(parent)
        self.controller = controller
        self.product = product
        
        self.nom = product.get("nom_materiel", "Inconnu")
        self.photo = product.get("photo_materiel", None)

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

        if self.photo and self.photo != "default":
            threading.Thread(target=self.load_image_thread, daemon=True).start()

    def load_image_thread(self):
        """
        Waits for global SMB connection, then fetches image.
        """
        # 1. WAIT FOR CONNECTION
        max_retries = 20  # Wait max 10 seconds
        attempts = 0
        
        while not self.controller.smb_connected:
            if self.controller.smb_error:
                print("SMB Failed globally. Stopping image load.")
                return
            
            if attempts > max_retries:
                print("Timed out waiting for SMB connection.")
                return

            time.sleep(0.5)
            attempts += 1

        # 2. FETCH IMAGE
        try:

            # Ensure slashes are correct for Windows SMB (Backslashes)
            clean_filename = self.photo.replace("/", "\\").lstrip("\\")
            
            full_path = fr"\\{SAMBA_SRV}\{clean_filename}"

            with smbclient.open_file(full_path, mode="rb") as file:
                file_data = file.read()

            img_stream = io.BytesIO(file_data)
            pil_image = Image.open(img_stream)
            
            # Keep aspect ratio roughly
            ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(60, 60))

            # Update UI on main thread
            self.after(0, self.update_image_label, ctk_image)

        except Exception as e:
            print(f"Image load error for {full_path}: {e}")
            pass

    def update_image_label(self, ctk_image):
        self.img_label.configure(image=ctk_image, text="")


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