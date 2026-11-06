import requests
from bs4 import BeautifulSoup
import csv
import os

print("===== AMAZON PRODUCT SCRAPER =====")

url = input("Paste Amazon product URL: ").strip()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-IN,en;q=0.9"
}

try:
    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    print("Status:", response.status_code)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.select_one("#productTitle")
    price = soup.select_one(".a-price .a-offscreen")

    product_name = (
        title.get_text(strip=True)
        if title else "Not found"
    )

    product_price = (
        price.get_text(strip=True)
        if price else "Not found"
    )

    print("Product:", product_name)
    print("Price:", product_price)

    filename = "amazon_products.csv"
    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Product", "Price", "URL"])

        writer.writerow([product_name, product_price, url])

    print("Saved to amazon_products.csv")

except requests.exceptions.RequestException as e:
    print("Request error:", e)