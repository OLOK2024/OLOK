import numpy as np
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest

def save_log(log, path):
    # Vérifier si le fichier existe déjà
    if not os.path.exists(path):
        # Créer le fichier s'il n'existe pas
        with open(path, "x") as f:
            pass

    # Ouvrir le fichier en mode ajout et écrire le log
    with open(path, "a") as f:
        f.write(log + "\n")

def convert_log_2_csv(csv_path, log_path):

    # Ouvrez le fichier texte en mode lecture
    with open(log_path, 'r') as fichier_texte:
        # Lisez le contenu du fichier
        texte = fichier_texte.read()

    # Divisez le texte en lignes
    lignes = texte.strip().split('\n')

    # Créez un fichier CSV
    with open(csv_path, 'w', newline='') as fichier_csv:
        csv_writer = csv.writer(fichier_csv)
        # Écrivez chaque ligne dans le fichier CSV
        for ligne in lignes:
            # Divisez chaque ligne en éléments distincts en utilisant les espaces comme délimiteurs
            elements = ligne.split(' - ')
            del elements[1]

            # Écrivez chaque élément dans le fichier CSV, en ajoutant une virgule entre chaque élément
            csv_writer.writerow(elements)

def pre_treatment(path):

    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(path, header=None)

    # Créer un dictionnaire pour mapper les valeurs
    mapping = {'new': 1, 'get': 2, 'modif': 4, 'del': 3}

    # Remplacer les valeurs dans la deuxième colonne en utilisant le mapping
    df[1] = df[1].replace(mapping)

    # Supprimer la dernière colonne avec les id des objets
    df = df.iloc[:, :-1]

    # Conversion du timestamp en datetime
    df[0] = pd.to_datetime(df[0], format="%Y-%m-%d %H:%M:%S,%f")

    # Écrire le DataFrame modifié dans un nouveau fichier CSV
    df.to_csv(path, index=False, header=False)

def train_model(id):

    csv_path = f"./user_{id}.csv"
    log_path = f"./user_{id}.log.test"

    # Convertir le fichier de log en fichier CSV
    convert_log_2_csv(csv_path, log_path)

    # Prétraitement du fichier CSV
    pre_treatment(csv_path)

    # Définir les noms des colonnes
    noms_colonnes = ['Date', 'Action', 'ID']

    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(csv_path, names=noms_colonnes, parse_dates=['Date'])
    #df['Date'] = df['Date'].astype(np.int64) / 10**9

    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    # Sélectionner les colonnes à utiliser
    X = df[['Hour', 'Minute', 'Action']]

    #mapping = {1:'new', 2:'get', 4:'modif', 3:'del'}

    # Affichage des données
    #plt.figure(figsize=(10, 5))
    #plt.plot(df['Date'],df['Action'].map(mapping))
    #plt.xlabel('Date')
    #plt.ylabel('Action')
    #plt.title('Action en fonction de la Date')
    #plt.grid(True)
    #plt.show()

    # Entraîner le modèle d'Isolation Forest
    clf = IsolationForest()
    clf.fit(X)

    # Suppression du fichier temporaire
    os.remove(csv_path)

    # Renvoie le modèle entraîné
    return clf

def predict(clf, log):

    save_log(log, "./predict.log")

    convert_log_2_csv("./predict.csv", "./predict.log")

    pre_treatment("./predict.csv")

    noms_colonnes = ['Date', 'Action', 'ID']

    df = pd.read_csv("./predict.csv", names=noms_colonnes, parse_dates=['Date'])
    #df['Date'] = df['Date'].astype(np.int64) / 10**9

    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    X = df[['Hour', 'Minute', 'Action']]

    anomalie = clf.predict(X)

    os.remove("./predict.log")
    os.remove("./predict.csv")

    return anomalie


#log = "2024-05-01 20:56:44,308 - INFO - get - 1 - 6606dcd25379a50c0e318597"

# Ouvrir fichier user_1_predict.log.test et lire ligne par ligne
filename = 'user_1_predict.log.test'
with open(filename, 'r') as file:

    convert_log_2_csv("./user_1.csv", "./user_1.log.test")
    pre_treatment("./user_1.csv")

    clf = train_model(1)

    for line in file:
        # Traiter chaque ligne ici
        log = line.strip()
        anomalie = predict(clf, log)
        print(log)
        print(anomalie)