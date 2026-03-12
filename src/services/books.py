from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.books import Book
from src.schemas.books import BookCreate, BookUpdate

class BookService:
    @staticmethod
    def get_books(db: Session):
        return db.query(Book).all()
    
    @staticmethod
    def get_book(db: Session, book_id: int):
        return db.query(Book).filter(Book.id == book_id).first()
    
    @staticmethod
    def create_book(db: Session, book: BookCreate):
        db_book = Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    
    @staticmethod
    def update_book(db: Session, book_id: int, book_update: BookUpdate):
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if db_book:
            update_data = book_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_book, key, value)
            db.commit()
            db.refresh(db_book)
        return db_book
    
    @staticmethod
    def delete_book(db: Session, book_id: int):
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if db_book:
            db.delete(db_book)
            db.commit()
        return db_book