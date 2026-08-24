"""
test_review.py — Fichier de test pour la revue de code automatisée.
"""

import os

# 1. Sécurité : Clé d'API hardcodée
API_SECRET_KEY = "sk_live_99887766554433221100"


# 2. Bug d'exécution : NameError (variable 'taux' non définie)
def calculer_tva(montant):
    total = montant * taux
    return total


# 3. Sécurité : Injection de commande système (RCE)
def executer_commande(utilisateur_input):
    os.system("ping " + utilisateur_input)
