from flask import Flask
from flask_restx import Api, Resource, fields
from flask_cors import CORS

from models import BookDB
from database import get_db, init_db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(
    app,
    version='1.0',
    title='Library API',
    description='API для управления библиотекой',
    doc='/doc'  # Swagger UI будет доступен по /doc
)

# Модели для Swagger документации
book_model = api.model('Book', {
    'id': fields.Integer(required=True, description='ID книги'),
    'title': fields.String(required=True, description='Название книги'),
    'author': fields.String(required=True, description='Автор книги'),
    'description': fields.String(description='Описание книги')
})

book_create_model = api.model('BookCreate', {
    'title': fields.String(required=True, description='Название книги'),
    'author': fields.String(required=True, description='Автор книги'),
    'description': fields.String(description='Описание книги')
})

books_ns = api.namespace('books', description='Операции с книгами')

@books_ns.route('')
class BooksList(Resource):
    @books_ns.marshal_list_with(book_model)
    def get(self):
        """Получить список всех книг"""
        db = next(get_db())
        books = db.query(BookDB).order_by(BookDB.id).all()
        db.close()
        return books
    
    @books_ns.expect(book_create_model)
    @books_ns.marshal_with(book_model)
    def post(self):
        """Создать новую книгу"""
        db = next(get_db())
        data = api.payload
        new_book = BookDB(
            title=data['title'],
            author=data['author'],
            description=data.get('description')
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        db.close()
        return new_book

# Инициализация базы данных при запуске
def init_app():
    init_db()
    # Добавляем тестовые данные, если их еще нет
    db = next(get_db())
    if db.query(BookDB).count() == 0:
        test_book = BookDB(title='Война и мир', author='Лев Толстой', description='Эпический роман')
        db.add(test_book)
        db.commit()
        print("Добавлена тестовая книга: Война и мир")
    db.close()

if __name__ == "__main__":
    init_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
else:
    # Для запуска в Docker/gunicorn
    try:
        init_app()
    except Exception as e:
        print(f"Ошибка инициализации: {e}")
