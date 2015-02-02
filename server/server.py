
import SocketServer

ADDRESS = ('localhost', 43650)
DEFAULT_READ_SIZE = 256

class EchoRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print '...Server received new connection from %s:%d' % self.client_address

        data = self.request.recv(DEFAULT_READ_SIZE)
        print('recv()->"%s"' % data)
        self.request.send(data)
        return

class EchoServer(SocketServer.TCPServer):
    def __init__(self, server_address, handler_class=EchoRequestHandler):
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

try:
    print 'Starting server on port' % ADDRESS[1]
    server = EchoServer(ADDRESS)
    print 'Serving...'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Admin killed server'
except Exception as e:
    print 'Error:', repr(e)
finally:
    server.shutdown()