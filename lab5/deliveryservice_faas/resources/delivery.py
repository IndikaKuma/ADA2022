from datetime import datetime

from flask import jsonify

from constant import STATUS_CREATED
from daos.delivery_dao import DeliveryDAO
from daos.status_dao import StatusDAO
from db import Session


class Delivery:
    @staticmethod
    def create(body):
        session = Session()
        delivery = DeliveryDAO(body['id'], body['customer_id'], body['provider_id'], body['package_id'], datetime.now(),
                               datetime.strptime(body['delivery_time'], '%Y-%m-%d %H:%M:%S.%f'),
                               StatusDAO(body['id'], STATUS_CREATED, datetime.now()))
        session.add(delivery)
        session.commit()
        session.refresh(delivery)
        session.close()
        return jsonify({'delivery_id': delivery.id}), 200

    @staticmethod
    def get(d_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        delivery = session.query(DeliveryDAO).filter(DeliveryDAO.id == int(d_id)).first()

        if delivery:
            status_obj = delivery.status
            text_out = {
                "customer_id:": delivery.customer_id,
                "provider_id": delivery.provider_id,
                "package_id": delivery.package_id,
                "order_time": delivery.order_time.isoformat(),
                "delivery_time": delivery.delivery_time.isoformat(),
                "status": {
                    "status": status_obj.status,
                    "last_update": status_obj.last_update.isoformat(),
                }
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no delivery with id {d_id}'}), 404

    @staticmethod
    def delete(d_id):
        session = Session()
        effected_rows = session.query(DeliveryDAO).filter(DeliveryDAO.id == int(d_id)).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no delivery with id {d_id}'}), 404
        else:
            return jsonify({'message': 'The delivery was removed'}), 200
