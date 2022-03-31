import json
import os
from io import StringIO
from pathlib import Path

import numpy
import pandas
from flask import jsonify
from google.cloud import storage
from keras.models import load_model
from werkzeug.utils import secure_filename


class DiabetesPredictor:
    def __init__(self):
        self.model = None

    def update(self, body):
        req_data = body.get_json()
        client = storage.Client(project=req_data['project_id'])
        bucket = client.get_bucket(req_data['bucket_name'])
        blob = bucket.blob(req_data['model_file'])
        blob.download_to_filename('model.h5')
        self.model = load_model('model.h5')
        return jsonify({'message': "The diabetes predictor was updated"}), 200

    def predict(self, request):
        home = str(Path.home())
        soda_home = os.path.join(home, ".service_dir")
        if not os.path.exists(soda_home):
            os.makedirs(soda_home)

        if 'file' not in request.files:
            return jsonify({'message': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'message': 'No file selected for uploading'}), 400
        else:
            filename = secure_filename(file.filename)
            file_path = os.path.join(soda_home, filename)
            file.save(file_path)
            df = numpy.loadtxt(file_path, delimiter=",")
            df = df[:, 0:8]
            y_pred = self.model.predict(df)
            y_pred = (y_pred > 0.5)
            results = pandas.read_csv(file_path,
                                      names=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
                                             'BMI', 'DiabetesPedigreeFunction', 'Age'])
            results['Outcome'] = y_pred
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print("The file does not exist to be removed")

            parsed = json.loads(results.to_json(orient="records"))
            return jsonify(parsed), 200

    def predict_from_string(self, str):
        print(str)
        if self.model is None:
            self.model = load_model('model.h5')
        input2 = StringIO(str)
        df = numpy.fromstring(str, sep=",")
        df = numpy.reshape(df, (1, -1))
        df = df[:, 0:8]
        y_pred = self.model.predict(df)
        y_pred = (y_pred > 0.5)
        results = pandas.read_csv(input2,
                                  names=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
                                         'BMI', 'DiabetesPedigreeFunction', 'Age'])
        results['Outcome'] = y_pred
        parsed = json.loads(results.to_json(orient="records"))
        return jsonify(parsed), 200
