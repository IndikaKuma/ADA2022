from flask import jsonify

inventories = [
    {
        "name": "Laptop",
        "quantity": 1000
    },
    {
        "name": "Phone",
        "quantity": 5000
    }
]


class Product:
    def get(self, pname):
        for record in inventories:
            if pname == record["name"]:
                return jsonify(record), 200
        return jsonify({"message": "No product for " + pname}), 404

    def put(self, pname, value):
        for record in inventories:
            if pname == record["name"]:
                record["quantity"] = record["quantity"] - value
                return jsonify(record), 200
        return jsonify({"message": "No product for " + pname}), 404


class Products:
    def post(self, request):
        record_to_be_created = request.get_json(force=True)
        pname = record_to_be_created["name"]
        for record in inventories:
            if pname == record["name"]:
                return jsonify({"message": "There is a product with the name " + pname}), 400
        inventories.append(record_to_be_created)
        return jsonify(record_to_be_created), 201

    def post_query(self, request):
        pname = request.args.get('name')
        quantity = request.args.get('quantity')
        for record in inventories:
            if pname == record["name"]:
                return jsonify({"message": "There is a product with the name " + pname}), 400
        record_to_be_created = {"name": pname, "quantity": quantity}
        inventories.append(record_to_be_created)
        return jsonify(record_to_be_created), 201
