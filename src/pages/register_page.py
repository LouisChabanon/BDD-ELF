import customtkinter as ctk
from database.queries import get_all_users, add_user
from utils.session import set_session

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Couleur de fond principale
        self.configure(fg_color="#F9F7F0")
        
        # Titre de la page
        self.label = ctk.CTkLabel(self, text="Inscription à la base de données ELF", font=("Helvetica", 24, "bold"))
        self.label.pack(pady=40)

        # Identifiant
        self.username_label = ctk.CTkLabel(self, text="Scanner votre carte ou entrer votre identifiant ENSAM: ", font=("Helvetica", 16))
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self, width=300, font=("Helvetica", 16))
        self.username_entry.pack(pady=10)

        #Nom
        self.name_label = ctk.CTkLabel(self, text="Nom : ", font=("Helvetica", 16))
        self.name_label.pack(pady=10)
        self.name_entry = ctk.CTkEntry(self, width=300, font=("Helvetica", 16))
        self.name_entry.pack(pady=10)

        #Prenom
        self.firstname_label = ctk.CTkLabel(self, text="Prénom : ", font=("Helvetica", 16))
        self.firstname_label.pack(pady=10)
        self.firstname_entry = ctk.CTkEntry(self, width=300, font=("Helvetica", 16))
        self.firstname_entry.pack(pady=10)

        #Mail
        self.email_label = ctk.CTkLabel(self, text="Mail : ", font=("Helvetica", 16))
        self.email_label.pack(pady=10)
        self.email_entry = ctk.CTkEntry(self, width=300, font=("Helvetica", 16))
        self.email_entry.pack(pady=10)
        

        # Bouton d'inscription (aucune validation pour l'instant)
        self.register_button = ctk.CTkButton(self, text="S'inscrire", font=("Helvetica", 16), command=self.register)
        self.register_button.pack(pady=20)

        # Message d'erreur
        self.error_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14), text_color="red")
        self.error_label.pack(pady=10)

        self.username_entry.focus_set()

        # Fonction pour gérer l'appui sur la touche "Entrée"
        self.username_entry.bind("<Return>", self.register)

        # Bouton retour (en bas à droite)
        self.back_button = ctk.CTkButton(
            self,
            text="Retour",
            font=("Helvetica", 14),
            command=lambda: controller.show_page("LoginPage")
        )
        self.back_button.place(relx=0.95, rely=0.95, anchor="se")

    def register(self, event=None):
        username = self.username_entry.get().strip()
        firstname = self.firstname_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()

        print(f"Utilisateur '{username}' tente de s'inscrire.")

        if not username:
            self.error_label.configure(text="Veuillez entrer un identifiant valide.")
            return
        if not name:
            self.error_label.configure(text="Veuillez entrer un nom valide.")
            return
        if not firstname:
            self.error_label.configure(text="Veuillez entrer un prénom valide.")
            return
        if not email or "@" not in email:
            self.error_label.configure(text="Veuillez entrer une adresse email valide.")
            return
        self.error_label.configure(text="")  # Effacer le message d'erreur
        
        # Verifier si l'utilisateur existe déjà dans la base
        existing_users = get_all_users()
        for user in existing_users:
            if user['mail'] == email or str(user['id_personnel']) == username:
                self.error_label.configure(text="Un utilisateur avec cet identifiant ou email existe déjà.")
                return
        
        # Inscrire l'utilisateur dans la base
        try:
            add_user(int(username), email, "doctorant", name, firstname)
        except ValueError as ve:
            self.error_label.configure(text=str(ve))
            return
        print(f"Utilisateur '{username}' inscrit avec succès.")
        
        # Objet user analogue à celui retourné par la fonction de login (peut-être à refactorer plus tard)
        user = {
            "id_personnel": int(username),
            "mail": email,
            "type_personnel": "doctorant",
            "nom": name,
            "prenom": firstname
        }
        
        set_session(user)

        self.controller.show_page("MainPage")