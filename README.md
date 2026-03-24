# BDD-ELF

Application de bureau développée en Python pour la gestion d'emprunt de materiel pédagogique. L'application se connecte à une base de données MySQL et utilise un serveur Samba pour le stockage et la récupération des images/fichiers. Elle intègre également l'envoi d'e-mails via l'API Resend.

## Prérequis

- **Python 3.8+** installé sur votre machine.
- Accès à une base de données **MySQL**.
- Accès à un serveur de fichiers **Samba**.
- Un compte [Resend](https://resend.com/) pour l'envoi d'e-mails.

---

## Variables d'environnement (`.env`)

L'application utilise un fichier `.env` pour stocker les informations sensibles et les configurations. Créez un fichier `.env` à la racine du projet (au même niveau que `src/`) et renseignez les variables suivantes :

```env
# --- Configuration de la base de données MySQL ---
DB_HOST=127.0.0.1          # L'adresse de votre base (ex: localhost ou une IP)
DB_USER=root               # L'utilisateur MySQL
DB_PORT=3306               # Le port (3306 par défaut)
DB_PASSWORD=secret         # Le mot de passe de l'utilisateur
DB_NAME=bdd_elf            # Le nom de la base de données utilisée par l'app

# --- Configuration du Serveur Samba ---
SAMBA_SRV=192.168.1.0      # Adresse IP ou Nom d'hôte du serveur Samba
SAMBA_USER=partage         # Utilisateur autorisé à accéder au dossier Samba
SAMBA_PASSWORD=mdp_samba   # Mot de passe de l'utilisateur Samba

# --- Configuration de l'API Email (Resend) ---
RESEND_API_KEY=re_xxxx...  # Clé d'API fournie par resend.com
SENDER_EMAIL=test@test.com # L'adresse e-mail de l'expéditeur
```

---

## Déploiement de l'Application

Pour exécuter l'application localement, suivez ces étapes :

1. **Cloner le projet** (si ce n'est pas déjà fait) :
   ```bash
   git clone <URL_DU_DEPOT>
   cd BDD-ELF
   ```

2. **Créer un environnement virtuel (Recommandé)** :
   ```bash
   python -m venv venv
   # Sur Windows :
   venv\Scripts\activate
   # Sur macOS / Linux :
   source venv/bin/activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer l'environnement** :
   Créez le fichier `.env` à la racine comme expliqué dans la section ci-dessus.

5. **Initialiser la base de données** :
   Un script est prévu pour initialiser les tables de la base :
   ```bash
   python scripts/create_database.py
   ```

   > Attention, ce script recrée la base à chaque exécution !

6. **Lancer l'application** :
   ```bash
   python src/main.py
   ```

*(Note : Pour déployer l'application sous forme de fichier exécutable `.exe` unique (sans besoin que les utilisateurs installent Python), vous pouvez utiliser un outil comme **PyInstaller**.)*

---

## Guide D'Hébergement

### 1. Comment héberger une Base de Données MySQL

Si vous testez l'application localement et n'avez pas de base de données MySQL :

**Solution Locale avec XAMPP (Windows/Mac/Linux)**
- Allez sur [Apache Friends](https://www.apachefriends.org/) et téléchargez **XAMPP**.
- Installez le logiciel et lancez le **XAMPP Control Panel**.
- Cliquez sur "Start" sur la ligne **MySQL**.
- Votre base locale est maintenant en ligne ! 
- Pour créer la base `bdd_elf`, cliquez sur "Admin" à côté de MySQL. Cela ouvre *phpMyAdmin* dans votre navigateur.
- Allez dans "Nouvelle base de données", tapez `bdd_elf` et cliquez sur "Créer".
- *Vos identifiants dans le `.env` seront :* `DB_HOST=127.0.0.1`, `DB_USER=root`, `DB_PASSWORD=` (vide par défaut).

**Solution sur un Serveur Local** 
(A TESTER, JAMAIS ESSAYÉ PAR MOI-MEME : PRENDRE UN RASPBERRY PI (le + simple) ET TEST !! (DMD à AE il doit en avoir))
Pour héberger sur un serveur dédié (ex: Serveur Linux ou Raspberry Pi) :
1. Installez MySQL sur le serveur : `sudo apt install mysql-server`. (Si vous utilisez Debian/Ubuntu)
2. Autorisez les connexions distantes en modifiant le fichier de configuration (souvent `/etc/mysql/mysql.conf.d/mysqld.cnf`) : changez `bind-address = 127.0.0.1` en `bind-address = 0.0.0.0`.
3. Redémarrez le service : `sudo systemctl restart mysql`.
4. Connectez-vous à MySQL (`sudo mysql`) et créez la base ainsi qu'un utilisateur distant :
   ```sql
   CREATE DATABASE bdd_elf;
   CREATE USER 'admin_app'@'%' IDENTIFIED BY 'mot_de_passe_robuste';
   GRANT ALL PRIVILEGES ON bdd_elf.* TO 'admin_app'@'%';
   FLUSH PRIVILEGES;
   ```
5. *Vos identifiants dans le `.env` de l'application (sur les PC clients) seront :* `DB_HOST=<IP_DU_SERVEUR>` (ex: 192.168.1.50), `DB_USER=admin_app`, `DB_PASSWORD=mot_de_passe_robuste`.

**Solution en Ligne**
Si vous voulez que la DB soit accessible de n'importe où, vous pouvez utiliser des services cloud avec des offres gratuites comme **Aiven**, **Clever Cloud**, ou **PlanetScale**. Vous y créerez un cluster MySQL, et ils vous fourniront un `Host`, un `User`, et un `Password` à mettre dans votre fichier `.env`.

### 2. Comment configurer un Serveur Samba (SMB)

L'application a besoin d'un serveur Samba pour lire/écrire des fichiers (les images/notices). Le plus simple est de créer un "Dossier Partagé" Windows sur votre réseau local.

**Sur Windows (Créer un partage réseau local) :**
1. Créez un nouveau dossier, par exemple `Images_App` sur votre PC.
2. Faites un clic-droit sur le dossier -> **Propriétés**.
3. Allez dans l'onglet **Partage** et cliquez sur **Partage avancé...**
4. Cochez **Partager ce dossier**. Notez le "Nom du partage".
5. Cliquez sur le bouton **Autorisations** et assurez-vous que l'utilisateur a le droit de "Lecture" et de "Modifier".
6. *Vos identifiants dans le `.env` seront :* 
   - `SAMBA_SRV`: L'adresse IP de ce PC Windows sur le réseau local (ex: `192.168.1.15`).
   - `SAMBA_USER`: Votre nom d'utilisateur Windows.
   - `SAMBA_PASSWORD`: Votre mot de passe de session Windows.

