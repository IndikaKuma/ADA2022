from flask import jsonify

from daos.address_dao import AddressDAO
from daos.place_dao import PlaceDAO
from db import Session


# resource place record
class PlaceRecord:
    @staticmethod
    def get(name):
        session = Session()
        place = session.query(PlaceDAO).filter(PlaceDAO.name == name).first()
        if place:
            addresses_obj = place.addresses
            addresses = []
            for addr in addresses_obj:
                addresses.append(
                    {
                        "addr_id": addr.id
                    }
                )

            text_out = {
                "name:": place.name,
                "rating": place.rating,
                "addresses": addresses
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no place record with id {name}'}), 404

    @staticmethod
    def put(name, rating):
        session = Session()
        place = session.query(PlaceDAO).filter(PlaceDAO.name == name).first()

        if place:
            place.rating = rating
            session.commit()
            session.close()
            return jsonify({'message': 'The place record was updated'}), 200
        else:
            session.close()
            return jsonify({'message': f'There is no place record with id {name}'}), 404

    @staticmethod
    def delete(name):
        session = Session()
        effected_rows = session.query(PlaceDAO).filter(PlaceDAO.name == name).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no place record with id {name}'}), 404
        else:
            return jsonify({'message': 'The place record was removed'}), 200


class PlaceRecords:
    @staticmethod
    def post(body):
        name = body['name']
        session = Session()
        place = session.query(PlaceDAO).filter(PlaceDAO.name == name).first()
        if place:
            session.commit()
            session.close()
            return jsonify({'message': f'There exist a place record with id {name}'}), 404
        else:
            placedao = PlaceDAO()
            placedao.name = name
            placedao.rating = body['rating']

            for address in body['addresses']:
                addressdao = AddressDAO()
                addressdao.city = address['city']
                addressdao.postcode = address['postcode']
                addressdao.houseNo = address['houseNo']
                addressdao.street = address['street']
                placedao.addresses.append(addressdao)

            session.add(placedao)
            session.commit()
            session.refresh(placedao)
            session.close()
            return jsonify({'place_id': placedao.id}), 201
