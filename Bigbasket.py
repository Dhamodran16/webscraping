import os
import time
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def connect_mongodb():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["BigBasketDB"]
        return db
    except Exception as e:
        print("\u274c MongoDB Connection Error:", e)
        return None

def scrape_bigbasket(urls):
    driver = setup_driver()
    db = connect_mongodb()

    if db is None:
        print("\u274c Exiting due to MongoDB connection failure.")
        return

    collection = db["BigBasketProducts"]

    for index, url in enumerate(urls):
        print(f"\U0001F50D Scraping: {url}")

        # Restart WebDriver every 5 URLs to prevent session crashes
        if index % 5 == 0 and index != 0:
            print("🔄 Restarting WebDriver to avoid session crashes...")
            driver.quit()
            driver = setup_driver()

        driver.get(url)
        time.sleep(5)  

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "SKUDeck___StyledDiv-sc-1e5d9gk-0"))
            )
        except:
            print(f"⚠️ No products found on {url}")
            continue

        data = []
        products = driver.find_elements(By.CLASS_NAME, "SKUDeck___StyledDiv-sc-1e5d9gk-0")
        print(f"🛒 Found {len(products)} products on {url}")

        for product in products:
            try:
                # ✅ Corrected Product Name Selector
                name_element = product.find_elements(By.XPATH, ".//h3[contains(@class, 'block m-0 line-clamp-2 font-regular text-base leading-sm text-darkOnyx-800')]")
                name = name_element[0].text if name_element else "N/A"

                price_element = product.find_elements(By.CSS_SELECTOR, "span.Pricing___StyledLabel-sc-pldi2d-1")
                price = price_element[0].text if price_element else "N/A"

                discount_element = product.find_elements(By.XPATH, ".//span[contains(@class, 'font-semibold')]")
                discount = discount_element[0].text if discount_element else "No Discount"

                quantity_element = product.find_elements(By.CSS_SELECTOR, "button.PackChanger___StyledButton-sc-newjpv-0 span")
                quantity = quantity_element[0].text.strip() if quantity_element else "N/A"

                record = {
                    "Name": name,
                    "Quantity": quantity,
                    "Price": price,
                    "Discount": discount,
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
        print(f"\u274c Error: File '{file_path}' not found!")
        return []

    with open(file_path, "r") as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

if __name__ == "__main__":
    url_file = r"C:\Users\dhanashri laptop\Downloads\bigbasketlinks-copy.txt"
    urls = read_urls_from_file(url_file)

    if urls:
        scrape_bigbasket(urls)
    else:
        print("⚠️ No URLs found. Exiting.")