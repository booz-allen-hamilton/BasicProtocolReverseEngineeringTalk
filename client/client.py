
import socket
import struct
from binascii import hexlify
import json
import base64

ADDRESS = ('localhost', 43650)
DEFAULT_READ_SIZE = 256

class ClientConnection(object):
    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print 'Socket failed. Error Code : ' + repr(e)
        print 'Client socket created.'
        
        try:
            self.socket.connect(ADDRESS)
            print 'Client connected on local port %d.' % self.socket.getsockname()[1]
        except Exception as e:
            print 'Connection failed. Error Code : ' + repr(e)
        print 'Client connected to server.'
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        if self.socket is not None:
            self.flush()
            self.socket.close()
        self.socket = None
    
    @staticmethod
    def _decode_response(response):
        return base64.b64decode(response)
    
    def flush(self):
        while self.socket.recv(DEFAULT_READ_SIZE) != '':
            continue
    
    def request(self, req):
        print 'Sending request:', hexlify(req)
        self.socket.send(req)
        
        try:
            print 'Awaiting response...'
            response = ''
            packet = None
            while packet != '':
                packet = self.socket.recv(DEFAULT_READ_SIZE)
                response += packet
            
            print 'Got response:', repr(response)
            try:
                response = self._decode_response(response)
            except:
                pass
        except Exception as e:
            print 'err:', repr(e)
        finally:
            self.flush()
        return response

username = 'bob'
user_id = 0
age = 0
gps = None
with ClientConnection() as client:
    packFmt = '<H%ds' % len(username)
    request = struct.pack(packFmt, 2, username)
    response = client.request(request)
    d = json.loads(response)
    user_id = d['id']

if user_id > 0:
    with ClientConnection() as client:
        request = struct.pack('<HI', 3, user_id)
        response = client.request(request)
        d = json.loads(response)
        age = d['age']
        
    with ClientConnection() as client:
        request = struct.pack('<HI', 4, user_id)
        response = client.request(request)
        d = json.loads(response)
        gps = d['last_gps_coords']
print 'username:', username
print 'user_id:', user_id
print 'age:', age
print 'gps:',gps