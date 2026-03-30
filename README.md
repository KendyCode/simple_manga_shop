# 📚 Manga Shop — Guide d'installation

> Application Flask de vente de mangas en ligne, avec catalogue, wishlist, panier et espace d'administration.

---

## 📋 Prérequis

- Python 3.x
- MariaDB installé et démarré
- pip
- Git

---

## ⚙️ 1. Créer l'environnement virtuel

```bash
python3 -m venv venv
```

---

## 🔌 2. Activer l'environnement virtuel

**Windows (PowerShell)** — si tu vois `PS` devant le chemin dans le terminal :

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS :**

```bash
source venv/bin/activate
```

> ✅ L'activation est réussie quand tu vois `(venv)` au début de ta ligne de commande.

---

## 🏫 3. (Lycée uniquement) Configurer le proxy

> ⚠️ **À faire AVANT `pip install` si tu es au lycée**, sinon pip ne pourra pas télécharger les paquets.

```bash
export http_proxy="http://172.16.0.51:8080"
export https_proxy="http://172.16.0.51:8080"
```

---

## 📦 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🗄️ 5. Créer la base de données MariaDB

Connecte-toi à MariaDB :

```bash
mysql -u root -p
```

Puis crée ta base de données :

```sql
CREATE DATABASE nom_de_ta_base;
EXIT;
```

> Remplace `nom_de_ta_base` par le nom de ton choix (ex: `mangashop_db`).

---

## 🔐 6. Créer le fichier `.env`

Crée un fichier `.env` **à la racine du projet** (au même niveau que `run.py`) :

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_DEBUG=1

# Database Configuration (MySQL/MariaDB)
DB_USER=ton_utilisateur
DB_PASSWORD=ton_mot_de_passe
DB_HOST=localhost
DB_NAME=nom_de_ta_base
```

> ⚠️ Ne commit **jamais** le fichier `.env` sur Git. Vérifie qu'il est bien dans ton `.gitignore`.

---

## 🔄 7. Appliquer les migrations

Si un dossier `migrations/` est déjà présent dans le projet :

```bash
flask db upgrade
```

---

## ▶️ 8. Lancer l'application

```bash
flask run
```


---

## 👑 9. Passer un utilisateur en administrateur

Après avoir créé un compte via l'interface web, partir dans plus.py:

Puis exécute :

```python
from app import app, db
from app.models import User

with app.app_context():
    # Chercher l'utilisateur par son pseudo
    mon_user = User.query.filter_by(username='ton_pseudo').first()

    # Passer le statut admin à True
    mon_user.is_admin = True

    # Sauvegarder dans la base de données
    db.session.commit()
    print("Succès ! L'utilisateur est maintenant admin.")

```

> Remplace `'ton_pseudo'` par le `username` du compte créé au préalable sur le site.  
> Une fois admin, l'utilisateur aura accès au tableau de bord `/admin/dashboard`.

---

## 🛑 .gitignore recommandé

```
venv/
.env
__pycache__/
*.pyc
instance/
```

---

## ❓ Problèmes fréquents

| Problème | Solution |
|---|---|
| `pip` ne télécharge rien au lycée | Configure le proxy (étape 3) |
| `flask db upgrade` échoue | Vérifie les identifiants dans `.env` et que MariaDB tourne |
| `Activate.ps1` refusé sous Windows | Exécute `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` dans PowerShell |
| Module introuvable | Vérifie que `(venv)` est bien actif dans ton terminal |

---

## 📖 À propos du projet

**Manga Shop** est une application web de vente de mangas en ligne. Elle permet aux utilisateurs de parcourir un catalogue, d'ajouter des titres à leur wishlist ou à leur panier, et de gérer leur compte. Un espace d'administration complet permet de gérer le catalogue et les auteurs.

### Fonctionnalités principales

- 📖 **Catalogue de mangas** : affichage de tous les titres disponibles avec couverture, description, prix et stock
- 👤 **Gestion de compte** : inscription, connexion, déconnexion
- ❤️ **Wishlist** : sauvegarde des mangas que l'utilisateur souhaite acheter plus tard
- 🛒 **Panier** : ajout de mangas en vue d'un achat
- 🛡️ **Espace d'administration** : gestion complète des mangas et des auteurs (ajout, modification, suppression)

### 🗂️ Structure des données

Le projet s'articule autour de quatre modèles principaux :

**`User`** — Compte utilisateur avec gestion des rôles (utilisateur / administrateur).

**`Author`** — Auteur de manga, avec nom et biographie. Un auteur peut être lié à plusieurs mangas.

**`Manga`** — Entrée du catalogue avec titre, description, prix, stock, URL de couverture et référence à l'auteur. L'auteur est optionnel : un manga peut exister sans auteur associé.

**`WishlistItem` / `CartItem`** — Éléments liés à un utilisateur, permettant de suivre les mangas en wishlist ou dans le panier.



### 🛡️ Fonctionnement de l'administration

L'accès à toutes les routes `/admin/*` est protégé par un double contrôle : l'utilisateur doit être connecté (`@login_required`) **et** avoir le statut `is_admin = True` (`@admin_required`). Tout accès non autorisé renvoie une erreur **403**.

Depuis le tableau de bord, un administrateur peut :

- Ajouter, modifier ou supprimer un **auteur**
- Ajouter, modifier ou supprimer un **manga** du catalogue
- Lors de la modification d'un manga, dissocier l'auteur en sélectionnant *"Aucun auteur"*