import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from app.email_finder import extract_email_from_website
from app.utils import get_random_proxy
import sys
sys.stdout.reconfigure(line_buffering=True)



def run_scraper(search_text: str, limit: int = 50):
    results = []
    proxy = None  # şimdilik kapalı

    print(f"[INFO] Using proxy: {proxy}")

    # ---------- CHROME OPTIONS ----------
    chromeOptions = Options()
    chromeOptions.add_argument("--headless=new")  # Docker için şart
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--disable-gpu")



    # Docker için (gerekirse açarız)
    # chrome_options.add_argument("--headless=new")

    if proxy:
        chromeOptions.add_argument(f"--proxy-server={proxy}")

    driver = webdriver.Chrome(
        options=chromeOptions
    )
    print("[INFO] Chrome WebDriver initialized.",flush=True)
    try:
        # ---------- GOOGLE MAPS ----------
        driver.get("https://www.google.com/maps?hl=tr")
        time.sleep(3)
        print("[INFO] Google Maps loaded.",flush=True)
        # ---------- COOKIE ACCEPT ----------
        try:
            accept_button = driver.find_element(
                By.XPATH,
                "//button//span[text()='Tümünü kabul et' or text()='Accept all']"
            )
            accept_button.click()
            time.sleep(2)
            print("[INFO] Cookies accepted.",flush=True)
        except:
            print("[INFO] No cookie accept button found.",flush=True)
            pass

        # ---------- SEARCH ----------
        wait = WebDriverWait(driver, 30)
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        print(f"[INFO] Searching for: {search_text}")
        driver.save_screenshot("/app/debug.png")
        search_box.send_keys(search_text)
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)


        # ---------- RESULTS LIST ----------
        try:
            results_list = driver.find_element(
                By.XPATH,
                f"//div[@aria-label='{search_text} için sonuçlar']"
            )
        except:
            driver.quit()
            return []

        # ---------- SCROLL ----------
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

        # ---------- PARSE HTML ----------
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

        # ---------- SCRAPE DATA ----------
        for container in data_containers[:limit]:
            try:
                name = container.find(
                    "div", class_="qBF1Pd fontHeadlineSmall"
                ).text
            except:
                name = "No name"

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
                phone = container.find(
                    "span", class_="UsdlK"
                ).text
            except:
                phone = "No phone number"

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
                "phone": phone,
                "emails": ", ".join(emails)
            })

    finally:
        driver.quit()

    return results
