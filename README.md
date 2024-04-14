### Initialisation

#### Création de dossier pour le ML

Avant tout premier démarrage du projet il est nécessaire de créer trois dossier à l'endroit suivant:

```
./BackEnd/logAnalysis/
```

Les dossiers à créer sont les suivants: `logs`, `models` et `tmp`

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

Le format général des logs est le suivant :

```txt
<Timestamp> - <new | modif | del | get | login> - <userId> - <elmntId | data | password>
```

##### Création d'une nouvelle clé

```txt
<Timestamp> - new - <userId> - <keyId>
```

##### Modification d'une clé

```txt
<Timestamp> - modif - <userId> - <keyId>
```

##### Suppression d'une clé

```txt
<Timestamp> - del - <userId> - <keyId>
```

##### Récupération d'une clé

```txt
<Timestamp> - get - <userId> - <keyId>
```

#### Logs concernant les porte-clés

##### Création d'un porte clé

```txt
<Timestamp> - new - <userId> - <bunchOfKeysId>
```

##### Modification d'un porte clé

```txt
<Timestamp> - modif - <userId> - <bunchOfKeysId>
```

##### Suppression d'un porte clé

```txt
<Timestamp> - del - <userId> - <bunchOfKeysId>
```

##### Changement clé de porte clé

```txt
plus de log car info inutile
```

##### Récupération des portes clés

```txt
plus de log car info inutile on redondant avec la connexion
```

#### Logs concernant l'authentification'

##### Création d'un compte

```txt
plus de log car info apparait 1 fois inutile pour analyse comportementale
```

##### Connexion à un compte

```txt
<Timestamp> - login - <userId> - <countryCode>
```

#### Logs concernant le profil

##### Suppression d'un compte

```txt
plus de log car info apparait 1 fois inutile pour analyse comportementale
```

##### Modification du profil

```txt
<Timestamp> - modif - <userId> - data
```

##### Changement de mot de passe

```txt
<Timestamp> - modif - <userId> - password
```