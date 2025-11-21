import customtkinter as ctk
from utils.session import get_session

class Band_sup(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user = None      

        # Couleurs optionnelles 
        self.configure(fg_color="#B17457", height=60)
        
        # Grille flexible
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        self.user_button = None

        # Bouton Accueil 
        self.home_button = ctk.CTkButton(self,text="🏠",width=20,height=20,fg_color="#B17457",hover_color="#9C6049",font=("Helvetica", 20),command=lambda: controller.show_page("MainPage"))


        # Bouton "Ajouter objet"
        self.add_button = ctk.CTkButton(
            self, 
            text="Ajouter objet", 
            command=lambda: self.controller.show_page("AjouterObjetPage")
,
        )
        self.add_button.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        # Bouton "Rendre"
        self.return_button = ctk.CTkButton(
            self, 
            text="Rendre", 
            command=self.return_page,
        )
        self.return_button.grid(row=0, column=2, sticky="e", padx=20, pady=10)

    def refresh(self, args=None):
        """Met à jour le bouton utilisateur ou connexion."""
        if hasattr(self, 'user_button') and self.user_button:
            self.user_button.destroy()
        
        self.user = get_session()

        if self.user:
            self.home_button.grid(row=0, column=3, sticky="e", padx=10, pady=10)
        else:
            self.home_button.grid_forget()

        # Style du bouton utilisateur / connexion
        button_style = {
            "font": ("Helvetica", 16, "bold"),
            "fg_color": "#B17457",
            "text_color": "#F9F7F0",
            "border_color": "#D8D2C2",
            "border_width": 2,
            "hover_color": "#9C6049",
            "corner_radius": 8,
            "width": 150,
            "height": 35
        }

        if self.user:
            # Bouton "Nom Prénom" utilisateur
            self.user_button = ctk.CTkButton(
                self,
                text=f"{self.user['prenom']} {self.user['nom']}",
                command=lambda: self.controller.show_page("UserPage"),
                **button_style
            )
        else:
            # Bouton "Connexion"
            self.user_button = ctk.CTkButton(
                self,
                text="Connexion",
                command=lambda: self.controller.show_page("LoginPage"),
                **button_style
            )

        self.user_button.grid(row=0, column=0, sticky="w", padx=20, pady=10)

    # Méthodes associées aux boutons 
        
    def add_page(self):
        print("Aller à la page d'ajout d'objet")
        

    def return_page(self):
        """Redirige vers la page de rendu du matériel"""
        self.controller.show_page("ReturnPage")
        print("Aller à la page de rendu d'objet")

        