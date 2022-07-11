import requests
from bs4 import BeautifulSoup
import csv
import os

url = "http://books.toscrape.com/"


def get_menu():
    return input("Veuillez selectionner votre action parmis les choix suivants \n "
                 "1    - Récupérer les détails d'un livre par son url \n "
                 "2    - Récupérer les livres d'une catégorie selectionnée \n "
                 "3    - Récupération de l'integralité des livres du site \n "
                 "exit - Quitter\n "
                 " ").strip().lower()


def get_select_url():
    return input("Veuillez saisir l'url du livre : ").strip().lower()


# On affiche l'input de selection de la catégorie
def input_select_cat():
    return input("Veuillez saisir la catégorie à récuperer : ").strip().lower()


def with_picture():
    text_picture = "Voulez-vous télécharger les images (y/n) : ".strip().lower()
    with_picture_choice = input(text_picture)
    while not (with_picture_choice in allowed_with_picture):
        print("Le choix n'est pas valide")
        with_picture_choice = input(text_picture)

    if with_picture_choice == "y":
        with_picture = True
    else:
        with_picture = False

    return with_picture


# On récupère la clé de la valeur recherchée dans le dictionnaire si elle existe, sinon none
def key_in_dict(dictionary, key, search):
    return next((i for i, item in enumerate(dictionary) if item[key] == search), None)


def get_dict_all_category():
    # site a scrapper
    response = requests.get(url)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")

    # On récupère toutes les catégories de la page principale
    toutes_categorie_ul = soup.find_all("ul", class_="nav-list")

    categorie = []

    for bloc_categorie in toutes_categorie_ul:
        all_a_cat = bloc_categorie.find_all("a")
        for a_info in all_a_cat:
            categorie.append({'nom': a_info.get_text().strip().lower(), 'url': a_info.get('href')})
    # On supprime la 1ere catégorie qui est un titre
    categorie.pop(0)
    # categorie = Tableau des catégories + url associées
    return categorie


# charger la donnée dans un fichier csv
def charger_donnees(
        nom_fichier,
        en_tete,
        detail_livre
):
    with open(nom_fichier, 'w', encoding="utf8", newline='') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        # Si le fichier est vide, alors on met l'entete
        if os.path.getsize(nom_fichier) == 0:
            writer.writerow(en_tete)
        writer.writerows([detail_livre])


def get_detail_livre(url_detail_livre, with_picture=False, cat_dir=""):

    response_detail_livre = requests.get(url_detail_livre)
    page_detail_livre = response_detail_livre.content
    soup_detail_livre = BeautifulSoup(page_detail_livre, "html.parser")

    product_page_url = url_detail_livre

    # Tableau des infos produit
    product_information = soup_detail_livre.find_all("td")

    universal_product_code = product_information[0].get_text().strip()
    price_including_tax = product_information[3].get_text().strip()[1:]
    price_excluding_tax = product_information[2].get_text().strip()[1:]
    number_available = product_information[5].get_text().strip()

    # Le titre du livre est dans la seule balise h1 de la page
    title = soup_detail_livre.find("h1").get_text().strip()

    product_description = soup_detail_livre.find_all('p')[3].get_text().strip()

    # La catégorie est dans le fil d'ariane
    category = soup_detail_livre.find_all("a")[3].get_text().strip()

    review_rating = soup_detail_livre.find('p', class_="star-rating").get('class')[1]

    # l'url de l'image n'est pas absolue et commence par ../..
    # donc on les retire et on concatène avec l'url du site pour avoir l'url complete
    image_url = url + soup_detail_livre.find('img').get('src')[6:]

    if with_picture:
        name_picture = title.lower() + ".jpg"
        char_replace = "!#$%^&*(),': ’"
        for char in char_replace:
            name_picture = name_picture.replace(char, "_")

        if cat_dir != "":
            name_picture = cat_dir + "/pictures/" + name_picture

        f = open(name_picture, "wb")
        picture = requests.get(image_url)
        f.write(picture.content)
        f.close()

    data_return = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                   number_available, product_description, category, review_rating, image_url]
    return data_return


