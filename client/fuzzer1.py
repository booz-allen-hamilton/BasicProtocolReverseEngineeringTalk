
import struct
from pprint import pprint

from client import ClientConnection

valids = {}
for i in range(1000):
    with ClientConnection() as client:
        request = struct.pack('<H', i)
        response = client.request(request)
        if response != '' and response != 'error':
            valids[i] = response

pprint(valids)