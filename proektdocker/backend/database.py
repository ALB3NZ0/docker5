import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql://postgres:1@db:5432/library_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.close()
            break
        except psycopg2.OperationalError:
            print("Ожидаем запуск базы данных...")
            time.sleep(2)

def init_db():
    wait_for_db()
    try:
        Base.metadata.create_all(bind=engine)
        print("База данных инициализирована")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        print("Проверьте, что PostgreSQL запущен и доступен по адресу localhost:5432")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
