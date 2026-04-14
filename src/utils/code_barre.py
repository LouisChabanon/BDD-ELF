# def lire_code_barre():
#     """
#     Attend la lecture d'un code-barres via un lecteur USB (mode clavier)
#     et retourne la valeur lue sous forme de chaîne de caractères.
#     """
#     code = input("Scannez un code-barres : ").strip()
#     return code

# # Exemple d'appel
# print("=== LECTURE CODE-BARRES ===")
# code_lu = lire_code_barre()
# print(f"Code-barres lu : {code_lu}")



#import random
#import barcode
#from barcode.writer import ImageWriter

codes_existants = set()

def generer_code_barre_unique(prefixe="123456", nom_fichier="code_auto"):
    while True:
        code = prefixe + str(random.randint(0, 999999)).zfill(6)
        if code not in codes_existants:
            codes_existants.add(code)
            ean = barcode.get_barcode_class('ean13')
            mon_code = ean(code[:12], writer=ImageWriter())
            fichier = mon_code.save(nom_fichier)
            print(f" Code-barres unique généré : {code}")
            return fichier


def parse_vcard(vcard_text):
    #Permet de récupérer les informations du QR-code carte ENSAM
    data = {}
    lines = vcard_text.splitlines()
    for line in lines:
        if line.startswith("N:"):
            parts = line[2:].split(";")
            data["nom"] = parts[0]
            data["prenom"] = parts[1] if len(parts) > 1 else ""

        elif line.startswith("FN:"):
            data["full_name"] = line[3:]

        elif line.startswith("EMAIL"):
            data["email"] = line.split(":")[1]

    return data