import customtkinter as ctk
from utils.session import get_session

class Band_sup(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user = None      

        # Couleurs optionnelles 
        self.configure(fg_color="#80276C", height=60)
        
        # Grille flexible
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        self.user_button = None
        self.refresh()


        # Bouton Ajouter objet 
        self.add_button = ctk.CTkButton(self, text="Ajouter objet", font=("Helvetica", 16), fg_color="#BB2A89", text_color="white", command=self.add_page)
        self.add_button.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        # Bouton Rendre
        self.return_button = ctk.CTkButton(self, text="Rendre", font=("Helvetica", 16), fg_color="#BB2A89", text_color="white", command=self.return_page)
        self.return_button.grid(row=0, column=2, sticky="e", padx=20, pady=10)

    def refresh(self):
        if hasattr(self, 'user_button') and self.user_button:
            self.user_button.destroy()
        
        self.user = get_session()
        

        if self.user:
            # Bouton Nom Prénom utilisateur
            print(f"Bandeau supérieur : utilisateur actuel = {self.user}")
            self.user_button = ctk.CTkButton(self, text=f"{self.user['prenom']} {self.user['nom']}", font=("Helvetica", 16, "bold"), fg_color="#BB2A89", text_color="white", width=150, command=lambda: self.controller.show_page("UserPage"))
            self.user_button.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        else:
            # Bouton Connexion
            self.login_button = ctk.CTkButton(self, text="Connexion", font=("Helvetica", 16, "bold"), fg_color="#BB2A89", text_color="white", width=150, command=lambda: self.controller.show_page("LoginPage"))
            self.login_button.grid(row=0, column=0, sticky="w", padx=20, pady=10)

    # Méthodes associées aux boutons 
    def show_user_info(self):
        print(f"Utilisateur connecté : {self.user}")
        

    def add_page(self):
        print("Aller à la page d'ajout d'objet")
        

    def return_page(self):
        print("Aller à la page de rendu d'objet")

        