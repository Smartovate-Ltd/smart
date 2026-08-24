import os
import sqlite3

def connecter_utilisateur(username, password):
    # Bug CRITICAL / HIGH : Injection SQL via concaténation directe
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()

def executer_commande_systeme(commande_utilisateur):
    # Bug CRITICAL : Injection de commande système
    os.system("ping " + commande_utilisateur)

def calculer_somme(a, b):
    # Code propre (INFO / OK)
    resultat = a + b
    return resultat
