import re
import os
import resend
import dotenv


mail_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

# Charger les variables d'environnement depuis le fichier .env
dotenv.load_dotenv()
resend_api_key = os.getenv("RESEND_API_KEY")
sender_email = os.getenv("SENDER_EMAIL")

def is_valid_email(email):
    return re.fullmatch(mail_regex, email)

# Fonction pour envoyer un e-mail automatiquement
def envoie_mail(destinataire: str, sujet: str, corps: str, schedule_time: str = None):

    assert resend_api_key is not None, "La clé API RESEND_API_KEY n'est pas définie dans les variables d'environnement."
    assert sender_email is not None, "L'adresse e-mail de l'expéditeur SENDER_EMAIL n'est pas définie dans les variables d'environnement."
    resend.api_key = resend_api_key

    if not is_valid_email(destinataire):
        raise ValueError("L'adresse e-mail du destinataire n'est pas valide.")
    
    if not is_valid_email(sender_email):
        raise ValueError("L'adresse e-mail de l'expéditeur n'est pas valide.")

    params = {
        "from": sender_email,
        "to": [destinataire],
        "subject": sujet,
        "html": corps
    }
    if schedule_time:
        params["scheduleAt"] = schedule_time

    try:
        email = resend.Emails.send(params)
        print(f"E-mail envoyé avec succès à {destinataire}. Reponse: {email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")



