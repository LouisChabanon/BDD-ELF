import customtkinter as ctk
from database.queries import get_user_by_id
from database.queries import return_product

class RentValidationPopup(ctk.CTkToplevel):
    def __init__(self, parent, product_name, on_success_callback):
        super().__init__(parent)
        self.product_name = product_name
        self.on_success = on_success_callback
        
        self.title("Validation de l'emprunt")
        self.geometry("450x250")
        self.resizable(False, False)
        
        # Modal behavior
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color="#F9F7F0")
        
        # UI
        ctk.CTkLabel(
            self, 
            text=f"Vous voulez emprunter : {self.product_name}", 
            font=("Helvetica", 16, "bold")
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            self, 
            text="Veuillez scanner le code-barre de l'exemplaire\nque vous avez en main pour confirmer.", 
            font=("Helvetica", 14)
        ).pack(pady=5)
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Scanner l'exemplaire ici...", width=300)
        self.entry.pack(pady=15)
        self.entry.bind("<Return>", self.validate)
        
        self.status_label = ctk.CTkLabel(self, text="", font=("Helvetica", 12, "bold"))
        self.status_label.pack(pady=5)
        
        self.entry.focus_set()

    def validate(self, event=None):
        from database.queries import validate_scan_match, get_product_details
        
        scanned_code = self.entry.get().strip()
        if not scanned_code:
            return

        # Validate against DB
        is_valid, message = validate_scan_match(scanned_code, self.product_name)
        
        if is_valid:
            self.status_label.configure(text="✅ Code valide ! Ajout au panier...", text_color="green")
            self.after(800, lambda: self.finalize(scanned_code))
        else:
            self.status_label.configure(text=f"❌ {message}", text_color="red")
            self.entry.delete(0, 'end')

    def finalize(self, scanned_id):
        # We need to construct the item object to add to cart
        # We know the ID and the Name. We can fetch the rest or construct it.
        item = {
            "id_exemplaire": int(scanned_id),
            "nom_materiel": self.product_name,
            "lieu_rangement": "Inconnu (Scan)" # Simplified
        }
        self.on_success(item)
        self.destroy()

class ReturnValidationPopup(ctk.CTkToplevel):
    def __init__(self, parent, product_name, on_success_callback):
        super().__init__(parent)
        self.product_name = product_name
        self.on_success = on_success_callback
        
        self.title("Validation du rendu")
        self.geometry("450x250")
        self.resizable(False, False)
        
        # Modal behavior
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color="#F9F7F0")
        
        # UI
        ctk.CTkLabel(
            self, 
            text=f"Vous voulez rendre : {self.product_name}", 
            font=("Helvetica", 16, "bold")
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            self, 
            text="Veuillez scanner le code-barre de l'exemplaire\nque vous avez en main pour confirmer.", 
            font=("Helvetica", 14)
        ).pack(pady=5)
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Scanner l'exemplaire ici...", width=300)
        self.entry.pack(pady=15)
        self.entry.bind("<Return>", self.validate)
        
        self.status_label = ctk.CTkLabel(self, text="", font=("Helvetica", 12, "bold"))
        self.status_label.pack(pady=5)
        
        self.entry.focus_set()

    def validate(self, event=None):
        """Méthode déclenchée quand on appuie sur Entrée ou sur le bouton."""
        code_barre = self.username_entry.get().strip()

        if not code_barre:
            self.error_label.configure(text="Veuillez scanner ou saisir un code barre.")
            return

        try:
            success = return_product(code_barre)

            if success:
                self.error_label.configure(
                    text=f"Matériel '{code_barre}' rendu avec succès ✅",
                    text_color="green"
                )
            else:
                self.error_label.configure(
                    text="Aucun emprunt actif trouvé pour ce matériel.",
                    text_color="maroon"
                )

        except Exception as e:
            self.error_label.configure(
                text=f"Erreur lors du rendu : {str(e)}",
                text_color="maroon"
            )