def get_list_book_by_category(category_url, link=None, page="index.html"):

    reponse_category_par_page = requests.get(category_url + page)
    page_category_par_page = reponse_category_par_page.content
    soup_category_par_page = BeautifulSoup(page_category_par_page, "html.parser")

    all_link_livre = soup_category_par_page.find_all("div", class_="image_container")

    if link is None:
        link = []
    for bloc_link_livre in all_link_livre:
        all_a_livre = bloc_link_livre.find_all("a")
        for link_livre in all_a_livre:
            link.append(url + 'catalogue/' + link_livre.get('href')[9:])

    have_pagination = soup_category_par_page.find_all("li", class_="next")
    if have_pagination:
        for link_pagination in have_pagination:
            a_pagination = link_pagination.find_all("a")
            url_pagination = a_pagination[0].get('href')
            # On rappelle la fonction dans laquelle on
            # est s'il y a une page suivante et on rajoute les livres a la suite
            link = get_list_book_by_category(category_url, link, url_pagination)

    return link


def get_all_book_detail(category_dict, with_picture=False):

    for category in category_dict:
        url_category_split = category['url'][:-10]
        category_url = url + url_category_split
        # retrait de index et rajouté param fontion par defaut page1.html
        all_link_livre = get_list_book_by_category(category_url)
        cat_dir = category["nom"].strip().replace(" ", "_").lower()
        if not os.path.exists(cat_dir):
            os.makedirs(cat_dir)
        if with_picture and not os.path.exists(cat_dir + "/pictures"):
            os.makedirs(cat_dir + "/pictures")
        with open(cat_dir + '/' + category["nom"] + ".csv", 'w', encoding="utf8", newline='') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            # Si le fichier est vide, alors on met l'entete
            if os.path.getsize(cat_dir + '/' + category["nom"] + ".csv") == 0:
                writer.writerow(en_tete)
            for link_livre in all_link_livre:
                writer.writerows([get_detail_livre(link_livre, with_picture, cat_dir)])


if __name__ == "__main__":

    url_choice = ""

    # entete du fichier CSV
    en_tete = [
        "product_page_url",
        "universal_product_code (upc)",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url"
    ]

    # On gère le choix du menu principal
    allowed_menu_choice = ["1", "2", "3", "exit"]
    allowed_with_picture = ["y", "n"]

    menu_choice = get_menu()
    index_cat_in_dict = None

    # Tant que le choix est invalide, on demande de ressaisir
    while not(menu_choice in allowed_menu_choice):
        print("Le choix n'est pas valide")
        menu_choice = get_menu()

    if menu_choice == "1":
        url_choice = get_select_url()
        test_url = requests.get(url_choice)
        while test_url.status_code != 200:
            print("URL invalide")
            url_choice = get_select_url()
            test_url = requests.get(url_choice)

        with_picture = with_picture()

        detail_livre = get_detail_livre(url_choice, with_picture, "")
        charger_donnees("detail_livre.csv", en_tete, detail_livre)

    elif menu_choice == "2":
        # On récupère un dictionnaire de toutes les catégories
        all_category = get_dict_all_category()
        # On affiche l'input de selection de la catégorie
        cat_select = input_select_cat()
        # On récupère la clé de la catégorie recherchée dans le dictionnaire de toutes les catégories, sinon None
        index_cat_in_dict = key_in_dict(all_category, "nom", cat_select)

        # Tant qu'on a pas de clé trouvée, on redemande de saisir la catégorie, jusqu'a en avoir une valide
        while index_cat_in_dict is None:
            print("La catégorie saisie n'éxiste pas")
            cat_select = input_select_cat()
            index_cat_in_dict = key_in_dict(all_category, "nom", cat_select)

        with_picture = with_picture()

        get_all_book_detail([all_category[index_cat_in_dict]], with_picture)

    elif menu_choice == "3":
        # On récupère un dictionnaire de toutes les catégories
        all_category = get_dict_all_category()

        with_picture = with_picture()

        get_all_book_detail(all_category, with_picture)

    elif menu_choice == "exit":
        exit()
