import pickle,threading
from og_log import LOG
from og_messaging.net.svr.handler import RequestHandler


class UDPRequestHandler(RequestHandler):

    def _set_name(self):
        threading.currentThread().setName(self.server.name+':'+''.join((hex(int(i))[2:].ljust(2, '0') for i in self.client_address[0].split('.')))+hex(self.client_address[1])[2:])

class ThreadedUDPRequestHandler(UDPRequestHandler):

    def handle(self):
        try:
            self._set_name()
            item = pickle.loads(self.request[0])
            LOG.debug(str(self.server.server_address)+" <- "+str(self.client_address)+" Received: " + str(item))
            self._send(self.server.callback(item))
        except Exception as e:
            LOG.error("Failure : "+str(e))

    def _send(self,msg):
        LOG.debug(str(self.server.server_address)+" -> "+str(self.client_address)+" Sending: " + str(msg))
        self.request[1].sendto(pickle.dumps(msg),self.client_address)
