### Prérequis

- Docker
- Angular:20.9.0

#### Installation 

##### Windows

```
Docker => installation de docker desktop : https://docs.docker.com/desktop/install/windows-install/
Node => https://nodejs.org/en
```

Pour l'installation d'angular sur powershell:

```
npm install -g @angular/cli
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

##### Ubuntu

Installation de docker (https://docs.docker.com/engine/install/ubuntu/)
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

Installation de node et angular
```
sudo apt update
sudo apt install nodejs
sudo apt install npm

Angular :
npm install -g @angular/cli
```

##### MacOS

Installation de docker => https://docs.docker.com/desktop/install/mac-install/

Installation de Node
```
# download and install Node.js
brew install node@20

# verifies the right Node.js version is in the environment
node -v # should print `v20.12.2`

# verifies the right NPM version is in the environment
npm -v # should print `10.5.0`
```

Installation de Angular
```
npm install -g @angular/cli
```

### Initialisation

#### Initialisation angular

Avant de lancer le projet il est impératif d'installer les modules angular. Pour cela dans le dossier `FrontEnd` lancez la commande suivante :

```
npm i
```

#### Création de dossier pour le ML

Avant tout premier démarrage du projet il est nécessaire de créer trois dossier à l'endroit suivant:

```
./BackEnd/logAnalysis/
```

Les dossiers à créer sont les suivants: `logs`, `models` et `tmp`

### Démarrage

Pour le premier démarrage:
```
docker compose up --build
```

Pour lancer le projet il suffit d'éxecuter cette commande :

```
docker compose up
```

#### Interfaces web

- frontend : `localhost`
- backend : `localhost:8000/swagger`
- mail : `localhost:1080`

#### Bases de données

- mongoDB : `port : 27017`
- postgreSQL : `port : 5432`

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
Possibilité de log : <Timestamp> - login - <userId> - <countryCode>
```

#### Logs concernant le profil

##### Suppression d'un compte

```txt
plus de log car info apparait 1 fois inutile pour analyse comportementale
```

##### Modification du profil

```txt
Possibilité de log : <Timestamp> - modif - <userId> - data
```

##### Changement de mot de passe

```txt
Possibilité de log : <Timestamp> - modif - <userId> - password
```
