from flask import Flask, request

from diabetes_predictor import DiabetesPredictor

app = Flask(__name__)
app.config["DEBUG"] = True

model = None


@app.route('/diabetes_predictor', methods=['PUT'])
def refresh_model():
    return dp.update(request)


@app.route('/diabetes_predictor/file', methods=['GET'])
def predict():
    return dp.predict(request)


@app.route('/diabetes_predictor/str', methods=['POST', 'GET'])
def predict_str():
    return dp.predict_from_string(request.get_json()["input"])


@app.route('/diabetes_predictor/qstr', methods=['GET'])
def predict_strarg():
    return dp.predict_from_string(request.args.get("input"))


dp = DiabetesPredictor()
app.run(host='0.0.0.0', port=5000)
