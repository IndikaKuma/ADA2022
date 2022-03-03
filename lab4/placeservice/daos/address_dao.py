from sqlalchemy import Column, String, Integer, ForeignKey

from db import Base


class AddressDAO(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    postcode = Column(String)
    street = Column(String)
    houseNo = Column(Integer)
    city = Column(String)
    place_id = Column(Integer, ForeignKey('place.id'))