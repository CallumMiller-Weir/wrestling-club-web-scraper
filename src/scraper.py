import time
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def extract_contact_details(details):
    phone = None
    email = None
    address = None

    phone_regex = r"^\+?[\d\s\-]{7,15}$"
    email_regex = r"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"

    for detail in details:
        if re.match(phone_regex, detail):
            phone = detail
        elif re.match(email_regex, detail):
            email = detail
        else:
            address = detail

    return phone, email, address

def scrape(weblet_url, target_element, parent_container_div_class, club_name_div_class, details_div_class):
    weblet_url_len = len(weblet_url)
    print(f"Loading weblet {weblet_url}...")
    print("=" * weblet_url_len)

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(weblet_url)

    try:
        div_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, target_element))
        )
        print("Successfully located dynamic content.")
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        exit()

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    print("Parsing club details...")

    clubs = []
    club_elements = driver.find_elements(By.CSS_SELECTOR, parent_container_div_class)
    for club in club_elements:
        name = club.find_element(By.CSS_SELECTOR, club_name_div_class).text
        details = club.find_elements(By.CSS_SELECTOR, details_div_class)
        phone, email, address = extract_contact_details([detail.text for detail in details])

        result = {
            "name": name,
            "details": { k: v for k, v in { "phone": phone, "email": email, "address": address }.items() if v }
        }

        clubs.append(result);

    print(f"Found {len(clubs)} clubs in directory.")
    print("=" * weblet_url_len)

    driver.quit()

    return clubs