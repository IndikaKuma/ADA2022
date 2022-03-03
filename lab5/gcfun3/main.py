import os

import numpy
from google.cloud import storage
from keras.models import load_model


def predict_diabetes(event, context):
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

    project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
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
    # fix random seed for reproducibility
    numpy.random.seed(7)
    # load pima indians dataset
    df = numpy.loadtxt(temp_filename, delimiter=",")
    df = df[:, 0:8]
    # Download model
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(model_bucket_name)
    blob = bucket.blob('model.h5')
    temp_model_filename = os.path.join('/tmp', 'model.h5')
    blob.download_to_filename(temp_model_filename)
    model = load_model(temp_model_filename)
    y_pred = model.predict(df)
    y_pred = (y_pred > 0.5)
    print(y_pred)
    # Do clean up
    os.remove(temp_filename)
    os.remove(temp_model_filename)
