from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Got Request")
        url = urlparse(self.path)
        data = parse_qs(url.query)
        self.server.callback(data['code'][0])
        self.send_response(200)
        self.end_headers()


class Server(HTTPServer):
    def __init__(self, *args):
        super(Server, self).__init__(*args)
    
    def setCallback(self,callback):
        self.callback = callback

# Class: OathResponseListener
# Listens for a response from google containing an oath authorization token
class OathResponseListener(object):
    # Constructor
    # Params
    # address: address of the internal server
    # port: port to listen for requests on
    def __init__(self, address, port):
        def cb(content):
            self.content = content
        self.server = Server((address,port), RequestHandler)
        self.server.setCallback(cb)
        self.server.timeout = 60
        self.content = ""
        self.server.handle_request()