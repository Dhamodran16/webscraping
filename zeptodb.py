import os
import time
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def connect_mongodb():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")  
        db = client["ZeptoDB"]  
        return db
    except Exception as e:
        print("❌ MongoDB Connection Error:", e)
        return None

def scrape_zepto(urls):
    driver = setup_driver()
    db = connect_mongodb()

    if db is None:
        print("❌ Exiting due to MongoDB connection failure.")
        return

    collection = db["ZeptoProducts"]

    for url in urls:
        print(f"🔍 Scraping: {url}")
        driver.get(url)
        time.sleep(5) 

        data = []
        products = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='product-card']")

        for product in products:
            try:
                name = product.find_element(By.CSS_SELECTOR, "h5[data-testid='product-card-name']").text
                quantity = product.find_element(By.CSS_SELECTOR, "span[data-testid='product-card-quantity'] h4").text
                price = product.find_element(By.CSS_SELECTOR, "h4[data-testid='product-card-price']").text

                try:
                    discount_price = product.find_element(By.CSS_SELECTOR, "p.line-through").text
                except:
                    discount_price = "N/A"

                record = {
                    "Name": name,
                    "Quantity": quantity,
                    "Price": price,
                    "Discount": discount_price,
                    "URL": url
                }
                data.append(record)
            except Exception as e:
                print(f"⚠️ Error extracting product details from {url}: {e}")
                continue

        if data:
            collection.insert_many(data)
            print(f"✅ Inserted {len(data)} products from {url} into MongoDB.")

    driver.quit()
    print("🎉 Scraping completed.")


def read_urls_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found!")
        return []

    with open(file_path, "r") as file:
        urls = [line.strip() for line in file.readlines()]
    return urls


if __name__ == "__main__":
    url_file = r"C:\Users\dhanashri laptop\Downloads\httpswww.zepto.comcnfruits-vegetabl.txt"
    urls = read_urls_from_file(url_file)

    if urls:
        scrape_zepto(urls)
    else:
        print("⚠️ No URLs found. Exiting.")