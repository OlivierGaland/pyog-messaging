import socketserver,threading,pickle
from og_log import LOG

class RequestHandler(socketserver.BaseRequestHandler):

    def _send(self,msg):
        LOG.debug(str(self.request.getsockname())+" -> "+str(self.request.getpeername())+" Sending: " + str(msg))
        self.request.sendall(pickle.dumps(msg))
