
import socket
import sys

ADDRESS = ('localhost', 43650)
DEFAULT_READ_SIZE = 256

print 'Client instance started.'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Client socket created.'

try:
    sock.connect(ADDRESS)
    print 'Client connected on local port %d.' % sock.getsockname()[1]
except Exception as e:
    print 'Connection failed. Error Code : ' + repr(e)
    sys.exit(1)
print 'Client connected to server.'

print 'Client sending request.'
sock.send('hello')

try:
    print 'Client awaiting response...'
    response = ''
    packet = None
    while packet != '':

        packet = sock.recv(DEFAULT_READ_SIZE)
        response += packet
    
    print 'Client got response:', response
except Exception as e:
    print 'err:', repr(e)
finally:
    sock.close()
    print 'Client socket closed.'
print 'Client stopped.'    