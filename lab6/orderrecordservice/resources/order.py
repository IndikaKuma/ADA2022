import random

from flask import jsonify

orderRecords = [
    {
        "id": "id1",
        "product_type": "Laptop",
        "quantity": 4000,
        "unit_price": 444.50
    }
]


class Order:
    def get(self, id):
        for record in orderRecords:
            if id == record["id"]:
                return record, 200
        return jsonify({"message": "Order record not found"}), 404

    def put(self, id, rating):
        for record in orderRecords:
            if id == record["id"]:
                record["rating"] = rating
                return record, 200
        return jsonify({"message": "Order record not found"}), 404

    def delete(self, id):
        to_be_deleted = None
        for record in orderRecords:
            if id == record["id"]:
                to_be_deleted = record
                break
        if to_be_deleted:
            orderRecords.remove(to_be_deleted)
            return jsonify({"message": "{} is deleted.".format(id)}), 200
        return jsonify({"message": "Order record not found"}), 404


class Orders:
    def post(self, request):
        record_to_be_created = request.get_json(force=True)
        id1 = "id" + str(random.randint(1, 100001))
        record_to_be_created["id"] = id1
        for record in orderRecords:
            if id1 == record["id"]:
                return jsonify({"message": "Order with id {} already exists".format(id)}), 400
        orderRecords.append(record_to_be_created)
        return jsonify(record_to_be_created), 201

    def put(self, request):
        record_to_be_created = request.get_json(force=True)
        id = record_to_be_created['id']
        to_be_deleted = None
        for record in orderRecords:
            if id == record["id"]:
                to_be_deleted = record
                break
        if to_be_deleted:
            orderRecords.remove(to_be_deleted)
        orderRecords.append(record_to_be_created)
        return jsonify(record_to_be_created), 201

    def get(self):
        results = []
        for record in orderRecords:
            results.append(record["id"])
        return jsonify(results), 200
