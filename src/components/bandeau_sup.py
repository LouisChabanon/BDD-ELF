import customtkinter as ctk

class Band_sup(ctk.CTkFrame):
    def __init__(self, parent, controller, username="Utilisateur"):
        super().__init__(parent)
        self.controller = controller
        self.username = username

        # Couleurs optionnelles 
        self.configure(fg_color="#80276C", height=60)
        
        # Grille flexible
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        # Bouton Nom Prénom utilisateur
        self.user_button = ctk.CTkButton(self, text=f"{self.username}", font=("Helvetica", 16, "bold"), fg_color="#BB2A89", text_color="white", width=150, command=self.show_user_info)
        self.user_button.grid(row=0, column=0, sticky="w", padx=20, pady=10)

        # Bouton Ajouter objet 
        self.add_button = ctk.CTkButton(self, text="Ajouter objet", font=("Helvetica", 16), fg_color="#BB2A89", text_color="white", command=self.add_page)
        self.add_button.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        # Bouton Rendre
        self.return_button = ctk.CTkButton(self, text="Rendre", font=("Helvetica", 16), fg_color="#BB2A89", text_color="white", command=self.return_page)
        self.return_button.grid(row=0, column=2, sticky="e", padx=20, pady=10)

    # Méthodes associées aux boutons 
    def show_user_info(self):
        print(f"Utilisateur connecté : {self.username}")
        

    def add_page(self):
        print("Aller à la page d'ajout d'objet")
        

    def return_page(self):
        print("Aller à la page de rendu d'objet")

        