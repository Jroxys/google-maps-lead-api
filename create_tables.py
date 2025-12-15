from app.database import engine
from app.db_models import Base

def create_tables():
    print("📦 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully")

if __name__ == "__main__":
    create_tables()
