import os

import requests
from flask import Flask, request, make_response, jsonify

from db import Base, engine
from resources.delivery import Delivery
from resources.status import Status

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/deliveries', methods=['POST'])
def create_delivery():
    if check_if_authorize(request) == 200:
        req_data = request.get_json()
        return Delivery.create(req_data)
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 401


@app.route('/deliveries/<d_id>', methods=['GET'])
def get_delivery(d_id):
    if check_if_authorize(request) == 200:
        return Delivery.get(d_id)
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 401


@app.route('/deliveries/<d_id>/status', methods=['PUT'])
def update_delivery_status(d_id):
    if check_if_authorize(request) == 200:
        status = request.args.get('status')
        return Status.update(d_id, status)
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 401


@app.route('/deliveries/<d_id>', methods=['DELETE'])
def delete_delivery(d_id):
    if check_if_authorize(request) == 200:
        return Delivery.delete(d_id)
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 401


def check_if_authorize(req):
    auth_header = req.headers['Authorization']
    if 'AUTH_URL' in os.environ:
        auth_url = os.environ['AUTH_URL']
    else:
        auth_url = 'http://userservice_ct:5000/verify'
    result = requests.post(auth_url,
                           headers={'Content-Type': 'application/json',
                                    'Authorization': auth_header})
    app.logger.debug(result.status_code)
    app.logger.debug(result.json())
    return result.status_code


app.run(host='0.0.0.0', port=5000, debug=True)
