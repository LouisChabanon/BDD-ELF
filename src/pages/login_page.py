import customtkinter as ctk
from components.bandeau_sup import Band_sup
from utils.session import set_session
from database.queries import get_user_by_id
import threading
from pyzbar import pyzbar
import cv2
from utils.code_barre import parse_vcard
import hashlib
from pages.register_page import generate_user_id

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.pack(fill="both", expand=True)

        # Couleur de fond principale
        self.configure(fg_color="#F9F7F0")

        # Ajout du bandeau supérieur
        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        # Titre de la page
        self.label = ctk.CTkLabel(self, text="Connexion à la base de données ELF", font=("Helvetica", 24, "bold"),text_color="#4A4947")
        self.label.pack(pady=40)

        # Identifiant
        self.username_label = ctk.CTkLabel(self, text="Scanner votre carte ou entrer votre identifiant ENSAM: ", font=("Helvetica", 16),text_color="#4A4947")
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self, width=300, font=("Helvetica", 16))
        self.username_entry.pack(pady=10)

        # Fonction pour gérer l'appui sur la touche "Entrée"
        self.username_entry.bind("<Return>", self.login)

        # Bouton de connexion (aucune validation pour l'instant)
        self.login_button = ctk.CTkButton(self, text="Se connecter", font=("Helvetica", 16), command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = ctk.CTkButton(self, text="Inscription", font=("Helvetica", 16), command=lambda: controller.show_page("RegisterPage"))
        self.register_button.pack(pady=10)

        #Scann avec la caméra
        ctk.CTkButton(self,text="Scanner avec la caméra",command=self.start_scanner).pack(pady=10)

        # Message d'erreur
        self.error_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14), text_color="maroon")
        self.error_label.pack(pady=10)

        self.username_entry.focus_set()

    def login(self, manual=False):
        username = self.username_entry.get().lower().strip()
        print(f"Utilisateur '{username}' tente de se connecter.")

        if not username:
            self.error_label.configure(text="Veuillez entrer un identifiant valide.")
            return

        if username.isdigit():
            pass
        else :
            username = generate_user_id(username)


        user = get_user_by_id(username)
        if user is None:
            self.error_label.configure(text="Identifiant inconnu. Veuillez vous inscrire.")
            return
        
        print(f"Utilisateur '{username}' connecté avec succès.")
        set_session(user)
        self.controller.show_page("MainPage")

    def start_scanner(self):
        thread = threading.Thread(target=self.scan_barcode)
        thread.daemon = True
        thread.start()

    def scan_barcode(self):
        cap = cv2.VideoCapture(0)

        scanned = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:
                scanned = barcode.data.decode("utf-8")
                
                # Dès qu'on a un code → on arrête
                cap.release()
                cv2.destroyAllWindows()

                # ⚠️ IMPORTANT : interaction avec Tkinter = via after()
                self.after(0, lambda: self.fill_and_validate(scanned))
                return

            cv2.imshow("Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def fill_and_validate(self, code):
        if code.startswith("BEGIN:VCARD"):
            data = parse_vcard(code)

            if "email" in data:
                # Générer un identifiant à partir du mail
                email = data["email"].lower().strip()
                self.username_entry.delete(0, 'end')
                self.username_entry.insert(0, email)

        else:
            # Cas code-barres classique
            self.username_entry.delete(0, 'end')
            self.username_entry.insert(0, code)

        # Lancer l'inscription
        self.login()
        self.username_entry.delete(0, 'end')
        self.username_entry.insert(0, code)
