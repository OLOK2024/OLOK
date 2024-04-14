import numpy as np
import pandas as pd
import csv
import joblib
import re
import os
import datetime

from sklearn.ensemble import IsolationForest
from mail import send_mail

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
    mapping = {'new': 1, 'get': 2, 'modif': 3, 'del': 4}

    # Remplacer les valeurs dans la deuxième colonne en utilisant le mapping
    df[1] = df[1].replace(mapping)

    # Supprimer la dernière colonne avec les id des objets
    df = df.iloc[:, :-1]

    # Conversion du timestamp en datetime
    df[0] = pd.to_datetime(df[0], format="%Y-%m-%d %H:%M:%S,%f")

    # Écrire le DataFrame modifié dans un nouveau fichier CSV
    df.to_csv(path, index=False, header=False)

def train_model(id):

    csv_path = f"./tmp/user_{id}.csv"
    log_path = f"./logs/user_{id}.log"

    # Convertir le fichier de log en fichier CSV
    convert_log_2_csv(csv_path, log_path)

    # Prétraitement du fichier CSV
    pre_treatment(csv_path)

    # Définir les noms des colonnes
    noms_colonnes = ['Date', 'Action', 'ID']

    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(csv_path, names=noms_colonnes, parse_dates=['Date'])
    df['Date'] = df['Date'].astype(np.int64) / 10**9

    # Sélectionner les colonnes à utiliser
    X = df[['Date', 'Action']]

    # Entraîner le modèle d'Isolation Forest
    clf = IsolationForest()
    clf.fit(X)

    # Suppression du fichier temporaire
    os.remove(csv_path)

    # Renvoie le modèle entraîné
    return clf

def predict(clf, log):

    save_log(log, "./tmp/predict.log")

    convert_log_2_csv("./tmp/predict.csv", "./tmp/predict.log")

    pre_treatment("./tmp/predict.csv")

    noms_colonnes = ['Date', 'Action', 'ID']

    df = pd.read_csv("./tmp/predict.csv", names=noms_colonnes, parse_dates=['Date'])
    df['Date'] = df['Date'].astype(np.int64) / 10**9

    X = df[['Date', 'Action']]

    anomalie = clf.predict(X)

    os.remove("./tmp/predict.log")
    os.remove("./tmp/predict.csv")

    return anomalie

# Possibilité:
# 1 - Entrainer le modèle
# 2 - Prédire les anomalies
def handler_log(log):
    print("Log reçu: ", log)
    match = re.search(r"- (\d+) -", log)
    if match:
        # Récupération de l'ID
        id = match.group(1)

        # Sauvegarder le log
        save_log(log, f"./logs/user_{id}.log")

        filename = f"./models/user_{id}_model.joblib"
        # Vérifier si le modèle existe déjà
        if not os.path.exists(filename):
            # Création du modèle
            user_model = {
                'model': IsolationForest(),
                'file_creation_date': datetime.datetime.now(),
                'last_train_date': ""
            }

            # Sauvegarder le modèle
            joblib.dump(user_model, filename)
        else:
            # Charger le modèle
            user_model = joblib.load(filename)

            clf = user_model["model"]
            date_now = datetime.datetime.now()
            log_filename = f"./logs/user_{id}.log"

            # Vérifier la date de dernière mise à jour
            if ((date_now - user_model["file_creation_date"]).days) >= 30 and user_model["last_train_date"] == "":

                # Entraîner le modèle
                clf = train_model(id)

                # Détecter les anomalies
                anomalie = predict(clf, log)

                print("Anomalie détectée: ", anomalie)
                if anomalie == -1:
                    send_mail(log)

                # Mise à jour du modèle
                user_model["model"] = clf
                user_model["last_train_date"] = date_now

                # Sauvegarder le modèle
                joblib.dump(user_model, filename)

            elif user_model["last_train_date"] != "" and ((date_now - user_model["last_train_date"]).days) >= 30:

                # Détecter les anomalies
                anomalie = predict(clf, log)

                print("Anomalie détectée: ", anomalie)
                if anomalie == -1:
                    send_mail(log)

                # Calculer la date limite (il y a deux mois)
                limit_date = date_now - datetime.timedelta(days=61)

                # Lire le fichier de log et supprimer les lignes plus vieilles que la date limite
                with open(log_filename, "r") as f:
                    lines = f.readlines()

                with open(log_filename, "w") as f:
                    for line in lines:
                        # Extraire la date du log
                        log_date = datetime.datetime.strptime(line.split(" - ")[0], "%Y-%m-%d %H:%M:%S,%f")

                        # Vérifier si la date du log est plus récente que la date limite
                        if log_date >= limit_date:
                            # Écrire la ligne dans le fichier
                            f.write(line)

                # Entraîner le modèle
                clf = train_model(id)

                # Mise à jour du modèle
                user_model["model"] = clf
                user_model["last_train_date"] = date_now

                # Sauvegarder le modèle
                joblib.dump(user_model, filename)

    else:
        print("Aucun ID trouvé dans le log.")
    return

#log = "2024-04-11 17:53:24,861 - INFO - new - 3 - 6606decc5379a50c0e3185b3"

#print(log.split(" - "))

#handler_log(log)