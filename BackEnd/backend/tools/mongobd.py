import pymongo

def create_mongo_client():
    # Création d'une nouvelle connexion à la base de données MongoDB
    return pymongo.MongoClient(
        "mongodb://{username}:{password}@10.0.1.4:27017/".format(
            username="olok",
            password="olok",
        )
    )

def create_bunchOfKeysHolder(idOwner):
    # Création d'un porte trousseau
    bunchOfKeysHolder = {
        "idOwner": idOwner,

        "bunchOfKeysIDs": []
    }
    return bunchOfKeysHolder

def create_bunchOfKeys(name, description, deletable, editable, role):
    # Création d'un trousseau
    bunchOfKeys = {
        "name": name,
        "description": description,
        "deletable": deletable,
        "editable": editable,
        "role": role,
        "keysIDs": []
    }
    return bunchOfKeys
