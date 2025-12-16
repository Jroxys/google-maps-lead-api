from app.scraper import run_scraper

if __name__ == "__main__":
    data = run_scraper("ayakkabıcı sivas", limit=10)
    print(f"Toplam lead: {len(data)}")
    for d in data:
        print(d)
