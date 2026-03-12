from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base  # Изменено с BaseModel на Base

class Seller(Base):
    __tablename__ = "sellers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    e_mail = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    
    # Relationship with books
    books = relationship("Book", back_populates="seller", cascade="all, delete-orphan")