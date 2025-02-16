import requests 
from bs4 import BeautifulSoup
import pprint

url = "https://books.toscrape.com/"

response  = requests.get(url)

with open("index.html", "w") as f : 
    f.write(response.text)
soup = BeautifulSoup(response.text, 'html.parser')

aside = soup.find("div",class_= "side_categories") 
categories_div = aside.find("ul").find("li").find("ul")
# categories = [child.text.strip() for child in categories_div.children if child.name]

images = soup.find("section" ).find_all("img")
# article_div = soup.find("section" ).find_all("article").find_all("div")

product_prod = soup.find_all("article",class_= "product_pod")
i = 0 
titles  = []
for product in product_prod :
    title= product.find("h3").find("a")["title"]
    i += 1
    print(title)
    titles.append(title)
    # print(f" {i} -  {title}")
    


