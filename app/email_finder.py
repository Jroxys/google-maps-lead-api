import requests
import re
from requests.exceptions import RequestException

EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

def extract_email_from_website(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            emails = re.findall(EMAIL_REGEX, r.text)
            return emails[0] if emails else None
    except RequestException:
        return None
    return None
