"""
simple_test.py - Fichier léger de test pour la revue de code.
"""

# 1. Secret hardcodé
DATABASE_URL = "postgres://admin:Password123!@localhost:5432/mydb"


# 2. Erreur NameError (variable non définie)
def calculer_remise(prix):
    total = prix - reduction
    return total
