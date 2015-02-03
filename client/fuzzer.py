
import struct
import base64

from client import ClientConnection

valids = {}
for i in range(1000):
    with ClientConnection() as client:
        request = struct.pack('<H', i)
        response = client.request(request)
        if response != '' and response != 'error':
            valids[i] = response

for (k, v) in valids.items():
    print '%d:' % k,
    try:
        print base64.b64decode(v)
    except:
        print v