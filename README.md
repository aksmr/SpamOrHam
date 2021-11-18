# Spam or Ham
Website that lets you know if a text is considered spam or not.

## Informations
- This project was done by myself from A to Z.
- Link to the site: [`https://is-it-spam-or-ham.herokuapp.com/`](https://is-it-spam-or-ham.herokuapp.com/)

## Composition of the repository
The repository is composed of two elements:
* The backend
* The frontend

### Backend
#### General Overview
In this file we find the `app.py` file. In this file we find the trained Naïve Bayes generative model for differentiating text from a `SPAM` class from a `HAM` class.

#### Steps in creating the model
The creation of the model consists of several steps:
1. Building a dictionary of words from a given set of emails.
2. For each email, construction of a feature vector that indicates which word from the dictionary appears in the email.
3. Design a generative model for the problem:
  * Compute `Φ_y` = `P(Y = 1)`
  * Compute `Φ_n_given_spam` = `P(Xn = 1 | Y = 1)`
  * Compute `Φ_n_given_ham` = `P(Xn = 1 | Y = 0)`

#### Predictions
Once these three parameters have been calculated, the model is trained and operational. All we have to do now is to save it in binary form in a file. This file will be read each time we want to make a prediction.

We use the `Flask` library to create our routes - mainly the `/prediction/<stringToPredict>` route - which will be used by HTTP requests on the [frontend](#frontend) side.

#### Launching the server
To start the server, it is necessary to enter the following code at the root of the `backend` folder in a command prompt:
```PowerShell
src\backend> flask run
```

### Frontend
#### General presentation
The frontend is made with the Javascript library named `ReactJS`.

#### Launching the server
To start the server, it is necessary to enter the following code at the root of the `frontend` folder in a command prompt:
```PowerShell
src\frontend> npm start
```
