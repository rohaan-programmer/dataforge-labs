import requests
from bs4 import BeautifulSoup

url = "https://www.scrapingcourse.com/ecommerce/"
response = requests.get(url)
print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
products = soup.select("li.product")
print("Products on page:", len(products))

for p in products[:3]:
    name = p.select_one("h2").text.strip()
    price = p.select_one(".price").text.strip()
    link = p.select_one("a")["href"]
    print(name, "|", price, "|", link)

next_btn = soup.select_one("a.next")
print("Next page exists:", next_btn is not None)
if next_btn:
    print("Next link:", next_btn["href"])