from sqlalchemy.orm import Session
from app.db_models import User


def consume_credit(db: Session, api_key: str) -> bool:
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        return False

    if user.credits <= 0:
        return False

    user.credits -= 1
    db.commit()
    return True


def get_credits(db: Session, api_key: str) -> int:
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        return 0
    return user.credits

def refund_credit(db: Session, api_key: str):
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        return
    user.credits += 1
    db.commit()
