import customtkinter as ctk
from pages.login_page import LoginPage
from pages.main_page import MainPage

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
        
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()