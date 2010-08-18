import simplejson as json
from ncore.rest import request
import httplib
import urllib
import sys

def main():
    if sys.argv[1] == 'create':
        config = {
            'mac': '02:52:0a:00:00:01',
            'nic': 'e1000',
        }
        req = urllib.urlopen('http://10.2.129.232:3000/api/1/t0001',
            urllib.urlencode({'json': json.dumps(config)}))
        print req.read()
        return

    if sys.argv[1] == 'update':
        config = {
            'nic': 'e1000',
            'boot': 'cn',
        }
        conn = httplib.HTTPConnection('10.2.129.232', 3000)
        conn.request('PUT', 'http://10.2.129.232:3000/api/1/t0001',
            headers={
                'Content-type': 'application/x-www-form-urlencoded',
            },
            body=urllib.urlencode({'json': json.dumps(config)}))
        response = conn.getresponse()
        print response.read()
        return

    if sys.argv[1] == 'start':
        status, headers, response = request('POST', 'http://10.2.129.232:3000/api/1/t0001/start')
        print status, response
        return

    if sys.argv[1] == 'stop':
        status, headers, response = request('POST', 'http://10.2.129.232:3000/api/1/t0001/stop')
        print status, response
        return

    if sys.argv[1] == 'delete':
        status, headers, response = request('DELETE', 'http://10.2.129.232:3000/api/1/t0001')
        print status, response
        return

    if sys.argv[1] == 'status':
        status, headers, response = request('GET', 'http://10.2.129.232:3000/api/1/t0001')
        print response
        return

if __name__ == '__main__':
    sys.exit(main())
