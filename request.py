"""
    6. Establecer conexión entre mensajero y receptor (¿sockets?)
    5. Generar bandeja para mensajes cifrados y otra para recibirlos

        0.1 Validar usuarios y emails
        0.2 Crear entorno visual (js, html, etc...) 
"""
import os
import json
import uuid
import requests
from flask_restful import Api, Resource, reqparse
from flask import Flask
from encryption import genKeys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

privateKey = Ed25519PrivateKey.generate()
publicKey = privateKey.public_key()
gen = genKeys(privateKey, publicKey)

login = str(input('loggin or sign in: '))
user = str(input('Nombre de usuario: '))
email = str(input('Email: '))
userId = uuid.uuid4().urn
userId = userId[9:]
api = f'http://localhost:3000/usuario?id={userId}'
def validateUser():
    
    with open('users.json') as file:
        data= json.load(file)
    
    if not user in data['users']:
        data['users'].update({user: {
            "nombre": user,
            "email": email,
            "api": api,
            "id": userId,
            "keys": {
                "private_key": gen.privateEnc(),
                "public_key": gen.publicEnc()
            },
            "loaded_keys": {
                "loaded_private_key": f"{gen.private_load_enc()}",
                "loaded_public_key": f"{gen.public_load_enc()}"
            },
            "certificates": f"{gen.certificates}"  
        }})
    with open('default.json') as file:
        defaults = json.load(file)
        
    if not user in defaults['users']:
        defaults['users'].update({user: {
            "inbound": [],
            "insent": []
        }})
    else:
        raise ValueError('user is already logged in ')

    with open('users.json', 'w') as file:
        json.dump(data, file, indent=3)
    with open('default.json', 'w') as file:
        json.dump(defaults, file, indent=3)

if login == '0':
    print('logged in')
else:
    validateUser()
    

while True:
    with open('default.json') as file:
        data = json.load(file)
    users = []
    for each in data['users']:
        users.append(each)
    for i in users:
        if len(data['users'][i]['insent']) != 0:
            os.system("python msgcrypt.py")

app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self, name):
        with open('users.json') as file:
            data = json.load(file)
        for user in data['users']:
            if (name == user):
                return data['users'][user] 
        return "Id not found", 400

api.add_resource(User, "/user/<name>")
app.run()



"""
b = Ed25519PrivateKey.from_private_bytes(data['usuario'][0]['mensajes']['keys']['private_key'].encode('latin-1'))
if str(b) != (data['usuario'][0]['mensajes']['loaded_keys']['loaded_private_key']):
    print("Hello")
"""

