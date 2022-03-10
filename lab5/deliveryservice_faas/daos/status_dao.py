from sqlalchemy import Column, String, Integer, TIMESTAMP

from db import Base


class StatusDAO(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True) # Auto generated primary key
    status = Column(String)
    last_update = Column(TIMESTAMP(timezone=False))

    def __init__(self, id, status, last_update):
        self.id = id
        self.status = status
        self.last_update = last_update
