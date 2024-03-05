i

### Représentation des données dans la base de donnée NoSQL

La logique pour parvenir à la représentation en base de données des mots de passe de l'utilisateur est la suivante :

Un utilisateur a un porte-trousseau qui est composé de trousseaux de clés. Ce trousseau est composé d'au moins une clé. Ainsi le porte clé ⊃ trousseau ⊃ clés.

#### Clé

```json
{
    "id": "1234",
    "domain": "domaine.domaine",
    "username": "john_doe",
    "password": "password"
}
```

#### trousseau
```json
{
    "id": "123456789",
    "name": "trousseau1",
    "role": "favorite | default | normal",
    "description": "Ceci est une description",
    "deletable": true or false,
    "editable": true or false,
    "keysIDs": [
        "keyId1",
        "keyId2"
    ]
}
```

#### porte-trousseau
```json
{
    "id": "123456789123",
    "idOwner": "65431",
    "bunchOfKeysIDs": [
        "bunchOfKeysId1",
        "bunchOfKeysId2"
    ]
}
```

Proposition: l'utilisateur a le droit à 1 seul trousseau favoris créé par défaut et un porte-trousseau normal composé lui de plusieurs trousseaux.

#### Frontend request

Pour le frontend on pourra renvoyer une structure plus conséquente mais complète comme représenté ci-dessous:

```json
{
    "bunchOfKeys": [
        {
            "id": "123456789",
            "name": "trousseau1",
            "description": "Ceci est une description",
            "role": "normal",
            "keys": [
                {
                    "id": "1234",
                    "domain": "domaine1.domaine",
                    "username": "john_doe",
                },
                {
                    "id": "5678",
                    "domain": "domaine2.domaine",
                    "username": "john_doe",
                }
            ]
        },
        {
            "id": "987654321",
            "name": "trousseau2",
            "description": "Ceci est une description",
            "role": "normal",
            "keys": [
                {
                    "id": "8765",
                    "domain": "domaine3.domaine",
                    "username": "john_doe",
                },
                {
                    "id": "4321",
                    "domain": "domaine4.domaine",
                    "username": "john_doe",
                }
            ]
        }
    ]
}
```