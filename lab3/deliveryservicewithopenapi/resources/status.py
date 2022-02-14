import datetime
from flask import jsonify
from daos.delivery_dao import DeliveryDAO
from db import Session


class Status:
    @staticmethod
    def update(d_id, status):
        session = Session()
        delivery = session.query(DeliveryDAO).filter(DeliveryDAO.id == d_id)[0]
        delivery.status.status = status
        delivery.status.last_update = datetime.datetime.now()
        session.commit()
        return jsonify({'message': 'The delivery status was updated'}), 200
