from pyson.pylib.forms import *

class Role(Forms):
    name = Input(name="name", maxlength=100, label="name")
    submit = Input(type="submit", value="valider",  name="valider", onclick="")
    enum=[name, submit]


class Billet(Forms):
    Titre = Input(name="Titre", maxlength=100, label="Titre")
    Corps = TextArea(name="Corps", maxlength=1000, label="Corps")
    Auteur = Input(name="Auteur", maxlength=100, label="Auteur")
    Categorie = Input(name="Categorie", maxlength=100, label="Categorie")
    submit = Input(type="submit", value="valider",  name="valider", onclick="")
    enum=[Titre,Corps,Auteur,Categorie, submit]


class Category(Forms):
    nom = Input(name="nom", maxlength=100, label="nom")
    submit = Input(type="submit", value="valider",  name="valider", onclick="")
    enum=[nom, submit]


class Groupe(Forms):
    nom = Input(name="nom", maxlength=100, label="nom")
    submit = Input(type="submit", value="valider",  name="valider", onclick="")
    enum=[nom, submit]


class Users(Forms):
    nom = Input(name="nom", maxlength=100, label="nom")
    prenom = Input(name="prenom", maxlength=100, label="prenom")
    pseudo = Input(name="pseudo", maxlength=100, label="pseudo")
    password = Input(name="password", maxlength=100, label="password")
    submit = Input(type="submit", value="valider",  name="valider", onclick="")
    enum=[nom,prenom,pseudo,password, submit]


class Comment(Forms):
    Titre = Input(name="Titre", maxlength=100, label="Titre")
    Corps = TextArea(name="Corps", maxlength=1000, label="Corps")
    Auteur = Input(name="Auteur", maxlength=100, label="Auteur")
    Billet = Input(name="Billet", maxlength=100, label="Billet")
    submit = Input(type="submit", value="valider",  name="valider", onclick="")
    enum=[Titre,Corps,Auteur,Billet, submit]

