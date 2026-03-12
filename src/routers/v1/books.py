from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.configurations.database import get_db
from src.services.books import BookService
from src.services.sellers import SellerService
from src.services.auth import AuthService
from src.schemas.books import Book, BookCreate, BookUpdate
from src.models.seller import Seller

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
    """Get all books"""
    return BookService.get_books(db)

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    book = BookService.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate, 
    db: Session = Depends(get_db),
    current_user: Seller = Depends(AuthService.get_current_active_user)
):
    """Create a new book (requires authentication)"""
    seller = SellerService.get_seller(db, book.seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    if current_user.id != book.seller_id:
        raise HTTPException(status_code=403, detail="Can only create books for yourself")
    
    return BookService.create_book(db, book)

@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int, 
    book_update: BookUpdate, 
    db: Session = Depends(get_db),
    current_user: Seller = Depends(AuthService.get_current_active_user)
):
    db_book = BookService.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if db_book.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only update your own books")
    
    return BookService.update_book(db, book_id, book_update)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int, 
    db: Session = Depends(get_db),
    current_user: Seller = Depends(AuthService.get_current_active_user)
):
    db_book = BookService.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if db_book.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only delete your own books")
    
    BookService.delete_book(db, book_id)
    return None