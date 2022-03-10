from flask import Flask, request

from db import Base, engine
from resources.delivery import Delivery
from resources.status import Status

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/deliveries', methods=['POST'])
def create_delivery():
    req_data = request.get_json()
    return Delivery.create(req_data)


@app.route('/deliveries/<d_id>', methods=['GET'])
def get_delivery(d_id):
    return Delivery.get(d_id)


@app.route('/deliveries/<d_id>/status', methods=['PUT'])
def update_delivery_status(d_id):
    status = request.args.get('status')
    return Status.update(d_id, status)


@app.route('/deliveries/<d_id>', methods=['DELETE'])
def delete_delivery(d_id):
    return Delivery.delete(d_id)


app.run(host='0.0.0.0', port=5000)
