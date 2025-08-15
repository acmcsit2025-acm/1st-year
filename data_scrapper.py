import csv
import time
import json
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the saved links from CSV
csv_filename = "torn_wiki_links.csv"

with open(csv_filename, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    links = [(row[0], row[1]) for row in reader]  # (Page Name, URL)

# Setup undetected Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-popup-blocking")

# Use a real Chrome profile (change path accordingly)
chrome_options.add_argument(r"user-data-dir=C:\Users\USER\AppData\Local\Google\Chrome\User Data")

# Start undetected Chrome
print("Starting undetected Chrome...")
driver = uc.Chrome(options=chrome_options, headless=False)

scraped_data = []  # Store extracted data

# Random User Agents List
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
]

# Function to scrape a single page
def scrape_page(name, url):
    try:
        print(f"Scraping: {name} - {url}")
        driver.get(url)
        
        # Wait for page to load completely (increase time if needed)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        time.sleep(random.randint(5, 10))  # Random delay to prevent detection

        # Extract Title
        title = driver.find_element(By.TAG_NAME, "h1").text.strip() if driver.find_elements(By.TAG_NAME, "h1") else "No Title Found"

        # Extract Main Content
        main_content = driver.find_element(By.CSS_SELECTOR, "div#mw-content-text").text.strip() if driver.find_elements(By.CSS_SELECTOR, "div#mw-content-text") else "No Content Found"

        print(f"✅ Successfully Scraped: {title}")

        return {"title": title, "url": url, "content": main_content}

    except Exception as e:
        print(f"❌ Failed to scrape {name}: {e}")
        return None

# Scrape all pages (with retries for failed pages)
failed_links = []
for name, url in links:
    data = scrape_page(name, url)
    if data:
        scraped_data.append(data)
    else:
        failed_links.append((name, url))

# Retry failed pages
if failed_links:
    print("\n🔄 Retrying failed links...")
    time.sleep(10)  # Wait before retrying

    for name, url in failed_links:
        data = scrape_page(name, url)
        if data:
            scraped_data.append(data)

# Close browser
print("Closing browser...")
driver.quit()

# Save Data as JSON
json_filename = "torn_wiki_data.json"
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)

print(f"\n✅ Data saved to {json_filename}!")
