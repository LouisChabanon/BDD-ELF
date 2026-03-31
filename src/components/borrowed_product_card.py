import customtkinter as ctk
from utils.session import add_to_cart
from components.scan_popup import ReturnValidationPopup
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

class BorrowedProductCard(ctk.CTkFrame):
    def __init__(self, parent, controller, product: dict):
        super().__init__(parent)
        self.controller = controller
        self.product = product
        
        # Données de base
        self.nom = product.get("nom_materiel", "Inconnu")
        self.photo = product.get("photo_materiel", None)
        
        # Données d'emprunt (doivent venir du backend)
        self.prenom = product.get("prenom")
        self.nom_user = product.get("nom")
        self.id_exemplaire = product.get("id_exemplaire")
        self.date_rendu = product.get("date_rendu")
        
        # Stock (non affiché mais conservé pour compatibilité)
        self.stock_count = product.get("stock_dispo", 0)

        # Configuration visuelle
        self.configure(
            corner_radius=10,
            border_width=1,
            fg_color="white",
            border_color="#D0D0D0",
            height=80
        )
        
        # Layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Image
        self.img_label = ctk.CTkLabel(
            self, 
            text="", 
            fg_color="#F0F0F0", 
            corner_radius=5,
            width=60, 
            height=60
        )
        self.img_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
        
        # Titre
        self.title_lbl = ctk.CTkLabel(
            self, 
            text=self.nom, 
            font=("Helvetica", 16, "bold"),
            anchor="w"
        )
        self.title_lbl.grid(row=0, column=1, sticky="sw", padx=(0, 10), pady=(10, 0))

        # Zone infos (anciennement stock)
        self.lbl_stock = ctk.CTkLabel(
            self, 
            text="", 
            font=("Helvetica", 12),
            justify="left"
        )
        self.lbl_stock.grid(row=1, column=1, sticky="nw", padx=(0, 10), pady=(0, 10))

        # Frame boutons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=0, column=2, rowspan=2, padx=15, pady=10)

        # Bouton fiche produit
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

        # Bouton rendre
        self.btn_rent = ctk.CTkButton(
            self.btn_frame,
            text="Rendre",
            fg_color="#B17457",
            hover_color="#9C6049",
            width=100,
            command=lambda: controller.show_page("MainPage")
        )
        self.btn_rent.pack(side="left", padx=5)

        # Initialisation affichage
        self.update_stock_display(self.stock_count)

        # Chargement image
        if self.photo and self.photo != "default":
            threading.Thread(target=self.load_image_thread, daemon=True).start()
            
    def update_stock_display(self, current_stock):
        """
        Affiche uniquement les infos d'emprunt
        """
        # Sécurisation minimale (évite crash si champ manquant)
        prenom = self.prenom if self.prenom else "?"
        nom = self.nom_user if self.nom_user else "?"
        id_ex = self.id_exemplaire if self.id_exemplaire else "?"
        date = self.date_rendu if self.date_rendu else "?"

        info_text = (
            f"Emprunté par : {prenom} {nom}\n"
            f"ID exemplaire : {id_ex}\n"
            f"Date de rendu : {date}"
        )

        self.lbl_stock.configure(
            text=info_text,
            text_color="black",
            justify="left"
        )

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
        ReturnValidationPopup(self, self.nom, self.confirm_rent)

    def confirm_rent(self, item):
        """Action déclenchée après validation du scan dans la popup"""
        # 1. Ajoute au panier (logique métier)
        add_to_cart(item)
        
        # 2. Feedback immédiat : on baisse le stock visuel tout de suite 
        # pour que l'utilisateur voit que son action a fonctionné.
        self.update_stock_display(self.stock_count - 1)
        
        # 3. On retourne sur la page principale (qui devrait se rafraîchir totalement idéalement)
        self.controller.show_page("MainPage")