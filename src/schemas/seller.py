from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from src.schemas.books import Book

class SellerBase(BaseModel):
    first_name: str
    last_name: str
    e_mail: EmailStr

class SellerCreate(SellerBase):
    password: str

class SellerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    e_mail: Optional[EmailStr] = None

class Seller(SellerBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class SellerWithBooks(Seller):
    books: List[Book] = []