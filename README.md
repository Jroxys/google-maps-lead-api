# Google Maps Lead Generation API

A production-ready API that generates fresh business leads directly from Google Maps using keyword and location queries.

This API is designed for agencies, freelancers, and developers who need real-time B2B lead data without managing scrapers, proxies, or infrastructure.

---

## 🚀 Features

- Real-time Google Maps lead generation
- Keyword + location based search
- Email extraction when available
- JSON and CSV output
- Credit-based usage system
- Automatic refund if insufficient leads
- Usage logs & monitoring
- Rate limiting & proxy protection

---

## 📦 Data Included

Each lead may include:
- Business name
- Website
- Email (when available)
- Phone number
- Google rating
- Location

---

## 🔐 Authentication

All requests require an API key provided via request headers.

X-API-Key: YOUR_API_KEY

yaml


---

## 📡 API Endpoints

### Create Lead Job

POST /leads

css


**Request Body**
```json
{
  "keyword": "immigration consultant",
  "location": "Berlin",
  "limit": 10
}
Response

json

{
  "job_id": "abc123",
  "status": "processing"
}
Check Job Status
bash

GET /leads/status/{job_id}
Response

json

{
  "status": "completed"
}
Get Job Results
bash

GET /leads/result/{job_id}
Response

json

{
  "total": 3,
  "leads": [
    {
      "name": "Sunset Restaurant",
      "email": "info@sunset.com",
      "phone": "+90 212 555 1234",
      "website": "www.sunset.com",
      "rating": "4.5"
    }
  ]
}
Download CSV
bash
Kodu kopyala
GET /leads/csv/{job_id}
Returns a CSV file containing all generated leads.

Check Remaining Credits
bash
Kodu kopyala
GET /credits
Response

json
Kodu kopyala
{
  "remaining_credits": 47
}
Usage Logs
pgsql
Kodu kopyala
GET /usage
Returns recent API usage including keywords, locations, lead counts, and execution time.

💳 Credit System
Each successful lead generation job consumes 1 credit

If a job returns fewer than 3 leads, the credit is automatically refunded

Failed or empty jobs do not consume credits

This ensures fair and transparent billing.

🛠️ Tech Stack
FastAPI

PostgreSQL

Selenium

SQLAlchemy

BeautifulSoup

Proxy rotation

Rate limiting

⚠️ Disclaimer
This repository contains the core logic of the API.

Production infrastructure, proxy configuration, API keys, rate limits, and usage policies are managed server-side and are not included in this repository.

📬 Contact & Access
This API is currently in beta and onboarding a limited number of users.

For access, feedback, or collaboration:

Email: okilic1049@email.com

Discord: jroxy