from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base  # Изменено с BaseModel на Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    year = Column(Integer)
    price = Column(Float)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    
    # Relationship with seller
    seller = relationship("Seller", back_populates="books")