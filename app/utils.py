import uuid
import random


PROXIES = []
def get_random_proxy():
    if not PROXIES:
        return None
    return random.choice(PROXIES)


def generate_job_id():
    return str(uuid.uuid4())
