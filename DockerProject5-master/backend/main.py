from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session

from models import BookDB
from schemas import Book, BookCreate
from database import get_db, init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    init_db()
    # Добавляем тестовые данные, если их еще нет
    db = next(get_db())
    if db.query(BookDB).count() == 0:
        test_book = BookDB(title='Война и мир', author='Лев Толстой', description='Эпический роман')
        db.add(test_book)
        db.commit()
        print("Добавлена тестовая книга: Война и мир")

@app.get("/books", response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
    return db.query(BookDB).order_by(BookDB.id).all()

@app.post("/books", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = BookDB(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
