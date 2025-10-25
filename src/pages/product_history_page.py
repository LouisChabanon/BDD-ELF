import customtkinter as ctk
from components.bandeau_sup import Band_sup
from utils.session import get_session
from database.queries import get_product_history, get_product_by_id

class ProductHistoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product_id = None
        self.product_name = "N/A"

        # Couleur de fond principale
        self.configure(fg_color="#F9F7F0")

        # Ajout du bandeau supérieur
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Conteneur principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Titre de la page
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Historique du produit",
            font=("Helvetica", 24, "bold"),
            text_color="#4A4947"
        )
        self.title_label.pack(pady=(10, 20))

        # Cadre pour la liste de l'historique
        self.history_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.history_frame.pack(fill="both", expand=True)

        # Bouton "Retour"
        self.back_button = ctk.CTkButton(
            self,
            text="Retour",
            font=("Helvetica", 14),
            command=self.go_back
        )
        self.back_button.place(relx=0.95, rely=0.95, anchor="se")

    def set_product_id(self, product_id):
        """Définit l'ID du produit à afficher."""
        self.product_id = product_id
        self.product_name = "N/A" # Réinitialiser

    def refresh(self):
        """Actualise la page et charge l'historique du produit."""
        
        # 1. Vérifier la session utilisateur
        if get_session() is None:
            self.controller.show_page("LoginPage")
            return
            
        # 2. Actualiser le bandeau
        self.bandeau.refresh()
        
        # 3. Vider l'ancien contenu
        for widget in self.history_frame.winfo_children():
            widget.destroy()
            
        # 4. Vérifier l'ID du produit
        if not self.product_id:
            self.title_label.configure(text="Erreur : Aucun produit sélectionné")
            ctk.CTkLabel(self.history_frame, text="Veuillez retourner et sélectionner un produit.").pack(pady=20)
            return

        # 5. Récupérer les données du produit (pour le nom)
        product_data = get_product_by_id(self.product_id)
        if not product_data:
            self.title_label.configure(text=f"Erreur : Produit ID {self.product_id} non trouvé")
            return
        
        self.product_name = product_data.get('nom_materiel', 'Nom Inconnu')
        self.title_label.configure(text=f"Historique pour : {self.product_name} (ID: {self.product_id})")
        
        # 6. Récupérer l'historique
        history_list = get_product_history(self.product_id)
        print(history_list)
        
        # 7. Afficher l'historique ou un message
        if not history_list:
            ctk.CTkLabel(self.history_frame, text="Aucun historique d'emprunt pour ce matériel.", font=("Helvetica", 16)).pack(pady=20)
            return

        for item in history_list:
            # Créer un cadre pour chaque entrée
            entry_frame = ctk.CTkFrame(self.history_frame, border_width=1, corner_radius=5)
            entry_frame.pack(fill="x", expand=True, padx=10, pady=5)
            
            date_rendu = item.get('date_rendu', 'Date inconnue')
            user_name = f"{item.get('prenom', 'Utilisateur')} {item.get('nom', 'Inconnu')}"
            motif = item.get('motif', 'Non spécifié')
            
            label_text = f"Rendu le: {date_rendu}  |  Par: {user_name}  |  Motif: {motif}"
            ctk.CTkLabel(entry_frame, text=label_text, font=("Helvetica", 14)).pack(anchor="w", padx=10, pady=10)

    def go_back(self):
            self.controller.show_page("MainPage")