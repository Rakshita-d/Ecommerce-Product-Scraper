import requests
from bs4 import BeautifulSoup
import csv

print("===== PRACTICE WEBSITE SCRAPER =====")

all_products = []

for page in range(1, 3):

    url = (
        "https://webscraper.io/test-sites/"
        f"e-commerce/static/computers/laptops?page={page}"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        products = soup.find_all(
            "div",
            class_="thumbnail"
        )

        print(f"Page {page}: Found {len(products)} products")

        for product in products:

            name_tag = product.find("a", class_="title")
            price_tag = product.find("h4", class_="price")

            name = (
                name_tag.get_text(strip=True)
                if name_tag else "Not found"
            )

            price = (
                price_tag.get_text(strip=True)
                if price_tag else "Not found"
            )

            all_products.append([name, price])

    except requests.exceptions.RequestException as e:
        print("Error:", e)

with open(
    "practice_products.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price"])
    writer.writerows(all_products)

print("\nTotal products scraped:", len(all_products))
print("Saved to practice_products.csv")