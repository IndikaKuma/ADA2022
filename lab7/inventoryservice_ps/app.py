import logging
import os

from flask import Flask, request

from message_puller import MessagePuller
from pub_sub_util import create_subscription, create_topic
from resources.product import Product, Products

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
product = Product()
products = Products()
project_id = os.environ['project_id']
create_subscription(project=project_id, topic="order_req", subscription="order_req_sub")
create_topic(project=project_id, topic="inventory_status")
MessagePuller(project=project_id, subscription="order_req_sub", product=product)


@app.route('/products/', methods=['POST'])
def create_products():
    return products.post(request)


@app.route('/qproducts', methods=['POST'])
def create_products_from_query():
    return products.post_query(request)


@app.route('/products/<string:pname>', methods=['GET'])
def get_product_stock(pname):
    return product.get(pname)


@app.route('/products/<string:pname>/quantity', methods=['PUT'])
def update_product_stock(pname):
    return product.put(pname, int(request.args.get('value')))


app.run(host='0.0.0.0', port=5000, debug=True)
