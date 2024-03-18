### Représentation des données dans la base de donnée NoSQL

La logique pour parvenir à la représentation en base de données des mots de passe de l'utilisateur est la suivante :

Un utilisateur a un porte-trousseau qui est composé de trousseaux de clés. Ce trousseau est composé d'au moins une clé. Ainsi le porte clé ⊃ trousseau ⊃ clés.

#### Clé

```json
{
    "id": "1234",
    "domain": "domaine.domaine",
    "username": "john_doe",
    "password": "password",
    "signature": "signature"
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

### Format des logs

Les logs vont servir de données pour entrainer une IA sur le comportement des utilisateurs afin de lever des alertes en cas de variations. Ces logs se limiteront aux actions des utilisateurs, c'est-à-dire qu'on ne considère pas pour ces logs des tentatives frauduleuses comme le brute-force, ddos, etc... . Les formats selon l'action effectué sont les suivants:

#### Logs concernant les clés

##### Création d'une nouvelle clé

```txt
<Timestamp> new key in <bunchOfKeysId> with id <keyId> for user <userId>
```

##### Modification d'une clé

```txt
<Timestamp> modification of key <keyId> in <bunchOfKeysId> for user <userId>
```

##### Suppression d'une clé

```txt
<Timestamp> deletion of key <keyId> in <bunchOfKeysId> for user <userId>
```

##### Récupération d'une clé

```txt
<Timestamp> get key <keyId> from bunchOfKeys <bunchOfKeysId> for user <userId>
```

#### Logs concernant les porte-clés

##### Création d'un porte clé

```txt
<Timestamp> new bunchOfKeys <bunchOfKeysId> for user <userId>
```

##### Modification d'un porte clé

```txt
<Timestamp> modification of bunchOfKeys <bunchOfKeysId> for user <userId>
```

##### Suppression d'un porte clé

```txt
<Timestamp> deletion of bunchOfKeys <bunchOfKeysId> for user <userId>
```

##### Suppression d'un porte clé

```txt
<Timestamp> get bunchOfKeys <bunchOfKeysId> for user <userId>
```

##### Changement clé de porte clé

```txt
<Timestamp> change key <keyId> spot from bunchOfKeys <bunchOfKeysId> to <bunchOfKeysId> for user <userId>
```

#### Logs concernant l'authentification'

##### Création d'un compte

```txt
<Timestamp> creation of an account <userId> from <countryCode>
```

##### Connexion à un compte

```txt
<Timestamp> login account <userId> from <countryCode>
```

#### Logs concernant le profil

##### Suppression d'un compte

```txt
<Timestamp> deletion of account <userId> from <countryCode>
```

##### Modification du profil

```txt
<Timestamp> modification data account <userId>
```

##### Changement de mot de passe

```txt
<Timestamp> modification password account <userId>
```

