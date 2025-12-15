import uuid
import random


PROXIES = [
    "http://spu8giugww:t=eH0cPZ7eEnr84pqc@gate.decodo.com:10001",
    "http://spu8giugww:t=eH0cPZ7eEnr84pqc@gate.decodo.com:10002",
    "http://spu8giugww:t=eH0cPZ7eEnr84pqc@gate.decodo.com:10003",
    "http://spu8giugww:t=eH0cPZ7eEnr84pqc@gate.decodo.com:10004",
    "http://spu8giugww:t=eH0cPZ7eEnr84pqc@gate.decodo.com:10005",
    "http://spu8giugww:t=eH0cPZ7eEnr84pqc@gate.decodo.com:10006",
    "http://spu8giugww:t=eH0cPZ7eEnr84pqc@gate.decodo.com:10007",
]

def get_random_proxy():
    if not PROXIES:
        return None
    return random.choice(PROXIES)


def generate_job_id():
    return str(uuid.uuid4())
