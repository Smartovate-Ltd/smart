"""
test_vulnerabilities.py — Fichier de démonstration pour tester l'agent d'analyse de code.
Contient des failles de sécurité critiques et des erreurs de syntaxe/logique.
"""

import os
import sqlite3
from fastapi import FastAPI, Request

app = FastAPI()

# 1. CRITICAL: Secret hardcodé (API Key / Token exposé)
AWS_SECRET_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE_SECRET_KEY_DONT_HARDCODE"
DATABASE_PASSWORD = "AdminPassword123!"


# 2. CRITICAL: Injection SQL (requête préparée manquante)
@app.get("/user")
def get_user_profile(user_id: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Faille de sécurité : Concaténation directe de chaîne pour requête SQL
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    return cursor.fetchall()


# 3. HIGH: Path Traversal (lecture arbitraire de fichiers)
@app.get("/read-file")
def read_user_file(filename: str):
    # Faille : Aucune vérification du chemin fourni (ex: ../../etc/passwd)
    filepath = os.path.join("/var/www/uploads", filename)
    with open(filepath, "r") as f:
        return f.read()


# 4. HIGH / MEDIUM: Execution de commande système (RCE potential)
@app.get("/ping")
def ping_host(host: str):
    # Faille : Exécution de commandes arbitraires via os.system / popen
    response = os.popen(f"ping -c 1 {host}").read()
    return {"result": response}


# 5. BUG / NameError: Utilisation d'une variable non définie
def calculate_total_price(items):
    total = 0
    for item in items:
        total += item.price
    # Erreur de syntaxe / logique : variable 'tax_rate' non définie
    final_amount = total * (1 + tax_rate)
    return final_amount
