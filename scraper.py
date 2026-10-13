import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE = "https://webscraper.io"
CATEGORIES = [
    "computers/laptops",
    "computers/tablets",
    "phones/touch",
]

rows = []
seen_links = set()

for category in CATEGORIES:
    page = 1
    while page <= 50:
        url = f"{BASE}/test-sites/e-commerce/allinone/{category}?page={page}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        new_count = 0
        for p in soup.select(".thumbnail"):
            link_tag = p.select_one("a.title")
            link = BASE + link_tag["href"]
            if link in seen_links:
                continue
            seen_links.add(link)
            new_count += 1
            rows.append({
                "source": "webscraper.io",
                "category": category.split("/")[-1],
                "name": link_tag["title"],
                "price": p.select_one(".price").text.strip(),
                "rating": p.select_one("[data-rating]")["data-rating"],
                "reviews": p.select_one(".review-count").text.strip(),
                "description": p.select_one(".description").text.strip(),
                "link": link,
            })

        print(f"{category} | page {page} | new: {new_count} | total: {len(rows)}")
        if new_count == 0:
            break
        page += 1
        time.sleep(0.5)

df = pd.DataFrame(rows)
df.to_csv("webscraper_products.csv", index=False, encoding="utf-8-sig")
print("Saved:", len(df), "rows")