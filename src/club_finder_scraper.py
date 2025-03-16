import os
import platform
import subprocess
import time
import json
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
            "details": {
                "phone": phone,
                "email": email,
                "address": address
            }
        }

        clubs.append(result);

    print(f"Found {len(clubs)} clubs in directory.")
    print("=" * weblet_url_len)

    driver.quit()

    return clubs

def dumpJsonToFile(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Data saved to '{file_name}'")

def openFile(file_name):
    current_os = platform.system()
    if current_os == "Windows":
        subprocess.run(["start", file_name], shell=True)
    elif current_os == "Linux":
        subprocess.run(["xdg-open", file_name])
    else:
        print(f"Unsupported OS: {current_os}")

WEBLET_URL = "https://britishwrestling.justgo.com/weblets/CoachAndClubFinder/74728f3b-1e94-44fc-8217-e70f15953222/"
TARGET_ELEMENT = "webletsCoachAndClubFinder74728f3b-1e94-44fc-8217-e70f15953222"
PARENT_CONTAINER_DIV_CLASS = ".flex.flex-col.md\\:flex-row.relative.space-y-4.md\\:space-y-0.md\\:space-x-4"
CLUB_NAME_DIV_CLASS = ".text-globalTextSizeLg.font-medium.text-jg-metal-900"
DETAILS_DIV_CLASS = ".text-jg-metal-800.text-globalTextSizeSm"

clubs = scrape(WEBLET_URL, TARGET_ELEMENT, PARENT_CONTAINER_DIV_CLASS, CLUB_NAME_DIV_CLASS, DETAILS_DIV_CLASS);

file_name = input("Enter a file name (default=\"clubs.json\"): ") or "clubs.json"
dumpJsonToFile(file_name, clubs)
openFile(file_name)