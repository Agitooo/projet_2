# Projet 2 python openclassrooms

Ce script permet de récupérer les informations des livres sur le site http://books.toscrape.com/.

La version de **Python** à utiliser : _**3.10.5**_

# **ENVIRONNEMENT VIRTUEL**

Création de l'environnement virtuel :


Pour créer l'environnement virtuel il faut exécuter la commande suivante à la racine du projet :

    python -m venv env


Puis la commande suivante pour démarrer l'environnement :

-   sous Linux

    
    source env/bin/activate

-   sous Windows


    env/Scripts/activate.bat


Pour installer les packages spécifiés dans le fichier requirements.txt il faut exécuter la commande suivante :

    pip install -r requirements.txt


# **SCRIPT**

Lors de l'exécution du script _script.py_, il y aura un menu dans la console, qui permettra de choisir 
ce que l'on souhaite effectuer

Il y a plusieurs possibilités :

    1 -  Récupérer les informations d'un livre via son URL (choix 1)
    2 -  Récupérer l'ensemble des informations des livres d'une catégorie (choix 2)
    3 -  Récuperer l'ensemble des informations des livres de toutes les catégories (choix 3)
    0 -  Quitter (choix 0)

Il suffit d'écrire 1, 2, 3 ou exit

Dans chacun des choix 1, 2 ou 3, il est également possible de choisir si l'on souhaite récupérer les images de 
couverture. 
Pour se faire il suffira de préciser 'y' ou 'n' lorsque la question 
"Voulez-vous télécharger les images (y/n)" sera posée

Une fois le choix effectuer, deux questions seront posées :

Le choix '1'

- Saisir l'URL du livre souhaité
- Souhait de l'image 'y' ou 'n'

Une fois terminé, il y aura un fichier CSV avec les informations du livre 
et l'image de la couverture si 'y' a été saisi.

Le choix '2'

- Saisir la catégorie souhaitée
- Souhait de l'image 'y' ou 'n'

Une fois terminé, un dossier du nom de la catégorie sera créé et dans ce dossier, se trouvera le fichier CSV
avec les informations des livres de la catégorie et un dossier pictures, 
avec les images à l'intérieur si le choix était 'y'.

Le choix '3'

- Souhait de l'image 'y' ou 'n'

Une fois terminé, il y aura toutes les catégories récupérées, chacune dans un dossier propre contenant le CSV
et le dossier pictures de chacune des images des livres de la catégorie si le choix 'y' a été fait.

Le choix 'exit' permet juste de quitter le script