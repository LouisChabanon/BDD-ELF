import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from utils.session import get_cart, remove_from_cart

class PanierFrame(ctk.CTkFrame):
    """Panneau latéral droit pour le panier."""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white", corner_radius=10)
        self.controller = controller
        self.pack_propagate(False)

        # Titre
        title = ctk.CTkLabel(self, text="🛒 Panier", font=("Helvetica", 20, "bold"))
        title.pack(pady=(15, 10))

        # Bouton de validation (toujours en bas)
        self.validate_btn = ctk.CTkButton(self, text="Valider mes emprunts", command=lambda: controller.show_page("ConfirmRentPage"))
        self.validate_btn.pack(side="bottom", pady=20, padx=20)

        # --- Mise en place du Scroll (Canvas) ---
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="white")

        # Configuration dynamique de la zone de scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # On garde l'ID de la fenêtre pour pouvoir la manipuler si besoin
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Ajustement automatique de la largeur du contenu au canvas
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True, padx=10)

        # --- Gestion du Scroll ---
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        self.refresh()

    def _on_canvas_configure(self, event):
        """Force le contenu interne à prendre toute la largeur du canvas."""
        self.canvas.itemconfig(self.window_id, width=event.width)

    def _on_mousewheel(self, event):
        """Défilement seulement si le contenu dépasse la taille du canvas."""
        # On vérifie si la hauteur du contenu est supérieure à la hauteur visible
        if self.scrollable_frame.winfo_height() > self.canvas.winfo_height():
            if event.num == 4 or (hasattr(event, 'delta') and event.delta > 0):
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5 or (hasattr(event, 'delta') and event.delta < 0):
                self.canvas.yview_scroll(1, "units")

    def refresh(self):
        """Met à jour l'affichage du panier."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        cart_products = get_cart()

        if not cart_products:
            # Réinitialiser la position du scroll à 0 quand on vide le panier
            self.canvas.yview_moveto(0)
            
            # Afficher le message
            empty_label = ctk.CTkLabel(self.scrollable_frame, text="Votre panier est vide.", text_color="gray")
            # Utilisation de expand=True pour que le label occupe l'espace et ne bouge pas de façon erratique
            empty_label.pack(pady=100, padx=10, fill="both", expand=True)
            
            # Désactiver le bouton de validation si le panier est vide
            self.validate_btn.configure(state="disabled")
            return

        self.validate_btn.configure(state="normal")
        
        # Génération de la liste
        total_items = len(cart_products)
        for i, item in enumerate(cart_products):
            # ... (Ton code de création des items reste identique)
            item_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            
            ctk.CTkButton(
                item_container,
                text="X",
                command=lambda i=item: self.delete_from_cart(i),
                width=28, height=28
            ).pack(side="right", padx=(10, 5))

            text_container = ctk.CTkFrame(item_container, fg_color="transparent")
            text_container.pack(side="left", fill="x", expand=True, padx=10)

            ctk.CTkLabel(text_container, text=item.get('nom_materiel', '...'), font=("Helvetica", 14, "bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(text_container, text=item.get('lieu_rangement', '...'), font=("Helvetica", 12), text_color="gray50", anchor="w").pack(fill="x")

            item_container.pack(fill="x", pady=5)

            if i < total_items - 1:
                ctk.CTkFrame(self.scrollable_frame, height=1, fg_color="#E0E0E0").pack(fill="x", padx=10, pady=5)

    def delete_from_cart(self, product):
        remove_from_cart(product)
        self.refresh()
