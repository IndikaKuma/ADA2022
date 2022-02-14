from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from daos.status_dao import StatusDAO
from db import Base


class DeliveryDAO(Base):
    __tablename__ = 'delivery'
    id = Column(Integer, primary_key=True)
    customer_id = Column(String)
    provider_id = Column(String)
    package_id = Column(String)
    order_time = Column(DateTime)
    delivery_time = Column(DateTime)
    status_id = Column(Integer, ForeignKey('status.id'))
    # https: // docs.sqlalchemy.org / en / 14 / orm / basic_relationships.html
    # https: // docs.sqlalchemy.org / en / 14 / orm / backref.html
    status = relationship(StatusDAO.__name__, backref=backref("delivery", uselist=False))

    def __init__(self, customer_id, provider_id, package_id, order_time, delivery_time, status):
        self.customer_id = customer_id
        self.provider_id = provider_id
        self.package_id = package_id
        self.order_time = order_time
        self.delivery_time = delivery_time
        self.status = status
