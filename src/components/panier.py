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

        # 1. Packer le bouton du bas D'ABORD
        # Il réserve sa place en bas.
        self.validate_btn = ctk.CTkButton(self, text="Valider mes emprunts", command=lambda: controller.show_page("ConfirmRentPage"))
        self.validate_btn.pack(side="bottom", pady=20, padx=20)

        # --- Mise en place du Scroll (Canvas) ---
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="white")

        # Redimensionnement dynamique de la zone de scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 2. Packer la scrollbar et le canvas EN DERNIER
        # Le canvas prendra tout l'espace restant.
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True, padx=10)

        # --- Scroll à la molette / trackpad ---
        def _on_mousewheel(event):
            # Windows / macOS
            self.canvas.yview_scroll(-int(event.delta / 120), "units")

        def _on_linux_scroll(event):
            # Linux : bouton 4 = haut, bouton 5 = bas
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

        # Lier les événements de scroll au canvas
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)      # Windows / macOS
        self.canvas.bind_all("<Button-4>", _on_linux_scroll)       # Linux scroll up
        self.canvas.bind_all("<Button-5>", _on_linux_scroll)       # Linux scroll down

        # Chargement initial des données
        self.refresh()


    def refresh(self):
        """Met à jour l'affichage du panier en fonction du contenu actuel."""
        
        # 1. Nettoyer l'affichage existant
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 2. Récupérer les données à jour
        cart_products = get_cart()

        # 3. Si le panier est vide, afficher un message
        if not cart_products:
            empty_label = ctk.CTkLabel(self.scrollable_frame, text="Votre panier est vide.", text_color="gray")
            empty_label.pack(pady=20, padx=10)
            return

        # 4. Générer la liste simple
        total_items = len(cart_products)
        for i, item in enumerate(cart_products):
            
            nom_text = item.get('nom_materiel', 'Nom inconnu')
            loc_text = item.get('lieu_rangement', 'Lieu inconnu')

            item_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            
            ctk.CTkButton(
                item_container,
                text="X",
                command=lambda i=item: self.delete_from_cart(i),
                width=28,
                height=28,
                anchor="l"
            ).pack(side="right", anchor="center", padx=(10, 5))

            text_container = ctk.CTkFrame(item_container, fg_color="transparent")
            text_container.pack(side="left", fill="x", expand=True, padx=10)

            # Label Nom
            ctk.CTkLabel(
                text_container, 
                text=nom_text, 
                font=("Helvetica", 14, "bold"),
                anchor="w"
            ).pack(fill="x", padx=10, pady=(5, 0))

            # Label Emplacement
            ctk.CTkLabel(
                text_container, 
                text=loc_text, 
                font=("Helvetica", 12), 
                text_color="gray50",
                anchor="w"
            ).pack(fill="x", padx=10, pady=(0, 5))

            item_container.pack(fill="x", pady=5)

            # Ajouter un séparateur (sauf après le dernier item)
            if i < total_items - 1:
                separator = ctk.CTkFrame(self.scrollable_frame, height=1, fg_color="#E0E0E0")
                separator.pack(fill="x", padx=10, pady=5)
        
    def delete_from_cart(self, product):
        remove_from_cart(product)
        self.refresh()
