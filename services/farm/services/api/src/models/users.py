






import enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship

from src.core.database import Base

class UserRole(str, enum.Enum):
    CONSUMER = "consumer"
    CHEF = "chef"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String(1024))
    full_name = Column(String(256))
    role = Column(SQLEnum(UserRole), default=UserRole.CONSUMER)
    identity_verification = Column(JSONB(nullable=True))  # KYC data
    rating = Column(Float, nullable=True)  # Average rating from consumers
    location = Column(String(1024), nullable=True)  # GeoJSON or address

    orders = relationship("Order", back_populates="consumer")
    chef_profile = relationship("Chef", uselist=False, back_populates="user")





