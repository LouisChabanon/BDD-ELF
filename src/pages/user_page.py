import customtkinter as ctk
from components.bandeau_sup import Band_sup
from utils.session import get_session, clear_session

class UserPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
         # Couleur de fond principale
        self.configure(fg_color="#F9F7F0")

        # Ajout du bandeau supérieur (commun à toutes les pages)
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")
        self.bandeau.refresh()

        # Conteneur principal pour le contenu
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True)


        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Helvetica", 22, "bold")
        )
        self.name_label.pack(pady=(40, 20))

        # Nom de l'utilisateur
        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Helvetica", 22, "bold"),
            text_color="#2E2E2E"
        )
        self.name_label.pack(pady=(40, 20))

        # Style commun des boutons principaux
        button_style = {
            "font": ("Helvetica", 16),
            "width": 220,
            "height": 40,
            "fg_color": "#B17457",
            "hover_color": "#9C6049",
            "text_color": "white"
        }

        # Bouton "Voir mes réservations"
        self.resa_button = ctk.CTkButton(
            self.main_frame,
            text="Voir mes réservations",
            command=lambda: self.controller.show_page("ReservationsPage"),
            **button_style
        )
        self.resa_button.pack(pady=10)

        # Bouton "Voir mes emprunts"
        self.emprunts_button = ctk.CTkButton(
            self.main_frame,
            text="Voir mes emprunts en cours",
            command=lambda: self.controller.show_page("EmpruntsPage"),
            **button_style
        )
        self.emprunts_button.pack(pady=10)

        # Bouton "Se déconnecter"
        self.logout_button = ctk.CTkButton(
            self.main_frame,
            text="Se déconnecter",
            command=self.logout,
            **button_style
        )
        self.logout_button.pack(pady=(30, 10))

        # Bouton "Retour"
        self.back_button = ctk.CTkButton(
            self,
            text="Retour",
            font=("Helvetica", 14),
            width=100,
            height=30,
            fg_color="#B17457",
            hover_color="#9C6049",
            text_color="white",
            command=lambda: controller.show_page("MainPage")
        )
        self.back_button.place(relx=0.95, rely=0.95, anchor="se")
    def refresh(self):
        """Actualise les informations de la page utilisateur"""
        session = get_session()
        if session:
            fullname = f"{session.get('prenom', 'Utilisateur')} {session.get('nom', '')}"
            self.name_label.configure(text=fullname)
            print(f"Page utilisateur actualisée pour : {fullname}")
        else:
            print("Aucun utilisateur connecté lors de l'actualisation, redirection vers la page de connexion.")
            self.controller.show_page("LoginPage")

    def logout(self):
        """Déconnexion de l'utilisateur"""
        clear_session()
        self.controller.show_page("LoginPage")