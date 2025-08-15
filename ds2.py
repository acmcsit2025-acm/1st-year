import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome options (RUNNING WITH GUI)
chrome_options = Options()
# REMOVE headless mode to see the browser
# chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection

# Initialize WebDriver
print("Initializing WebDriver...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Torn City Wiki URL
PAGE_URL = "https://www.torn.com/wiki/"

try:
    print(f"Opening {PAGE_URL} in a real browser...")
    driver.get(PAGE_URL)
    
    # Wait longer for Cloudflare to verify (Increase if needed)
    time.sleep(20)

    # Check if the page loaded correctly
    if "Torn" in driver.title:
        print("✅ Page loaded successfully!")
    else:
        print("❌ Page did not load properly. Cloudflare may be blocking it.")

    # Find all Quick Links in the side panel
    print("Extracting Quick Links...")
    quick_links = driver.find_elements(By.CSS_SELECTOR, 'nav.flex-column a.nav-link')

    # Extract link names and URLs
    links = []
    for link in quick_links:
        href = link.get_attribute("href")
        text = link.text.strip()
        if href and text:
            links.append([text, href])

    # Save to CSV
    csv_filename = "torn_wiki_links.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Page Name", "URL"])  # Write header
        writer.writerows(links)

    print(f"\n✅ Links saved to {csv_filename}!")

except Exception as e:
    print(f"❌ An error occurred: {e}")

finally:
    # Close the browser
    print("Closing WebDriver...")
    driver.quit()
