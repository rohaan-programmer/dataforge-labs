import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

rows = []
seen_links = set()
page = 1

while page <= 100:
    url = f"https://scrapeme.live/shop/page/{page}/"
    response = requests.get(url)
    if response.status_code != 200:
        break
    soup = BeautifulSoup(response.text, "html.parser")

    new_count = 0
    for p in soup.select("li.product"):
        link = p.select_one("a.woocommerce-LoopProduct-link")["href"]
        if link in seen_links:
            continue
        seen_links.add(link)
        new_count += 1

        price_text = p.select_one(".price").text.strip()
        match = re.match(r"(\D*)([\d,\.]+)", price_text)
        currency = match.group(1).strip() if match else ""
        price = float(match.group(2).replace(",", "")) if match else None

        rows.append({
            "source": "scrapeme.live",
            "name": p.select_one("h2.woocommerce-loop-product__title").text.strip(),
            "price": price,
            "currency": currency,
            "image": p.select_one("img")["src"],
            "link": link,
        })

    print(f"page {page} | new: {new_count} | total: {len(rows)}")
    if new_count == 0 or soup.select_one("a.next") is None:
        break
    page += 1
    time.sleep(0.5)

df = pd.DataFrame(rows)
df.to_csv("scrapeme_products.csv", index=False, encoding="utf-8-sig")
print("Saved:", len(df), "rows")