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

# --- CHARGEMENT DES VARIABLES D'ENVIRONNEMENT ---
dotenv.load_dotenv()
SAMBA_SRV = os.getenv("SAMBA_SRV")
SAMBA_USER = os.getenv("SAMBA_USER")
SAMBA_PASSWORD = os.getenv("SAMBA_PASSWORD")

class ProductCard(ctk.CTkFrame):
    def __init__(self, parent, controller, product: dict):
        super().__init__(parent)
        self.controller = controller
        self.product = product
        
        # Données de base extraites du dictionnaire 'product'
        self.nom = product.get("nom_materiel", "Inconnu")
        self.photo = product.get("photo_materiel", None)
        
        # Stock initial (sera mis à jour par update_stock_display plus bas)
        self.stock_count = product.get("stock_dispo", 0)

        # Configuration visuelle du cadre (Frame)
        self.configure(corner_radius=10, border_width=1, fg_color="white", border_color="#D0D0D0", height=80)
        
        # --- CONFIGURATION DU LAYOUT (Grille à 3 colonnes) ---
        self.grid_columnconfigure(0, weight=0) # Colonne Image
        self.grid_columnconfigure(1, weight=1) # Colonne Infos (s'étire)
        self.grid_columnconfigure(2, weight=0) # Colonne Boutons

        # 1. WIDGET IMAGE (Vide par défaut, chargé via thread)
        self.img_label = ctk.CTkLabel(
            self, 
            text="📷", 
            fg_color="#F0F0F0", 
            corner_radius=5,
            width=60, 
            height=60
        )
        self.img_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
        
        # 2. WIDGET TITRE
        self.title_lbl = ctk.CTkLabel(
            self, 
            text=self.nom, 
            font=("Helvetica", 16, "bold"),
            anchor="w"
        )
        self.title_lbl.grid(row=0, column=1, sticky="sw", padx=(0, 10), pady=(10, 0))

        # 3. WIDGET STOCK (L'élément critique qui doit changer)
        # On crée le widget SANS texte. Le texte sera mis par update_stock_display()
        self.lbl_stock = ctk.CTkLabel(
            self, 
            text="", 
            font=("Helvetica", 12)
        )
        self.lbl_stock.grid(row=1, column=1, sticky="nw", padx=(0, 10), pady=(0, 10))

        # 4. CADRE POUR LES BOUTONS
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=0, column=2, rowspan=2, padx=15, pady=10)

        # BOUTON DETAILS
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

        # BOUTON EMPRUNTER
        # On ne définit pas 'state' ici, car il dépend du stock
        self.btn_rent = ctk.CTkButton(
            self.btn_frame,
            text="Emprunter",
            fg_color="#B17457",
            hover_color="#9C6049",
            width=100,
            command=self.initiate_rent
        )
        self.btn_rent.pack(side="left", padx=5)

        # --- INITIALISATION DE L'AFFICHAGE ---
        # On appelle notre fonction magique pour afficher le stock correct dès le départ
        self.update_stock_display(self.stock_count)

        # Lancement du chargement de l'image en arrière-plan (pour ne pas figer l'interface)
        if self.photo and self.photo != "default":
            threading.Thread(target=self.load_image_thread, daemon=True).start()

    def update_stock_display(self, current_stock):
        """
        C'EST CETTE FONCTION QUI RÉSOUT TON PROBLÈME.
        Elle peut être appelée n'importe quand pour rafraîchir la carte.
        """
        self.stock_count = current_stock
        
        # Logique de décision : on définit le texte et la couleur selon le stock
        if self.stock_count > 0:
            stock_color = "green"
            stock_text = f"✅ {self.stock_count} disponible(s)"
            button_state = "normal"  # On active le bouton
        else:
            stock_color = "red"
            stock_text = "❌ Rupture de stock"
            button_state = "disabled" # On désactive le bouton

        # On APPLIQUE les changements aux widgets qui existent déjà dans le __init__
        self.lbl_stock.configure(text=stock_text, text_color=stock_color)
        self.btn_rent.configure(state=button_state)

    def load_image_thread(self):
        """Télécharge l'image depuis le serveur Samba sans bloquer l'UI"""
        max_retries = 20
        attempts = 0
        # Attend que la connexion SMB globale soit prête
        while not self.controller.smb_connected:
            if self.controller.smb_error: return
            if attempts > max_retries: return
            time.sleep(0.5)
            attempts += 1

        try:
            # Nettoyage du chemin de fichier pour Windows/Samba
            clean_filename = self.photo.replace("/", "\\").lstrip("\\")
            full_path = fr"\\{SAMBA_SRV}\{clean_filename}"
            
            with smbclient.open_file(full_path, mode="rb") as file:
                file_data = file.read()
            
            # Conversion des données binaires en image utilisable par CustomTkinter
            img_stream = io.BytesIO(file_data)
            pil_image = Image.open(img_stream)
            ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(60, 60))
            
            # Commande de mise à jour sur le thread principal (obligatoire pour Tkinter)
            self.after(0, self.update_image_label, ctk_image)
        except Exception as e:
            print(f"Image load error for {self.nom}: {e}")

    def update_image_label(self, ctk_image):
        """Met à jour le label image une fois chargée"""
        self.img_label.configure(image=ctk_image, text="")

    def open_product_page(self):
        """Transmet le nom du produit à la page de détails et change de vue"""
        page = self.controller.pages["ProductPage"]
        page.set_product_name(self.nom)
        self.controller.show_page("ProductPage")

    def initiate_rent(self):
        """Ouvre la popup de scan pour valider l'emprunt"""
        RentValidationPopup(self, self.nom, self.confirm_rent)

    def confirm_rent(self, item):
        """Action déclenchée après validation du scan dans la popup"""
        # 1. Ajoute au panier (logique métier)
        add_to_cart(item)
        
        # 2. Feedback immédiat : on baisse le stock visuel tout de suite 
        # pour que l'utilisateur voit que son action a fonctionné.
        self.update_stock_display(self.stock_count - 1)
        
        # 3. On retourne sur la page principale (qui devrait se rafraîchir totalement idéalement)
        self.controller.show_page("MainPage")