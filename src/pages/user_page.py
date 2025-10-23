import customtkinter as ctk
from components.bandeau_sup import Band_sup
from utils.session import get_session, clear_session

class UserPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


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

        # Bouton "Voir mes réservations"
        self.resa_button = ctk.CTkButton(
            self.main_frame,
            text="Voir mes réservations",
            font=("Helvetica", 16),
            command=lambda: self.controller.show_page("ReservationsPage")
        )
        self.resa_button.pack(pady=10)

        # Bouton "Voir mes emprunts en cours"
        self.emprunts_button = ctk.CTkButton(
            self.main_frame,
            text="Voir mes emprunts en cours",
            font=("Helvetica", 16),
            command=lambda: self.controller.show_page("EmpruntsPage")
        )
        self.emprunts_button.pack(pady=10)

        # Bouton de déconnexion
        self.logout_button = ctk.CTkButton(
            self.main_frame,
            text="Se déconnecter",
            font=("Helvetica", 16),
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self.logout
        )
        self.logout_button.pack(pady=(30, 10))

        # Bouton retour (en bas à droite)
        self.back_button = ctk.CTkButton(
            self,
            text="Retour",
            font=("Helvetica", 14),
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