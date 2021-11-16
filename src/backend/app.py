# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 17:31:47 2021

@author: simon.ak
"""

# --------------------------------------------------------------------------- #
# ------------------------- Librairies Importation -------------------------- #
# --------------------------------------------------------------------------- #

import pandas as pd
import re
from collections import Counter

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from urllib.parse import unquote
import pickle

# --------------------------------------------------------------------------- #
# -------------------- Naïve Bayes Model Implementation --------------------- #
# --------------------------------------------------------------------------- #

def dataframePreparation(path:str, sep="\t"):
    df = pd.read_csv(path, sep=sep, names=['Label', 'Email'])
    spam = df[df['Label'] == 'spam'].reset_index(drop=True)
    ham = df[df['Label'] == 'ham'].reset_index(drop=True)
    df['Email'] = df['Email'].str.replace('\W', ' ')
    df['Email'] = df['Email'].str.lower()
    
    return df, spam, ham

def cleanString(str_:str):
    return re.sub(r'[^\w\s]', '', str_).lower()

def make_Dictionary(df, most_common_words=3000):
    """
    Réalisation d'un dictionnaire récapitulant les mots les plus utilisés et le nombre de fois où ces mots sont utilisés.

    Paramètres
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame dont nous souhaitons obtenir le dictionnaire.
    most_common_words : int
        Nombre de mots dont nous souhaitons afficher (par défaut, égal à 3000).

    Returns
    -------
    dictionary : list
        Liste contenant des tuples du type : (Mot, Nb d'Utilisation).
    """
    all_words = []
    for oneEmail in df['Email']: # We go through all emails
        for word in oneEmail.split(): # We go through the words in an email
            all_words.append(word) # We add it to our list
    dictionary = Counter(all_words) # Using the `Counter()` function, we create a dictionary with the registered words

    for item in list(dictionary): # For each word in the dictionary...
        if item.isalpha() == False: # If the word does not consist of alphabetical letters...
            del dictionary[item] # We delete it
        elif len(item) == 1: # If the word is only one element...
            del dictionary[item] # We delete it
    dictionary = dictionary.most_common(most_common_words) # We keep only the `most_common_words` most used words in our dictionary.
    return dictionary

def extract_features(list_emails, dictionary):
    """
    Comptage du nombre de présence des mots utilisés dans chaque email.
    Elle retourne ensuite un dataset qui regroupe toutes ces informations.

    Paramètres
    ----------
    list_emails: list
        Liste des emails.
    dictionary : list
        Dictionnaire de mots créé grâce à la fonction make_Dictionary().

    Returns
    -------
    features_matrix : pandas.core.frame.DataFrame
        DataFrame avec l'extraction des features.
    """
    features_matrix = pd.DataFrame(columns=[d[0] for i, d in enumerate(dictionary)], index=range(len(list_emails))).fillna(0) # Creation of a DataFrame filled with 0
    
    docID = 0
    for one_email in list_emails: # We go through all the emails
        list_words_in_the_email = one_email.split()
        for word in list_words_in_the_email: # We go through the words in an email
            for i, d in enumerate(dictionary): # For each word in the dictionary...
                if d[0] == word: # Equal to 1 if the dictionary word is present in the mail, 0 otherwise.
                    features_matrix.loc[docID, d[0]] = 1
                    
        docID += 1
    return features_matrix

def indicator_function_of_word_in_specific_type_email(spam_or_ham_extracted_dataframe):
    """
    Cette fonction calcule la fonction indicatrice dans tous les spams/hams.
    Elle retourne ensuite un dataset récapitulant ces données.

    Paramètres
    ----------
    spam_or_ham_dataframe : pandas.core.frame.DataFrame
        DataFrame de nos emails donc l'extraction de features a été réalisée.

    Returns
    -------
    indicator_df : pandas.core.frame.DataFrame
        DataFrame avec le nombre d'utilisation d'un mot dans les emails.
    """
    columns_name = spam_or_ham_extracted_dataframe.columns # Retrieving dictionary words

    liste = list( spam_or_ham_extracted_dataframe.sum() ) # For each word, we count the number of emails where this word is present

    dico = {columns_name[i]:liste[i] for i in range(len(liste))}
    indicator_df = pd.DataFrame(data=dico, columns=columns_name, index=[0]) # Creation of a DataFrame to put in the calculations made previously
    
    return(indicator_df)

def calcul_phi_n_sachant_type_Email(df_indicator, df_spam_or_ham, laplace_smoothing=1) :
    """
    Calcul des paramètres pour Phi_n sachant SPAM ou HAM.

    Paramètres
    ----------
    df_indicator : pandas.core.frame.DataFrame
        DataFrame avec les occurences calculées grâce à la fonction indicator_function_of_word_in_specific_type_email().
    df_spam_or_ham : pandas.core.frame.DataFrame
        DataFrame listant les spams ou les hams.
    laplace_smoothing : int
        Laplace Smoothing (par défaut, égal à 1).
    
    Returns
    -------
    df_parameters : pandas.core.frame.DataFrame
        DataFrame regroupant les calculs de paramètres pour chaque mot.
    """
    columns_names = df_indicator.columns # Retrieving dictionary words

    liste = list(df_indicator[col][0] for col in df_indicator.columns) # Converting our DataFrame to a list (more convenient)

    dico = {columns_names[i]:((liste[i]+laplace_smoothing)/(len(df_spam_or_ham)+2*laplace_smoothing)) for i in range(len(columns_names))} # Calculation of the two parameters using the course formula
    df_parameters = pd.DataFrame( data=dico, columns=columns_names, index=range(1) ) # Creation of a DataFrame to put in the calculations made previously

    return(df_parameters)

def naiveBayes_fit(X_train, spam_train, ham_train, spam_train_clean, ham_train_clean, laplace_smoothing=0.1):
    """
    Prédiction des emails à l'aide de l'entraînement du modèle avec les 3 paramètres calculés.

    Paramètres
    ----------
    X_train : pandas.core.frame.DataFrame
        DataFrame avec les emails du training set.
    spam_train : pandas.core.frame.DataFrame
        DataFrame contenant tous les spams du training set.
    spam_train_clean : pandas.core.frame.DataFrame
        DataFrame composé des features extraites des spams.
    ham_train_clean : pandas.core.frame.DataFrame
        DataFrame composé des features extraites des hams.
    laplace_smoothing : float
        Valeur du Laplace Smoothing (par défaut, égal à 0.1)
    
    Returns
    -------
    phi_y : float
        Paramètre représentant P(Y = 1).
    phi_n_given_spam : pandas.core.frame.DataFrame
        DataFrame composé du paramètre représentant P(Xn = 1 | Y = 1).
    phi_n_given_ham : pandas.core.frame.DataFrame
        DataFrame composé du paramètre représentant P(Xn = 1 | Y = 0).
    """
    
    # Calculation of word occurrences
    number_occurrences_of_word_in_all_spams = indicator_function_of_word_in_specific_type_email(spam_train_clean)
    number_occurrences_of_word_in_all_hams = indicator_function_of_word_in_specific_type_email(ham_train_clean)

    # Calculation of parameters
    phi_y = ( len(spam_train) + laplace_smoothing ) / ( len(X_train) + 2*laplace_smoothing )
    phi_n_given_spam = calcul_phi_n_sachant_type_Email(number_occurrences_of_word_in_all_spams, spam_train, laplace_smoothing)
    phi_n_given_ham = calcul_phi_n_sachant_type_Email(number_occurrences_of_word_in_all_hams, ham_train, laplace_smoothing)

    return( phi_y, phi_n_given_spam, phi_n_given_ham )

def naiveBayes_predict(str_, phi_y, phi_n_given_spam, phi_n_given_ham):
    """
    Prédiction des emails à l'aide de l'entraînement du modèle avec les 3 paramètres calculés.

    Paramètres
    ----------
    X_test : pandas.core.frame.DataFrame
        DataFrame avec les emails du testing set.
    phi_y : float
        Paramètre représentant P(Y = 1).
    phi_n_given_spam : pandas.core.frame.DataFrame
        DataFrame composé du paramètre représentant P(Xn = 1 | Y = 1).
    phi_n_given_ham : pandas.core.frame.DataFrame
        DataFrame composé du paramètre représentant P(Xn = 1 | Y = 0).
    
    Returns
    -------
    y_pred : pandas.core.frame.DataFrame
        DataFrame regroupant les prédictions pour chaque email du testing set.
    """
    columns_name = phi_n_given_spam.columns.tolist()

    listWords = cleanString(str_).split() # Separate words in an string
    produit_spam, produit_ham = 1, 1

    for oneWord in listWords: # We go through the words in the string
        if oneWord in columns_name: # If the word is present in the dictionary
            produit_spam *= phi_n_given_spam[oneWord][0] # Product of probabilities for spam
            produit_ham *= phi_n_given_ham[oneWord][0] # Product of probabilities for ham
                
    if (produit_spam*phi_y / (produit_spam*phi_y + produit_ham*(1-phi_y))) > (produit_ham*(1-phi_y) / (produit_spam*phi_y + produit_ham*(1-phi_y))):
        return "Spam"
    else:
        return "Ham"

# --------------------------------------------------------------------------- #
# --------------------------- Creation of the Model -------------------------- #
# --------------------------------------------------------------------------- #

# df, spam, ham = dataframePreparation('messages.txt')
# dictionary = make_Dictionary(df)
# spam_clean = extract_features(spam['Email'], dictionary)
# ham_clean = extract_features(ham['Email'], dictionary)
# phi_y, phi_n_given_spam, phi_n_given_ham = naiveBayes_fit(df, spam, ham, spam_clean, ham_clean, 0.1)

# with open('myVariables.txt', 'wb') as f:
#     pickle.dump([phi_y, phi_n_given_spam, phi_n_given_ham], f)

# --------------------------------------------------------------------------- #
# ---------------------------- Roads for the API ---------------------------- #
# --------------------------------------------------------------------------- #

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)
@app.route("/api", methods = ['GET'])
@cross_origin()
def homepage():
    return jsonify({'message': [404, 'Not Found']})


@app.route("/prediction/<stringToPredict>", methods = ['GET'])
@cross_origin()
def prediction(stringToPredict):
    stringToPredict = unquote(stringToPredict)
    with open('myVariables.txt', 'rb') as f:
        phi_y, phi_n_given_spam, phi_n_given_ham = pickle.load(f)
    
    prediction = naiveBayes_predict(stringToPredict, phi_y, phi_n_given_spam, phi_n_given_ham)
    
    return jsonify({'prediction':prediction})

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()