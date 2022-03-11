from db import Base, engine
from resources.delivery import Delivery
from resources.status import Status


def create_delivery(request):
    from flask import abort
    if request.method == 'POST':
        Base.metadata.create_all(engine)
        request_json = request.get_json(silent=True)
        return Delivery.create(request_json)
    else:
        return abort(405)


def get_delivery(request):
    print(request.path)
    from flask import abort
    if request.method == 'GET':
        Base.metadata.create_all(engine)
        request_args = request.args
        d_id = request_args['d_id']
        return Delivery.get(d_id)
    else:
        return abort(405)


def update_delivery_status(request):
    from flask import abort
    if request.method == 'PUT':
        Base.metadata.create_all(engine)
        request_args = request.args
        status = request_args['status']
        d_id = request_args['d_id']
        return Status.update(d_id, status)
    else:
        return abort(405)


def delete_delivery(request):
    from flask import abort
    if request.method == 'DELETE':
        Base.metadata.create_all(engine)
        request_args = request.args
        d_id = request_args['d_id']
        return Delivery.delete(d_id)
    else:
        return abort(405)
