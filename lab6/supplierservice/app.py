from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/supplier1/orders/', methods=['POST', 'GET'])
def get_order():
    data = request.get_json(silent=True)
    return jsonify(data), 200


app.run(host='0.0.0.0', port=5000, debug=True)
