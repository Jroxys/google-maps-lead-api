from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from app.utils import get_random_proxy

from app.email_finder import extract_email_from_website


def run_scraper(search_text: str, limit: int = 50):
    proxy = get_random_proxy()
    results = []

    # -------- CHROME OPTIONS (HEADLESS YOK) --------
    chromeOptions = Options()
    chromeOptions.add_argument("--start-maximized")
    if proxy:
        chromeOptions.add_argument(f"--proxy-server={proxy}")
        print(f"[INFO] Using proxy: {proxy}")
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--log-level=3")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chromeOptions
    )

    # -------- go_to_maps (AYNEN) --------
    driver.get("https://www.google.com/maps")
    accept_cookies_button = driver.find_element(
        By.XPATH,
        "//button//span[text()='Tümünü kabul et' or text()='Accept all']"

    )
    accept_cookies_button.click()
    time.sleep(2)
    searchBox = driver.find_element(By.ID, "searchboxinput")
    searchBox.send_keys(search_text)
    searchBox.send_keys(Keys.ENTER)
    time.sleep(5)

    # -------- scroll_and_load (AYNEN) --------
    results_list = driver.find_element(
        By.XPATH,
        f"//div[@aria-label='{search_text} için sonuçlar']"
    )

    last_height = driver.execute_script(
        "return arguments[0].scrollHeight",
        results_list
    )

    while True:
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight",
            results_list
        )
        time.sleep(2.5)
        new_height = driver.execute_script(
            "return arguments[0].scrollHeight",
            results_list
        )
        if new_height == last_height:
            break
        last_height = new_height

    driver.execute_script(
        "arguments[0].scrollIntoView(true);",
        results_list
    )

    # -------- HTML PARSE --------
    soup = BeautifulSoup(driver.page_source, "html.parser")

    possible_classes = [
        "Nv2PK tH5CWc THOPZb",
        "Nv2PK THOPZb CpccDe",
        "Nv2PK Q2HXcd THOPZb"
    ]

    data_containers = None
    for class_name in possible_classes:
        data_containers = soup.find_all("div", class_=class_name)
        if data_containers:
            break

    if not data_containers:
        driver.quit()
        return []

    # -------- scrape_data (AYNEN) --------
    for container in data_containers[:limit]:
        name = container.find(
            "div", class_="qBF1Pd fontHeadlineSmall"
        ).text

        try:
            ratings = container.find("span", class_="MW4etd").text
        except:
            ratings = "Has No rating"

        try:
            comments = container.find("span", class_="UY7F9").text
        except:
            comments = "Has No comments."

        try:
            website = container.find(
                "a", {"class": "lcr4fd S9kvJb"}
            ).get("href")
        except:
            website = "No Website"

        try:
            phoneNumber = container.find(
                "span", class_="UsdlK"
            ).text
        except:
            phoneNumber = "No phone number"

        if website != "No Website":
            emails = extract_email_from_website(website)
        else:
            emails = ["No website to extract email"]
        if isinstance(emails, str):
            emails = [emails]
        elif emails is None:
            emails = ["No email found"]

        results.append({
            "name": name,
            "ratings": ratings,
            "comments": comments,
            "website": website,
            "phone": phoneNumber,
            "emails": ", ".join(emails)
        })

    driver.quit()
    return results
