import requests
from bs4 import BeautifulSoup

base_url = "https://books.toscrape.com/"

# Effectuer une requête pour obtenir la page principale
response = requests.get(base_url)
page_soup = BeautifulSoup(response.text, 'html.parser')

# Trouver la section des catégories
categories_section = page_soup.find("div", class_="side_categories")
categories_list = categories_section.find("ul").find("li").find("ul")

# Extraire les noms des catégories et leurs liens
category_links = categories_list.find_all("a")
category_names = [category.text.strip() for category in category_links]
category_urls = [base_url + link["href"] for link in category_links]

index = 0
min_books_count = float('inf')  # Initialisation avec un nombre très grand pour trouver le minimum

# Boucle pour trouver la catégorie avec le moins de livres
for i in range(len(category_names)):
    try:
        response = requests.get(category_urls[i])
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find("form")
        
        # Vérifier si le formulaire et le nombre de livres sont présents
        if form:
            nb_livre = form.find("strong")
            if nb_livre:
                nb_livre = int(nb_livre.text.strip())
                if nb_livre < min_books_count:
                    min_books_count = nb_livre
                    index = i
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête pour la catégorie {category_names[i]} : {e}")
    except Exception as e:
        print(f"Erreur lors du traitement de la catégorie {category_names[i]} : {e}")

# Afficher le résultat
if min_books_count != float('inf'):
    print(f"La catégorie avec le moins de livres est '{category_names[index]}' avec {min_books_count} livres.")
else:
    print("Aucune catégorie n'a pu être traitée correctement.")


   

titles = [a ["title"] for a in soup.find_all('a',title = True ) ]
# pprint(titles)


