
import struct
import json
import base64

from client import ClientConnection

user_id = 143
username = ''
age = 0
gps = None

def decode_response(response):
    try:
        response = base64.b64decode(response)
    except:
        pass
    return response

with ClientConnection() as client:
    packFmt = '!HI'
    request = struct.pack(packFmt, 2, user_id)
    response = client.request(request)
    response = decode_response(response)
    d = json.loads(response)
    username = d['username']

with ClientConnection() as client:
    request = struct.pack('!HI', 3, user_id)
    response = client.request(request)
    response = decode_response(response)
    d = json.loads(response)
    age = d['age']

with ClientConnection() as client:
    request = struct.pack('!HI', 4, user_id)
    response = client.request(request)
    response = decode_response(response)
    d = json.loads(response)
    gps = d['last_gps_coords']

print 'username:', username
print 'user_id:', user_id
print 'age:', age
print 'gps:',gps