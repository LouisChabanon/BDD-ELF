import customtkinter as ctk
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.register_page import RegisterPage
from pages.product_page import ProductPage
from pages.user_page import UserPage
from pages.product_history_page import ProductHistoryPage
from pages.modif_product_page import ModifierProduitPage
import dotenv
import os
import threading
import smbclient

dotenv.load_dotenv()
SMB_SRV = os.getenv("SAMBA_SRV")
SMB_USER = os.getenv("SAMBA_USER")
SMB_PASSWORD = os.getenv("SAMBA_PASSWORD")


class AppController(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Base de données ELF")
        self.geometry("1280x720")
        

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("src/assets/theme.json")

        self.smb_connected = False
        self.smb_error = None
        threading.Thread(target=self.connect_to_smb, daemon=True).start()

        self.pages = {}
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self._init_pages()
        self.show_page("LoginPage")

    def connect_to_smb(self):
        try:
            print(f"Connexion au serveur Samba {SMB_SRV}...")
            smbclient.register_session(
                SMB_SRV,
                username=SMB_USER,
                password=SMB_PASSWORD
            )
            print("Connexion au serveur Samba réussie.")
        except Exception as e:
            print(f"Erreur de connexion au serveur Samba : {e}")
            exit(1)

        
    def _init_pages(self):
        self.pages["LoginPage"] = LoginPage(self.container, self)
        self.pages["MainPage"] = MainPage(self.container, self)
        self.pages["RegisterPage"] = RegisterPage(self.container, self)
        self.pages["ProductPage"] = ProductPage(self.container, self)
        self.pages["UserPage"] = UserPage(self.container, self)
        self.pages["ProductHistoryPage"] = ProductHistoryPage(self.container, self)
        self.pages["ModifierProduitPage"] = ModifierProduitPage(self.container, self)

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_page(self, page_name):
        try:
            page = self.pages[page_name]
            if hasattr(page, 'refresh'):
                page.refresh()
            page.tkraise()
        except KeyError:
            print(f"Erreur : La page {page_name} n'existe pas")

    # Helper to show product page by ID (Spontaneous scan from other pages)
    def show_product_page(self, product_id_or_name):
        page = self.pages["ProductPage"]
        
        # Determine if it is an ID (int/digits) or a Name (string)
        if str(product_id_or_name).isdigit():
            # It's an ID, logic handles finding the name
            # However, ProductPage logic relies on set_product_name mostly now.
            # We should look up the name here or in the page.
            from database.queries import get_product_name_by_exemplaire_id
            name = get_product_name_by_exemplaire_id(product_id_or_name)
            if name:
                page.set_product_name(name)
        else:
            # It's a Name
            page.set_product_name(product_id_or_name)
            
        self.show_page("ProductPage")

    def show_product_history_page(self, product_id: str):
        page = self.pages["ProductHistoryPage"]
        page.set_product_id(product_id)
        self.show_page("ProductHistoryPage")
