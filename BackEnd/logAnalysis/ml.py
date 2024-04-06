import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import csv

def convertLog2CSV():

    # Ouvrez le fichier texte en mode lecture
    with open('log.txt', 'r') as fichier_texte:
        # Lisez le contenu du fichier
        texte = fichier_texte.read()

    # Divisez le texte en lignes
    lignes = texte.strip().split('\n')
    print(lignes)

    # Créez un fichier CSV
    with open('log.csv', 'w', newline='') as fichier_csv:
        csv_writer = csv.writer(fichier_csv)
        # Écrivez chaque ligne dans le fichier CSV
        for ligne in lignes:
            # Divisez chaque ligne en éléments distincts en utilisant les espaces comme délimiteurs
            elements = ligne.split(' - ')
            del elements[1]

            # Écrivez chaque élément dans le fichier CSV, en ajoutant une virgule entre chaque élément
            csv_writer.writerow(elements)

# new = 1
# get = 2
# modif = 3
# del = 4
def preTraitementDonnees():
    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv('log.csv', header=None)

    # Créer un dictionnaire pour mapper les valeurs
    mapping = {'new': 1, 'get': 2, 'modif': 3, 'del': 4}

    # Remplacer les valeurs dans la deuxième colonne en utilisant le mapping
    df[1] = df[1].replace(mapping)

    # Supprimer la dernière colonne avec les id des objets
    df = df.iloc[:, :-1]

    # Conversion du timestamp en datetime
    df[0] = pd.to_datetime(df[0], format="%Y-%m-%d %H:%M:%S,%f")

    # Écrire le DataFrame modifié dans un nouveau fichier CSV
    df.to_csv('log.csv', index=False, header=False)

convertLog2CSV()
preTraitementDonnees()

 # Définir les noms des colonnes
noms_colonnes = ['Date', 'Action', 'ID']

df = pd.read_csv('log.csv', names=noms_colonnes, parse_dates=['Date'])
df.info()


# Sélectionner les colonnes appropriées pour l'Isolation Forest
X = df.iloc[:, 1:].values

# Initialiser et entraîner l'Isolation Forest
clf = IsolationForest()
clf.fit(X)

scores=clf.decision_function(X)
anomalies=clf.predict(X)

# Afficher les résultats des prédictions
print(scores)
print(anomalies)
