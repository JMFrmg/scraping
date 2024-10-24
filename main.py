
# Les imports
import sqlite3
import requests
from pprint import pprint
from bs4 import BeautifulSoup

# On récupère le code html de la page web avec requests
page = requests.get("https://fr.wikipedia.org/wiki/Liste_des_pays_par_PIB_(PPA)_par_habitant")

# On transfère le code HTML dans un objet beautifulsoup
soup = BeautifulSoup(page.text, 'html.parser')

# On récupère les tables dans une liste avec la méthode find_all
# On crée une variable tables qui référence cette liste
tables = soup.find_all("table", {"class": "wikitable alternance"})

# La table qui nous intéresse est la seconde (index 1 dans la liste)
# On relance un find_all pour obtenir une liste de toutes les lignes (les tr) de la table
rows = tables[1].find_all("tr")

pib_list = []  # Variable qui va stocker les données

for row in rows[1:]:  # On itère sur chaque tr (ligne) du tableau
    country = row.find_all("a")[-1].text  # On récupère le pays
    pib = row.find_all("td")[-1].text.replace(u'\xa0', u'').strip()  # On récupère et on nettoie le text pib
    pib = int(pib)  # On transforme la chaîne de caractères pib en integer
    pib_list.append((country, pib))

pprint(pib_list)  # On affiche nos données en console pour contrôler

# Création de la table dans la base de données SQL
connexion = sqlite3.connect("data.db")
cursor = connexion.cursor()
sql_statement = "DROP TABLE IF EXISTS country_pib"
cursor.execute(sql_statement)
connexion.commit()

sql_statement = """CREATE TABLE IF NOT EXISTS country_pib
(
    country VARCHAR(100),
    pib_per_capita INT
)"""
cursor.execute(sql_statement)
connexion.commit()

# On itère sur nos données (liste de tuple)
for country, pib_per_capita in pib_list:
    # A chaque itération :
    #    country : nom du pays (type : string)
    #    pib_per_capita : pib par habitant (type: int)
    country = country.replace("'", "''").strip()
    sql_statement = f"INSERT INTO country_pib ('country', 'pib_per_capita') VALUES ('{country}', '{pib_per_capita}')"
    cursor.execute(sql_statement)
connexion.commit()
connexion.close()

