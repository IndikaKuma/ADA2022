import os

import requests
from flask import Flask, request

from db import Base, engine
from resources.delivery import Delivery
from resources.status import Status

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/deliveries', methods=['POST'])
def create_delivery():
    check_if_authorize(request)
    req_data = request.get_json()
    return Delivery.create(req_data)


@app.route('/deliveries/<d_id>', methods=['GET'])
def get_delivery(d_id):
    check_if_authorize(request)
    return Delivery.get(d_id)


@app.route('/deliveries/<d_id>/status', methods=['PUT'])
def update_delivery_status(d_id):
    check_if_authorize(request)
    status = request.args.get('status')
    return Status.update(d_id, status)


@app.route('/deliveries/<d_id>', methods=['DELETE'])
def delete_delivery(d_id):
    check_if_authorize(request)
    return Delivery.delete(d_id)


def check_if_authorize(req):
    auth_header = req.headers['Authorization']
    if 'AUTH_URL' in os.environ:
        auth_url = os.environ['AUTH_URL']
    else:
        auth_url = 'http://userservice_ct:5000/verify'
    result = requests.post(auth_url,
                           headers={'Content-Type': 'application/json',
                                    'Authorization': auth_header})
    print(result.status_code)
    print(result.json())


app.run(host='0.0.0.0', port=5000)
