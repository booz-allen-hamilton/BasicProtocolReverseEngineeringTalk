
import SocketServer
import json
import struct
import base64
from binascii import hexlify

ADDRESS = ('localhost', 43650)
DEFAULT_READ_SIZE = 256

commands = \
{
    2 : 'get_user_name',
    3 : 'get_user_age',
    4 : 'get_user_last_gps_coords',
    400 : 'dump_commands',
    401 : 'dump_encoding_type',
}

userDb = \
{
    'bob' : {
        'id' : 143,
        'age' : 24,
        'last_gps_coords': (14.2, 16.3),
    },
    'alice' : {
        'id' : 1223,
        'age' : 21,
        'last_gps_coords': (10.6, 22.0),
    },
    'carol' : {
        'id' : 845,
        'age' : 36,
        'last_gps_coords': (8.5, 3.1),
    },
}
    
class UserInfoRequestHandler(SocketServer.BaseRequestHandler):
    @staticmethod
    def _dict_to_json(d):
        return json.dumps(d)
    
    @staticmethod
    def _encode(string):
        return base64.b64encode(string)
    
    @staticmethod
    def _extract_user_id_from_request(request):
        packFmt = '<I'
        try:
            id, = struct.unpack_from(packFmt, request)
        except:
            id = -1
        return (id, request[struct.calcsize(packFmt):])
    
    @staticmethod
    def _get_username_from_id(id):
        username = None
        for (k,v) in userDb.items():
            if v['id'] == id:
                username = k
                break
        return username

    def handle(self):
        print '...Server received new connection from %s:%d' % self.client_address

        data = self.request.recv(DEFAULT_READ_SIZE)
        print 'request:', hexlify(data)
        
        commandPackFmt = '<H'
        command, = struct.unpack_from(commandPackFmt, data)
        
        if commands.has_key(command) is False:
            print 'command (%d) does not exist' % command
            self.request.send('error')
            return
        
        command_name = 'handle_%s' % commands[command]
        command_handler = getattr(self, command_name)
        response = command_handler(data[struct.calcsize(commandPackFmt):])
        print 'sending response:', str(response)
        self.request.send(response)
    
    def handle_get_user_name(self, request):
        response = 'error: id not found'
        (id, request) = self._extract_user_id_from_request(request)
        username = self._get_username_from_id(id)
        if username is not None:
            response = self._encode(self._dict_to_json({'username' : username}))
        return response
    
    def handle_get_user_age(self, request):
        response = 'error: id not found'
        (id, request) = self._extract_user_id_from_request(request)
        username = self._get_username_from_id(id)
        if username is not None:
            for (username, userdata) in userDb.items():
                if userdata['id'] == id:
                    response = self._encode(self._dict_to_json({'age' : userDb[username]['age']}))
                    break
        return response
    
    def handle_get_user_last_gps_coords(self, request):
        response = 'error: id not found'
        (id, request) = self._extract_user_id_from_request(request)
        username = self._get_username_from_id(id)
        if username is not None:
            for (username, userdata) in userDb.items():
                if userdata['id'] == id:
                    response = self._encode(self._dict_to_json({'last_gps_coords' : userDb[username]['last_gps_coords']}))
                    break
        return response
    
    def handle_dump_commands(self, request):
        return self._encode(self._dict_to_json(commands))
    
    def handle_dump_encoding_type(self, request):
        return 'base64'

class UserInfoServer(SocketServer.TCPServer):
    def __init__(self, server_address, handler_class=UserInfoRequestHandler):
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

server = None
try:
    print 'Starting server on port %d' % ADDRESS[1]
    server = UserInfoServer(ADDRESS)
    print 'Serving...'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Admin killed server'
except Exception as e:
    print 'Error:', repr(e)
finally:
    if server is not None:
        server.shutdown()