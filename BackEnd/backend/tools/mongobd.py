import pymongo
from bson import ObjectId

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

def create_KeysList(db, KeysIDs):
    result = []

    for keyID in KeysIDs:
        print(keyID)
        key = db["keys"].find_one({"_id": keyID})
        key.pop("password")
        key.pop("signature")
        key["keyId"] = str(key["_id"])
        key.pop("_id")
        result.append(key)

    print(result)

    return result

def create_BunchOfKeysData(db, bunchOfKeys):
    result = []

    # On récupère le trousseau de clés
    collection = db["bunchOfKeys"]
    bunchOfKeys = collection.find_one({"_id": ObjectId(bunchOfKeys)})

    # On créé la  structure contenant les données des clés
    keysData = create_KeysList(db, bunchOfKeys.get("keysIDs", []))
    bunchOfKeys.pop("deletable")
    bunchOfKeys.pop("editable")
    bunchOfKeys.pop("keysIDs")
    bunchOfKeys["bunchOfKeysId"] = str(bunchOfKeys["_id"])
    bunchOfKeys.pop("_id")
    bunchOfKeys["keys"] = keysData
    result.append(bunchOfKeys)

    return result
