from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.configurations.database import get_db
from src.services.sellers import SellerService
from src.services.auth import AuthService
from src.schemas.seller import Seller, SellerCreate, SellerUpdate, SellerWithBooks
from src.models.seller import Seller as SellerModel

router = APIRouter(prefix="/seller", tags=["sellers"])

@router.post("/", response_model=Seller, status_code=status.HTTP_201_CREATED)
def create_seller(seller: SellerCreate, db: Session = Depends(get_db)):
    existing_seller = SellerService.get_seller_by_email(db, seller.e_mail)
    if existing_seller:
        raise HTTPException(status_code=400, detail="Email already registered")
    return SellerService.create_seller(db, seller)

@router.get("/", response_model=List[Seller])
def get_sellers(db: Session = Depends(get_db)):
    return SellerService.get_sellers(db)

@router.get("/{seller_id}", response_model=SellerWithBooks)
def get_seller(seller_id: int, db: Session = Depends(get_db)):
    seller = SellerService.get_seller_with_books(db, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller

@router.put("/{seller_id}", response_model=Seller)
def update_seller(
    seller_id: int, 
    seller_update: SellerUpdate, 
    db: Session = Depends(get_db),
    current_user: SellerModel = Depends(AuthService.get_current_active_user)
):
    db_seller = SellerService.get_seller(db, seller_id)
    if not db_seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    if current_user.id != seller_id:
        raise HTTPException(status_code=403, detail="Can only update your own profile")
    
    if seller_update.e_mail and seller_update.e_mail != db_seller.e_mail:
        existing_seller = SellerService.get_seller_by_email(db, seller_update.e_mail)
        if existing_seller:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    return SellerService.update_seller(db, seller_id, seller_update)

@router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seller(
    seller_id: int, 
    db: Session = Depends(get_db),
    current_user: SellerModel = Depends(AuthService.get_current_active_user)
):
    db_seller = SellerService.get_seller(db, seller_id)
    if not db_seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    if current_user.id != seller_id:
        raise HTTPException(status_code=403, detail="Can only delete your own profile")
    
    SellerService.delete_seller(db, seller_id)
    return None