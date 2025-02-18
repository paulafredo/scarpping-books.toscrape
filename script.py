import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urljoin
import json

base_url = "https://books.toscrape.com/"


def main():

    # Effectuer une requête pour obtenir la page principale
    response = requests.get(base_url)
    page_soup = BeautifulSoup(response.text, "html.parser")

    # Trouver la section des catégories
    categories_section = page_soup.find("div", class_="side_categories")
    categories_list = categories_section.find("ul").find("li").find("ul")

    # Extraire les noms des catégories et leurs liens
    category_links = categories_list.find_all("a")
    category_names = [category.text.strip() for category in category_links]
    full_url = [urljoin(base_url, link["href"]) for link in category_links]

    index = 0
    min_books_count = float(
        "inf"
    )  # Initialisation avec un nombre très grand pour trouver le minimum
    dict_categorie = []

    # Boucle pour trouver la catégorie avec le moins de livres
    for i in range(len(category_names)):
        try:
            response = requests.get(full_url[i])
            soup = BeautifulSoup(response.text, "html.parser")
            article = soup.find_all("article", class_="product_pod")
            books = len(article)
            dict_categorie.append(
                {
                    "index": i+1 , 
                    "name ": category_names[i],
                    "number ": books,
                    "links": full_url[i],
                    "product by" :"THUG"
                }
            )

            # Vérifier si le formulaire et le nombre de livres sont présents
            if books:
                nb_livre = books
                if nb_livre:
                    if nb_livre < min_books_count:
                        min_books_count = nb_livre
                        index = i
        except requests.exceptions.RequestException as e:
            print(
                f"Erreur lors de la requête pour la catégorie {category_names[i]} : {e}"
            )
        except Exception as e:
            print(
                f"Erreur lors du traitement de la catégorie {category_names[i]} : {e}"
            )

    # Afficher le résultat
    if min_books_count != float("inf"):
        print(
            f"La catégorie avec le moins de livres est '{category_names[index]}' avec {min_books_count} livres."
        )
    else:
        print("Aucune catégorie n'a pu être traitée correctement.")
    pprint(dict_categorie)
    with open(
        "response.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            dict_categorie, f, ensure_ascii=False, indent=4
        )  # Convertit en JSON formaté

    # titles = [a ["title"] for a in soup.find_all('a',title = True ) ]
    # # pprint(titles)


if __name__ == "__main__":
    main()
