# 📚 Web Scraping de Books to Scrape

Ce projet est un exercice de web scraping réalisé en Python à l'aide des bibliothèques `requests`, `BeautifulSoup`, `selectolax` et `loguru`. Il permet d'extraire des informations sur les livres disponibles sur le site [Books to Scrape](https://books.toscrape.com/).

## 📌 Objectifs du projet

1. **Scraper toutes les URLs des livres** de la bibliothèque.
2. **Extraire des informations clés** comme le titre, le prix et la quantité en stock.
3. **Analyser les catégories** pour trouver celle avec le moins de livres.
4. **Sauvegarder les résultats** dans un fichier JSON.

---

## 🛠️ Technologies utilisées

- **Python 3**
- `requests` → Pour les requêtes HTTP
- `BeautifulSoup` → Pour le parsing HTML
- `selectolax` → Pour un parsing HTML rapide
- `loguru` → Pour la gestion des logs
- `json` → Pour le stockage des données

---

## 📂 Structure des fichiers

- **`scrape_books.py`** → Script principal pour récupérer les URLs des livres et calculer le prix total.
- **`scrape_categories.py`** → Script permettant d'analyser les catégories et de déterminer celle contenant le moins de livres.
- **`response.json`** → Fichier généré contenant les données extraites.

---

## 🚀 Installation et exécution

###  Cloner le dépôt

```sh

git clone https://github.com/paulafredo/scarpping-books.toscrape



