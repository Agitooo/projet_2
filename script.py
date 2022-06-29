import requests
from bs4 import BeautifulSoup
import csv

# site a scrapper
url = "http://books.toscrape.com/"
response = requests.get(url)
page = response.content
soup = BeautifulSoup(page, "html.parser")

# Ne fontionne que sur la page principale
def get_all_categorie():
    # On récupère toutes les catégories de la page principale
    toutes_categorie_ul = soup.find_all("ul", class_="nav-list")

    categorie = []

    for bloc_categorie in toutes_categorie_ul:
        all_a_cat = bloc_categorie.find_all("a")
        for a_info in all_a_cat:
            categorie.append({'nom': a_info.get_text().strip(), 'url': a_info.get('href')})
    # On supprime la 1ere catégorie qui est un titre
    categorie.pop(0)
    # categorie = Tableau des catégories + url associées
    return categorie


# tab_categotie = get_all_categorie()
# print(tab_categotie)


# charger la donnée dans un fichier csv
def charger_donnees(
        nom_fichier,
        en_tete,
        detail_livre
):
    with open(nom_fichier, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        writer.writerow(
            [
                (','.join(detail_livre))
            ]
        )


def get_detail_livre(url_detail_livre):

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

    data_return = [
        product_page_url, universal_product_code, price_including_tax, price_excluding_tax, number_available,
        title, product_description, category, review_rating, image_url
    ]

    return data_return


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

# Url du détail du 1er livre
url_detail_livre = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
detail_livre = get_detail_livre(url_detail_livre)

charger_donnees(
    "partie_1_detail_livre.csv",
    en_tete,
    detail_livre
)
