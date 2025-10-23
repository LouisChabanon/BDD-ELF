import customtkinter as ctk
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.register_page import RegisterPage
from pages.product_page import ProductPage
from pages.user_page import UserPage

class AppController(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Base de données ELF")
        self.geometry("1280x720")
        
        # Dictionnaire pour stocker les pages
        self.pages = {}

        # Conteneur pour empiler les pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self._init_pages()
        self.show_page("LoginPage")

    def _init_pages(self):
        self.pages["LoginPage"] = LoginPage(self.container, self)
        self.pages["MainPage"] = MainPage(self.container, self)
        self.pages["RegisterPage"] = RegisterPage(self.container, self)
        self.pages["ProductPage"] = ProductPage(self.container, self)
        self.pages["UserPage"] = UserPage(self.container, self)

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        

    def show_page(self, page_name):
        page = self.pages[page_name]

        if hasattr(page, 'refresh'):
            page.refresh()
        page.tkraise()
