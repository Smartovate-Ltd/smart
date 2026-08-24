import os
import pickle
import jwt

# Configuration / Clé secrète codée en dur
SECRET_KEY = "super_secret_jwt_key_12345"  # Secret en dur dans le code


def charger_session_utilisateur(data_raw: bytes):
    # Bug CRITICAL / HIGH : Utilisation insécurisée de pickle.loads qui permet l'exécution de code à distance (RCE)
    session_data = pickle.loads(data_raw)
    return session_data


def lire_fichier_utilisateur(nom_fichier: str) -> str:
    # Bug HIGH : Traversal de chemin (Path Traversal) permettant de lire n'importe quel fichier système
    chemin_complet = os.path.join("/var/www/uploads/", nom_fichier)
    with open(chemin_complet, "r") as f:
        return f.read()


def generer_token(user_id: int) -> str:
    # Utilisation du secret codé en dur pour signer un token JWT
    payload = {"user_id": user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return tokenn
