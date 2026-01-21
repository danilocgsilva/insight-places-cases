from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Database connection string
DATABASE_URL = "mysql+pymysql://user:password@localhost/insight_places"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables (use this only for initial setup, prefer Alembic for migrations)
def init_db():
    Base.metadata.create_all(bind=engine)