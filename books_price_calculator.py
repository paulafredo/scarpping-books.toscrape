import requests
import sys
from selectolax.parser import HTMLParser
from loguru import logger
from typing import List
import re
from urllib.parse import urljoin

# Supprime tous les handlers par défaut
logger.remove()
logger.add("books.log", level="WARNING", rotation="500 KB")
logger.add(sys.stderr, level="INFO")

BASE_URL = "https://books.toscrape.com/"


# Fonctions à coder
# - Fonction pour récupérer les URLs de tous les livres de la bibliothèque
#     - Fonction pour récupérer l'URL de la page suivante
#     - Fonction pour récupérer les URLs des livres sur une page spécifique
# - Récupérer les données directement à partir du HTML ou de la première URL ?

def get_all_books_url(url: str) -> List[str]:
    """Récupère toutes les URLs des livres en parcourant les pages de la bibliothèque."""
    urls = []
    page_number = 0
    while True:
        logger.info(f"Scraping de la page {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la requête HTTP sur la page {url} : {e}")
            continue

        tree = HTMLParser(response.text)
        books_urls = get_all_book_urls_on_page(url , tree)
        urls.extend(books_urls)

        url = get_next_page_url(url, tree)
        if not url:
            break

    return urls


def get_all_book_urls_on_page( url , tree: HTMLParser) -> List[str]:
    """Récupère les URLs des livres sur une page spécifique."""
    try:
        books_links_node = tree.css("h3 > a")

        return [urljoin(url, link.attributes["href"])  for link in books_links_node if "href" in link.attributes]






    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des URLs des livres : {e}")
        return []

def get_next_page_url(url: str, tree: HTMLParser):
    """Récupère l'URL de la page suivante si elle existe."""
    next_page_node = tree.css_first("li.next > a")
    if next_page_node and "href" in next_page_node.attributes:
        return urljoin(url, next_page_node.attributes["href"])

    logger.info("Aucun bouton 'next' trouvé sur la page.")
    return None

# Fonction qui, à partir de l'URL d'un livre, va calculer son prix total (prix * stock disponible)
#     - Fonction pour récupérer le prix à partir du HTML
#     - Fonction pour récupérer la quantité disponible à partir du HTML

def get_books_price(url: str) -> float:
    """Calcule le prix total d'un livre en multipliant son prix unitaire par sa quantité en stock."""
    try:

        response = requests.get(url)
        response.raise_for_status()
        tree = HTMLParser(response.text)

        price = extract_price(tree)
        stock = extract_stock_quantity(tree)

        if price == 0 or stock == 0:
            logger.warning(f"Valeur suspecte pour {url} : prix={price}, stock={stock}")
            return 0.0

        price_stock = price * stock
        logger.info(f"Get book price at  {url} found {price_stock}")
        return price_stock

    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur get books price {url} : {e}")
        return 0.0

def extract_price(tree: HTMLParser) -> float:
    """Extrait le prix du livre depuis le HTML."""
    price_node = tree.css_first("p.price_color")
    if price_node:
        price_str = price_node.text()
    else:
        logger.error("Aucun élément contenant le prix n'a été trouvé.")
        return 0.0

    try:
        price = re.findall(r"[0-9.]+", price_str)[0]
    except (IndexError, ValueError) as e:
        logger.error(f"Erreur lors de l'extraction du prix : {e}")
        return 0.0

    return float(price)


def extract_stock_quantity(tree: HTMLParser) -> int:
    """Extrait la quantité en stock du livre depuis le HTML."""
    try:
        stock_node = tree.css_first("p.instock.availability")
        stock = int(re.findall(r"[0-9]+", stock_node.text())[0])

    except AttributeError as e:
        logger.error(f"Aucun élément 'p.instock.availability' trouvé sur la page : {e}")
        return 0

    except IndexError as e:
        logger.error(f"Erreur : aucun nombre trouvé dans l'élément stock : {e}")
        return 0

    except Exception as e:
        logger.error(f"Erreur inconnue lors de la récupération du stock : {e}")
        return 0

    return stock


def main() -> float:
    """Récupère toutes les URLs des livres et calcule le prix total de la bibliothèque."""
    all_books_url = get_all_books_url(BASE_URL)
    total_price = []

    for book_url in all_books_url:
        price = get_books_price(book_url)
        total_price.append(price)

    resutls =  sum(total_price)
    print(resutls)


if __name__ == '__main__':
    main()






