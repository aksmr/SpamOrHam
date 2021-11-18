# Spam or Ham
Site Internet permettant de savoir si un texte est considéré comme un spam ou non.

## Lien vers le site
Voir le lien suivant : [`https://is-it-spam-or-ham.herokuapp.com/`](https://is-it-spam-or-ham.herokuapp.com/) !

## Composition du repository
Le repository est composé de deux éléments :
* Le backend
* Le frontend

### Backend
Dans ce dossier, nous retrouvons le fichier `app.py`. Dans ce fichier, nous trouvons le modèle génératif Naïve Bayes entraîné permettant de différencier un texte d'une classe `SPAM` d'une classe `HAM`.

La réalisation du modèle est composée de plusieurs étapes :
1. Construction d'un dictionnaire de mots provenant d'un ensemble d'emails donnés.
2. Pour chaque email, construction d'un feature vecteur qui indique quel mot du disctionnaire apparaît dans l'email.
3. Design d'un modèle génératif pour le problème:
  * Calcul de Φ_y = P(Y = 1)
  * Calcul de Φ_n_given_spam = P(Xn = 1 | Y = 1)
  * Calcul de Φ_n_given_ham = P(Xn = 1 | Y = 0)

save file
