import customtkinter as ctk
from tkinter import filedialog
from components.bandeau_sup import Band_sup
from database.queries import (
    add_matos as create_materiel,
    add_material as create_exemplaire,
    get_all_materiels,
    get_all_rangements,
    materiel_exists,
    exemplaire_exists
)



class AjouterObjetPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#F9F7F0")

        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        frame = ctk.CTkFrame(self, fg_color="#F9F7F0")
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Que souhaitez-vous ajouter ?", font=("Helvetica", 28, "bold")).pack(pady=30)

        ctk.CTkButton(
            frame,
            text="➕ Ajouter un nouveau matériel",
            height=80, width=500,
            font=("Helvetica", 18, "bold"),
            command=lambda: controller.show_page("AjouterMaterielPage")
        ).pack(pady=20)

        ctk.CTkButton(
            frame,
            text="➕ Ajouter un exemplaire d’un matériel existant",
            height=80, width=500,
            font=("Helvetica", 18, "bold"),
            command=lambda: controller.show_page("AjouterExemplairePage")
        ).pack(pady=10)

    


#Ajouter un matériel

class AjouterMaterielPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#F9F7F0")

        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        main = ctk.CTkFrame(self, fg_color="#F9F7F0")
        main.pack(fill="both", expand=True, padx=40, pady=20)

        # header
        header = ctk.CTkFrame(main, fg_color="#F9F7F0")
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Ajouter un matériel", font=("Helvetica", 24, "bold")).pack(side="left")

        # form
        form = ctk.CTkFrame(main, fg_color="#F9F7F0")
        form.pack(pady=20)

        # Nom matériel
        ctk.CTkLabel(form, text="Nom du matériel :", font=("Helvetica", 16)).grid(row=0, column=0, sticky="e", pady=8)
        self.nom_entry = ctk.CTkEntry(form, width=380)
        self.nom_entry.grid(row=0, column=1, pady=8, padx=8)

        # Photo
        ctk.CTkLabel(form, text="Photo :", font=("Helvetica", 16)).grid(row=1, column=0, sticky="e", pady=8)
        self.photo_var = ctk.StringVar()
        ctk.CTkEntry(form, textvariable=self.photo_var, width=300).grid(row=1, column=1, sticky="w")
        ctk.CTkButton(form, text="Choisir", command=self.select_photo).grid(row=1, column=2, padx=6)

        # Fréquence entretien
        ctk.CTkLabel(form, text="Fréquence d'entretien :", font=("Helvetica", 16)).grid(row=2, column=0, sticky="e", pady=8)
        self.freq_entry = ctk.CTkEntry(form, width=380)
        self.freq_entry.grid(row=2, column=1, pady=8)

        # Notice PDF
        ctk.CTkLabel(form, text="Notice PDF :", font=("Helvetica", 16)).grid(row=3, column=0, sticky="e", pady=8)
        self.notice_var = ctk.StringVar()
        ctk.CTkEntry(form, textvariable=self.notice_var, width=300).grid(row=3, column=1, sticky="w")
        ctk.CTkButton(form, text="Choisir PDF", command=self.select_pdf).grid(row=3, column=2, padx=6)

        # Lieu rangement
        ctk.CTkLabel(form, text="Lieu de rangement :", font=("Helvetica", 16)).grid(row=4, column=0, sticky="e", pady=8)
        self.lieu_combo = ctk.CTkComboBox(form, width=380, values=self.load_rangements())
        self.lieu_combo.grid(row=4, column=1, pady=8)

        self.error_label = ctk.CTkLabel(self, text="", text_color="maroon")
        self.error_label.pack(pady=5)

        # Actions
        actions = ctk.CTkFrame(main, fg_color="#F9F7F0")
        actions.pack(fill="x", pady=20)

        ctk.CTkButton(actions, text="💾 Ajouter le matériel",
                      font=("Helvetica", 16, "bold"),
                      command=self.save_material).pack(side="right", padx=10)

        ctk.CTkButton(actions, text="Annuler",
                      command=lambda: controller.show_page("AjouterObjetPage")).pack(side="left", padx=10)

    # --------------------------------------------------------------------
    def load_rangements(self):
        lst = get_all_rangements()
        return lst if lst else ["Aucun rangement"]

    def select_photo(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if path:
            self.photo_var.set(path)

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if path:
            self.notice_var.set(path)

    # --------------------------------------------------------------------
    def save_material(self):
        nom = self.nom_entry.get().strip()
        photo = self.photo_var.get().strip() or None
        freq = self.freq_entry.get().strip() or None
        notice = self.notice_var.get().strip() or None

        if not nom:
            self.error_label.configure(text= "Veuillez saisir un nom.")
            return

        if materiel_exists(nom):
            self.error_label.configure(text="Un matériel portant ce nom existe déjà.")
            return

        data = {
            "nom_materiel": nom,
            "photo_materiel": photo,
            "frequence_entretient": freq,
            "notice_materiel": notice
        }

        try:
            create_materiel(nom, photo, freq, notice)
        except Exception as e:
            self.popup("Erreur", f"Impossible d'ajouter le matériel, vérifie tes arguments :\n{e}",is_success=False)
            return

       # popup de succès
        self.popup(
            "Succès",
            f"Le matériel '{nom}' a été ajouté avec succès.\n\n"
            "Vous pouvez maintenant ajouter un exemplaire si nécessaire.",
            is_success=True
        )

    def close_popup_and_return(self, popup):
        popup.destroy()
        self.controller.show_page("AjouterObjetPage")

    # --------------------------------------------------------------------
    def popup(self, title, msg, is_success):
        p = ctk.CTkToplevel(self)
        p.geometry("420x180")
        p.title(title)
        p.configure(fg_color="#F9F7F0")

        p.attributes('-topmost', True)  # Force la fenêtre au-dessus de toutes les autres
        p.focus_force()                 # Donne le focus clavier/souris au popup
        p.grab_set()                    # Rend le popup "modal" (bloque la fenêtre arrière)

        color = "green" if is_success else "maroon"
        icon = "✅" if is_success else "❌"

        frame = ctk.CTkFrame(p, fg_color="#F9F7F0")
        frame.pack(expand=True, padx=20, pady=20)

        # Affichage du symbole et du message
        ctk.CTkLabel(frame, text=f"{icon} {title}", font=("Helvetica", 18, "bold"), text_color=color).pack(pady=5)
        ctk.CTkLabel(frame, text=msg, font=("Helvetica", 13), text_color=color, justify="center", wraplength=380).pack(pady=10)
        
        ctk.CTkButton(frame, text="OK", command=lambda: self.close_popup_and_return(p)).pack(pady=10)

# Ajouter un exemplaire

class AjouterExemplairePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#F9F7F0")

        self.bandeau = Band_sup(self, controller)
        self.bandeau.pack(fill="x", side="top")

        main = ctk.CTkFrame(self, fg_color="#F9F7F0")
        main.pack(fill="both", expand=True, padx=40, pady=20)

        # header
        header = ctk.CTkFrame(main, fg_color="#F9F7F0")
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Ajouter un exemplaire", font=("Helvetica", 24, "bold")).pack(side="left")

        # form
        form = ctk.CTkFrame(main, fg_color="#F9F7F0")
        form.pack(pady=20)

        # ID exemplaire
        ctk.CTkLabel(form, text="ID (code-barres) :", font=("Helvetica", 16)).grid(row=0, column=0, pady=8)
        self.id_entry = ctk.CTkEntry(form, width=380)
        self.id_entry.grid(row=0, column=1, pady=8)

        # Matériel
        ctk.CTkLabel(form, text="Matériel :", font=("Helvetica", 16)).grid(row=1, column=0, pady=8)
        self.mat_combo = ctk.CTkComboBox(form, width=380, values=self.load_materiels())
        self.mat_combo.grid(row=1, column=1, pady=8)

        # Lieu rangement
        ctk.CTkLabel(form, text="Lieu :", font=("Helvetica", 16)).grid(row=2, column=0, pady=8)
        self.lieu_combo = ctk.CTkComboBox(form, width=380, values=self.load_rangements())
        self.lieu_combo.grid(row=2, column=1, pady=8)

        # Garantie
        ctk.CTkLabel(form, text="Date garantie :", font=("Helvetica", 16)).grid(row=3, column=0, pady=8)
        self.garantie_entry = ctk.CTkEntry(form, width=380)
        self.garantie_entry.grid(row=3, column=1, pady=8)

        # Dernier entretien
        ctk.CTkLabel(form, text="Dernier entretien :", font=("Helvetica", 16)).grid(row=4, column=0, pady=8)
        self.entretien_entry = ctk.CTkEntry(form, width=380)
        self.entretien_entry.grid(row=4, column=1, pady=8)

        # Localisation
        ctk.CTkLabel(form, text="Dernière localisation :", font=("Helvetica", 16)).grid(row=5, column=0, pady=8)
        self.loc_entry = ctk.CTkEntry(form, width=380)
        self.loc_entry.grid(row=5, column=1, pady=8)

        self.error_label = ctk.CTkLabel(self, text="", text_color="maroon")
        self.error_label.pack(pady=5)

        # actions
        actions = ctk.CTkFrame(main, fg_color="#F9F7F0")
        actions.pack(fill="x", pady=20)

        ctk.CTkButton(actions, text="💾 Ajouter l’exemplaire",
                      font=("Helvetica", 16, "bold"),
                      command=self.save_exemplaire).pack(side="right", padx=10)

        ctk.CTkButton(actions, text="Annuler",
                      command=lambda: controller.show_page("AjouterObjetPage")).pack(side="left", padx=10)

    # --------------------------------------------------------------------
    def load_materiels(self):
        mats = get_all_materiels()
        if not mats:
            return ["Aucun matériel"]
        return [m["nom_materiel"] for m in mats]

    def load_rangements(self):
        lst = get_all_rangements()
        return lst if lst else ["Aucun rangement"]

    # --------------------------------------------------------------------
    def save_exemplaire(self):
        id_val = self.id_entry.get().strip()
        nom_mat = self.mat_combo.get().strip()
        lieu = self.lieu_combo.get().strip()

        # Validations simples
        if not id_val.isdigit():
            self.error_label.configure(text="L’ID doit être un nombre.")
            return

        id_val = int(id_val)

        if exemplaire_exists(id_val):
            self.error_label.configure(text="Cet exemplaire existe déjà.")
            return

        data = {
            "id_exemplaire": id_val,
            "date_garantie": self.garantie_entry.get().strip(),
            "date_dernier_entretient": self.entretien_entry.get().strip(),
            "derniere_localisation": self.loc_entry.get().strip() or lieu,
            "nom_materiel": nom_mat,
            "lieu_rangement": lieu
        }

        try:
            create_exemplaire(id_val,self.garantie_entry.get().strip(),self.entretien_entry.get().strip(),self.loc_entry.get().strip() or lieu, nom_mat )
        except Exception as e:
            self.popup("Erreur", f"Impossible d'ajouter l'exemplaire :\n{e}",is_success=False)
            return

        self.popup("Succès", f"L'exemplaire {id_val} a été ajouté au matériel '{nom_mat}'.",is_success=True)

    def close_popup_and_return(self, popup):
        popup.destroy()
        self.controller.show_page("MainPage")

    # --------------------------------------------------------------------
    def popup(self, title, msg, is_success):
        p = ctk.CTkToplevel(self)
        p.geometry("420x180")
        p.title(title)
        p.configure(fg_color="#F9F7F0")

        p.attributes('-topmost', True)  # Force la fenêtre au-dessus de toutes les autres
        p.focus_force()                 # Donne le focus clavier/souris au popup
        p.grab_set()                    # Rend le popup "modal" (bloque la fenêtre arrière)

        color = "green" if is_success else "maroon"
        icon = "✅" if is_success else "❌"

        frame = ctk.CTkFrame(p, fg_color="#F9F7F0")
        frame.pack(expand=True, padx=20, pady=20)

        # Affichage du symbole et du message
        ctk.CTkLabel(frame, text=f"{icon} {title}", font=("Helvetica", 18, "bold"), text_color=color).pack(pady=5)
        ctk.CTkLabel(frame, text=msg, font=("Helvetica", 13), text_color=color, justify="center", wraplength=380).pack(pady=10)
        
        ctk.CTkButton(frame, text="OK", command=lambda: self.close_popup_and_return(p)).pack(pady=10)