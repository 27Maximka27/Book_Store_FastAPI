from sqlalchemy.orm import Session
from src.models.seller import Seller
from src.schemas.seller import SellerCreate, SellerUpdate
from src.services.auth import AuthService

class SellerService:
    @staticmethod
    def get_sellers(db: Session):
        return db.query(Seller).all()
    
    @staticmethod
    def get_seller(db: Session, seller_id: int):
        return db.query(Seller).filter(Seller.id == seller_id).first()
    
    @staticmethod
    def get_seller_by_email(db: Session, email: str):
        return db.query(Seller).filter(Seller.e_mail == email).first()
    
    @staticmethod
    def get_seller_with_books(db: Session, seller_id: int):
        # В SQLAlchemy книги загружаются автоматически благодаря relationship
        return db.query(Seller).filter(Seller.id == seller_id).first()
    
    @staticmethod
    def create_seller(db: Session, seller: SellerCreate):
        # Hash the password
        hashed_password = AuthService.get_password_hash(seller.password)
        
        # Create seller with hashed password
        seller_data = seller.model_dump()
        seller_data["password"] = hashed_password
        
        db_seller = Seller(**seller_data)
        db.add(db_seller)
        db.commit()
        db.refresh(db_seller)
        return db_seller
    
    @staticmethod
    def update_seller(db: Session, seller_id: int, seller_update: SellerUpdate):
        db_seller = db.query(Seller).filter(Seller.id == seller_id).first()
        if db_seller:
            update_data = seller_update.model_dump(exclude_unset=True)
            
            for key, value in update_data.items():
                setattr(db_seller, key, value)
            db.commit()
            db.refresh(db_seller)
        return db_seller
    
    @staticmethod
    def delete_seller(db: Session, seller_id: int):
        db_seller = db.query(Seller).filter(Seller.id == seller_id).first()
        if db_seller:
            db.delete(db_seller)
            db.commit()
        return db_seller