import datetime
from flask import jsonify
from daos.delivery_dao import StatusDAO
from db import Session


class Status:
    @staticmethod
    def update(d_id, status_text):
        session = Session()
        statusobj = session.query(StatusDAO).filter(StatusDAO.id == int(d_id))[0]
        statusobj.status = status_text
        statusobj.last_update = datetime.datetime.now()
        session.commit()
        return jsonify({'message': 'The delivery status was updated'}), 200
