import datetime
import os

import jwt

# get SECRET_KEY
if 'SECRET_KEY' in os.environ:
    key_file = os.environ['SECRET_KEY']
else:
    key_file = 'key.txt'
with open(key_file, 'r') as file:
    data = file.read().replace('\n', '')
SECRET_KEY_VALUE = data


# see https://realpython.com/token-based-authentication-with-flask/

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=600),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            SECRET_KEY_VALUE,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY_VALUE, algorithms=["HS256"])
        print(payload)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
