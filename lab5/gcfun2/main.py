import logging
import os

import numpy
from google.cloud import storage
from keras.layers import Dense
from keras.models import Sequential


def build_diabetes_predictor(event, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        event (dict):  The dictionary with data specific to this type of event.
                       The `data` field contains a description of the event in
                       the Cloud Storage `object` format described here:
                       https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """

    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))
    print('Metageneration: {}'.format(event['metageneration']))
    print('Created: {}'.format(event['timeCreated']))
    print('Updated: {}'.format(event['updated']))

    project_id = os.environ.get('PROJET_ID', 'Specified environment variable is not set.')
    model_bucket_name = os.environ.get('MODEL_BUCKET', 'Specified environment variable is not set.')
    print('Project Id: {}'.format(project_id))

    bucket_name = event['bucket']
    file_name = event['name']

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
    bucket = client.get_bucket(model_bucket_name)
    blob = bucket.blob('model.h5')
    blob.upload_from_filename(model_path)
    # Do clean up
    os.remove(temp_filename)
    os.remove(model_path)
    logging.info("Saved the model to GCP bucket")
