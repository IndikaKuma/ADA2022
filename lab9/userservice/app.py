from flask import Flask, request

from db import Base, engine
from resources.loginapi import LoginAPI
from resources.user import User

app = Flask(__name__)
app.config["DEBUG"] = True

Base.metadata.create_all(engine)


@app.route('/register', methods=['POST'])
def register():
    req_data = request.get_json()
    return User.create(req_data)


@app.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    return LoginAPI.login(req_data)


@app.route('/verify', methods=['POST'])
def verify():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    return User.get(auth_header)


app.run(host='0.0.0.0', port=5000)
