# Spam or Ham
Site Internet permettant de savoir si un texte est considéré comme un spam ou non.

## Lien vers le site
Voir ci-joint : [`https://is-it-spam-or-ham.herokuapp.com/`](https://is-it-spam-or-ham.herokuapp.com/)

## Composition du repository
Le repository est composé de deux éléments :
* Le backend
* Le frontend

### Backend
#### Présentation Générale
Dans ce dossier, nous retrouvons le fichier `app.py`. Dans ce fichier, nous trouvons le modèle génératif Naïve Bayes entraîné permettant de différencier un texte d'une classe `SPAM` d'une classe `HAM`.

#### Étapes de création du modèle
La réalisation du modèle est composée de plusieurs étapes :
1. Construction d'un dictionnaire de mots provenant d'un ensemble d'emails donnés.
2. Pour chaque email, construction d'un feature vecteur qui indique quel mot du disctionnaire apparaît dans l'email.
3. Design d'un modèle génératif pour le problème:
  * Calcul de `Φ_y` = `P(Y = 1)`
  * Calcul de `Φ_n_given_spam` = `P(Xn = 1 | Y = 1)`
  * Calcul de `Φ_n_given_ham` = `P(Xn = 1 | Y = 0)`

#### Prédictions
Une fois ces trois paramètres calculés, le modèle est entraîné et opérationnel. Nous n'avons plus qu'à enregistrer de manière binaire dans un fichier. Ce fichier sera lu à chaque fois que nous souhaitons réaliser une prédiction.

Nous utilisons la librairie `Flask` pour créer nos routes — principalement la route `/prediction/<stringToPredict>` — qui seront utilisées par les requêtes HTTP côté [frontend](#frontend).

#### Lancement du serveur
Pour lancer le serveur, il est nécessaire de saisir le code suivant à la racine du dossier `backend` dans une invite de commande :
```PowerShell
src\backend> flask run
```

### Frontend
#### Présentation Générale
Le frontend est réalisé avec la bibliothèque Javascript nommée `ReactJS`.

#### Lancement du serveur
Pour lancer le serveur, il est nécessaire de saisir le code suivant à la racine du dossier `frontend` dans une invite de commande :
```PowerShell
src\frontend> npm start
```
