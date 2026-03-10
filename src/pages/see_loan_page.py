import customtkinter as ctk
from components.bandeau_sup import Band_sup
from utils.session import set_session
from utils.session import get_session
from database.queries import get_user_by_id
from database.queries import get_borrowed_items


class SeeLoanPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Couleur de fond principale
        self.configure(fg_color="#F9F7F0")

        # Ajout du bandeau supérieur (commun à toutes les pages)
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")
        self.bandeau.refresh()

        #Liste scrollable
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=20, pady=20)

    def load_borrowed(self):
        session = get_session()
        id_user = session["id_personnel"]
        items = get_borrowed_items(id_user)

        self.render_list(items)
    
    def render_list(self, items):
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        if not items:
            ctk.CTkLabel(self.scroll_container, text="Aucun objet emprunté.").pack(pady=20)
            return

        for item in items:
            label = ctk.CTkLabel(
                self.scroll_container,
                text=f"{item['nom_materiel']} - Retour le {item['date_retour_prevue']}"
            )
            label.pack(fill="x", pady=5, padx=5)
    
    def refresh(self, args=None):
        try:
            self.load_borrowed()
        except Exception as e:
            print("Erreur refresh SeeLoanPage :", e)


