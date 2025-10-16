import customtkinter as ctk

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Titre de la page
        self.label = ctk.CTkLabel(self, text="Inscription à la base de données ELF", font=("Helvetica", 24, "bold"))
        self.label.pack(pady=40)

        # Identifiant
        self.username_label = ctk.CTkLabel(self, text="Scanner votre carte ou entrer votre identifiant ENSAM: ", font=("Helvetica", 16))
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self, width=300, font=("Helvetica", 16))
        self.username_entry.pack(pady=10)

        # Fonction pour gérer l'appui sur la touche "Entrée"
        self.username_entry.bind("<Return>", self.register)

        # Bouton d'inscription (aucune validation pour l'instant)
        self.register_button = ctk.CTkButton(self, text="S'inscrire", font=("Helvetica", 16), command=self.register)
        self.register_button.pack(pady=20)

        # Message d'erreur
        self.error_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14), text_color="red")
        self.error_label.pack(pady=10)

        self.username_entry.focus_set()

    def register(self, event=None):
        username = self.username_entry.get().strip()
        print(f"Utilisateur '{username}' tente de s'inscrire.")

        if not username:
            self.error_label.configure(text="Veuillez entrer un identifiant valide.")
            return
        
        # Ici, vous pouvez ajouter la logique d'inscription (ex: vérifier si l'utilisateur existe déjà, etc.)

        self.controller.show_page("MainPage")