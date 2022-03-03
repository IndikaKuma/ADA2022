from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from daos.address_dao import AddressDAO
from db import Base


class PlaceDAO(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rating = Column(Integer)
    addresses = relationship(AddressDAO.__name__)
