from numpy import integer
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean,Text,Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.main.models.db.base_class import Base

class Country(Base):
    __tablename__ = 'countries'

    uuid = Column(String, primary_key=True, index=True)
    name = Column(String,nullable=True,index=True)
    iso3 = Column(String,nullable=True,index=True)  # ISO 3166-1 alpha-3
    iso2 = Column(String,nullable=True,index=True)  # ISO 3166-1 alpha-2
    phonecode = Column(String,nullable=True,index=True)  # Code du pays (ex : +237)
    capital = Column(String,nullable=True,index=True)
    currency = Column(String,nullable=True,index=True)
    currency_symbol = Column(String,nullable=True,index=True)
    tld = Column(String,nullable=True,index=True)  # Domaine de niveau supérieur (ex: .cm)
    native = Column(String, nullable=True)
    region = Column(String,nullable=True,index=True)
    subregion = Column(String,nullable=True,index=True)
    timezones = Column(Text,nullable=True,index=True)
    translations = Column(Text, nullable=True)
    latitude = Column(Text,nullable=True,index=True)
    longitude = Column(Text,nullable=True,index=True)
    emoji = Column(Text,nullable=True,index=True)
    emojiU = Column(Text,nullable=True,index=True)
    flag = Column(Boolean, default=False)
    wikiDataId = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
