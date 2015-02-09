
import struct
import base64
import json
from pprint import pprint

from client import ClientConnection

valids = {}
for i in range(1000):
    with ClientConnection() as client:
        request = struct.pack('!H', i)
        response = client.request(request)
        if response != '' and response != 'error':
            valids[i] = response

for (k, v) in valids.items():
    print '%d:' % k,
    try:
        string = base64.b64decode(v)
        chunks = []
        for i in range(0, len(string), 40):
            chunks += [string[i:i+40]]
        for chunk in chunks:
            print chunk
    except:
        print v