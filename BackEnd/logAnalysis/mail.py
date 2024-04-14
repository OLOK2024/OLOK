import smtplib
import pymongo
import psycopg2

# Définir les paramètres du serveur SMTP
server = "10.0.1.7"
port = 1025
username = None
password = None

# Définir les paramètres du message
from_addr = "olok@security.com"
subject = "Detection comportement suspect"

def create_mongo_client():
    # Création d'une nouvelle connexion à la base de données MongoDB
    return pymongo.MongoClient(
        "mongodb://{username}:{password}@10.0.1.4:27017/".format(
            username="olok",
            password="olok",
        )
    )

def get_mail(id):
    # Définir les paramètres de connexion à la base de données
    db_name = "olok"
    db_user = "olok"
    db_password = "olok"
    db_host = "10.0.1.5"
    db_port = "5432"

    # Se connecter à la base de données
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)

    # Créer un curseur pour exécuter des requêtes SQL
    cur = conn.cursor()

    # Exécuter une requête SQL pour récupérer l'adresse e-mail associée à l'ID
    cur.execute("SELECT email FROM authentification_user WHERE id = %s", (id,))

    # Récupérer le résultat de la requête
    result = cur.fetchone()

    # Vérifier si une adresse e-mail a été trouvée
    email = None
    if result is not None:
        email = result[0]

    # Fermer le curseur et la connexion à la base de données
    cur.close()
    conn.close()

    return email

def get_element(id):
    client = create_mongo_client()

    # Sélectionner la base de données
    db = client["olok"]

    # Sélectionner la collection
    collection = db["bunchOfKeys"]

    # Récupérer l'élément correspondant à l'ID
    document = collection.find_one({"_id": id})

    # Vérification si un document a été trouvé
    if document is not None:
        # On retire les keysIDs
        return (True, document)
    else:
        collection = db["keys"]
        document = collection.find_one({"_id": id})

        if document is not None:
            return (False, document)
    return None

def send_mail(log):

    # Extraire les informations du log
    info = log.split(" - ")
    user_id = info[3]
    action = info[2]
    element_id = info[4]
    timestamp = info[0]

    body_start = f"Le {timestamp} une action suspeccte a ete detecte ({action}) sur l'élément suivant:\n"

    # Récupération du destinataire
    to_addr = get_mail(user_id)

    if to_addr is None:
        print(f"Impossible de trouver l'adresse e-mail pour l'utilisateur {user_id}")
        return

    # Récupération du document lié à l'ID
    res = get_element(element_id)

    if res is None:
        print(f"Impossible de retrouver l'élément lié a cet id")
        return

    if res[0]:
        body_end = f"\tTrousseau de clés: {res[1]['name']}\n"
    else:
        body_end = f"\tClé du domaine: {res[1]['domain']}\n"
        #body_end += f"\t\Utilisateur: {res[1]['username']}\n"

    body = body_start + body_end

    # Créer le message
    message = f"Subject : {subject}\n\n{body}"

    # Encoder le message en UTF-8
    message_bytes = message.encode("utf-8")

    # Se connecter au serveur SMTP et envoyer le message
    with smtplib.SMTP(server, port) as smtp:
        smtp.sendmail(from_addr, to_addr, message_bytes)

#send_mail("2024-04-11 17:53:24,861 - INFO - new - 3 - 6606decc5379a50c0e3185b3")