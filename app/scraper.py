import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from app.utils import get_random_proxy
from app.email_finder import extract_email_from_website


def run_scraper(search_text: str, limit: int = 50):
    results = []
    proxy = get_random_proxy()

    print(f"[INFO] Using proxy: {proxy}")

    with sync_playwright() as p:
        launch_args = {
            "headless": True,
            "args": ["--no-sandbox", "--disable-dev-shm-usage"]
        }

        if proxy:
            launch_args["proxy"] = {"server": proxy}

        browser = p.chromium.launch(**launch_args)
        context = browser.new_context()
        page = context.new_page()

        # -------- go_to_maps (AYNEN) --------
        page.goto("https://www.google.com/maps", timeout=60000)

        # Accept cookies if exists
        try:
            page.locator(
                "//button//span[text()='Tümünü kabul et' or text()='Accept all']"
            ).click(timeout=5000)
            time.sleep(2)
        except:
            pass

        page.wait_for_selector("#searchboxinput", timeout=20000)
        page.fill("#searchboxinput", search_text)
        page.keyboard.press("Enter")
        time.sleep(5)

        # -------- scroll_and_load (AYNEN MANTIK) --------
        try:
            results_list = page.locator(
                f"//div[@aria-label='{search_text} için sonuçlar']"
            )
            results_list.wait_for(timeout=20000)
        except:
            browser.close()
            return []

        last_height = page.evaluate(
            "(el) => el.scrollHeight",
            results_list
        )

        while True:
            page.evaluate(
                "(el) => el.scrollTo(0, el.scrollHeight)",
                results_list
            )
            time.sleep(2.5)

            new_height = page.evaluate(
                "(el) => el.scrollHeight",
                results_list
            )

            if new_height == last_height:
                break

            last_height = new_height

        page.evaluate(
            "(el) => el.scrollIntoView(true)",
            results_list
        )

        # -------- HTML PARSE (AYNEN) --------
        soup = BeautifulSoup(page.content(), "html.parser")

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
            browser.close()
            return []

        # -------- scrape_data (AYNEN) --------
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

        browser.close()
        return results
