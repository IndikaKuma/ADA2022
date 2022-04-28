import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime

from db import Base


class UserDAO(Base):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = password
        self.registered_on = datetime.datetime.now()
        self.admin = admin
