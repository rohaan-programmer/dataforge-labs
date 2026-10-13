import requests
from bs4 import BeautifulSoup

url = "https://scrapeme.live/shop/page/1/"
response = requests.get(url)
print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
products = soup.select("li.product")
print("Products on page:", len(products))

for p in products[:3]:
    name = p.select_one("h2.woocommerce-loop-product__title").text.strip()
    price = p.select_one(".price").text.strip()
    link = p.select_one("a.woocommerce-LoopProduct-link")["href"]
    print(name, "|", price, "|", link)

next_btn = soup.select_one("a.next")
print("Next page exists:", next_btn is not None)