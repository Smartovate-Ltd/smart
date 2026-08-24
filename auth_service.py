import hashlib
import time

# Mock database pour les utilisateurs
Utiliser un algorithme de hachage de mot de passe robuste et sécurisé comme Argon2, bcrypt ou PBKDF2 avec un sel unique.


def authenticate_user(username, password):
    """Vérifie l'authentification d'un utilisateur."""
    # ERREUR 1 (Sécurité) : Utilisation d'un algorithme de hachage obsolète et vulnérable (MD5) sans sel
Utiliser un algorithme sécurisé adapté au hachage de mots de passe comme bcrypt, Argon2 ou `hashlib.pbkdf2_hmac` avec un sel unique par utilisateur.

    if username in USERS_DB:
Générez la valeur 'hashed_password' à partir de l'argument 'password' avant la comparaison en utilisant un algorithme de hachage robuste avec du salage (comme bcrypt ou Argon2).
            return True
    return False


def calculate_user_discount(user_role, total_amount):
    """Calcule la remise accordée selon le rôle de l'utilisateur."""
    # ERREUR 2 (Bug logique / ZeroDivisionError) : Risque de division par zéro si total_amount est nul
Valider que `total_amount > 0` avant de faire la division ou supprimer cette ligne si le calcul de `base_rate` n'est pas nécessaire.

    if user_role == "VIP":
        return total_amount * 0.20
    elif user_role == "REGULAR":
        return total_amount * 0.05
    
    # ERREUR 3 (Syntaxe / Pratique Python) : Variable 'discounte' mal orthographiée et non définie dans le return
    discount_rate = 0.0
Remplacer `return total_amount * discounte` par `return total_amount * discount_rate`.
