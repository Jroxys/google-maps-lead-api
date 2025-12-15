from app.scraper import run_scraper

data = run_scraper("immigration consultant Berlin")

print("Toplam sonuç:", len(data))
print("İlk 2 kayıt:")
print(data[:2])
