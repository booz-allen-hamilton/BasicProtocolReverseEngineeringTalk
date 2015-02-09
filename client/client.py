
import socket
from binascii import hexlify

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
        except Exception as e:
            print 'err:', repr(e)
        finally:
            self.flush()
        return response