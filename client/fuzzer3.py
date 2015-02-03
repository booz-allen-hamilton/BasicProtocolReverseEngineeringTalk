
import struct
import base64
from collections import OrderedDict
from pprint import pprint

from client import ClientConnection

def decode(string):
    return base64.b64decode(string)

users = {}
for i in range(1500):
    exists = False
    with ClientConnection() as client:
        request = struct.pack('<HI', 2, i)
        response = client.request(request)
        if response != 'error: id not found':
            exists = True
            username = decode(response)
    
    if exists is True:
        with ClientConnection() as client:
            request = struct.pack('<HI', 3, i)
            response = client.request(request)
            age = decode(response)
        
        with ClientConnection() as client:
            request = struct.pack('<HI', 4, i)
            response = client.request(request)
            gps = decode(response)
    
        users[username] = OrderedDict({'id': i, 'age' : age, 'gps' : gps})

pprint(users)