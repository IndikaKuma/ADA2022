import logging
import os

import numpy
from flask import jsonify
from google.cloud import storage
from keras.layers import Dense
from keras.models import Sequential


def train_diabetes_predictor(request):
    request_json = request.get_json(silent=True)
    project_id = request_json["project_id"]
    m_bucket = request_json["m_bucket"]
    bucket_name = request_json["f_bucket"]
    file_name = request_json["file_name"]

    # Open a channel to read the file from GCS
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    temp_filename = os.path.join('/tmp', file_name)
    blob.download_to_filename(temp_filename)
    # See https://machinelearningmastery.com/save-load-keras-deep-learning-models/ for ML model
    # fix random seed for reproducibility
    numpy.random.seed(7)
    # load pima indians dataset
    dataset = numpy.loadtxt(temp_filename, delimiter=",")
    # split into input (X) and output (Y) variables
    X = dataset[:, 0:8]
    Y = dataset[:, 8]
    # create model
    model = Sequential()
    model.add(Dense(12, input_dim=8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X, Y, epochs=150, batch_size=10, verbose=0)
    # evaluate the model
    scores = model.evaluate(X, Y, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    print(model.metrics_names)
    model_path = os.path.join('/tmp', "model.h5")
    model.save(model_path)
    # Save to GCS
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(m_bucket)
    blob = bucket.blob('model.h5')
    blob.upload_from_filename(model_path)
    # Do clean up
    os.remove(temp_filename)
    os.remove(model_path)
    logging.info("Saved the model to GCP bucket")
    return jsonify({"message": "Saved the model to GCP bucket"}), 200
