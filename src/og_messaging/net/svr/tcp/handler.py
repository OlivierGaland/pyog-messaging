import socket,time,pickle,threading
from og_log import LOG
from og_messaging.net.svr.handler import RequestHandler

class TCPRequestHandler(RequestHandler):

    def _set_name(self):
        threading.currentThread().setName(self.server.name+':'+''.join((hex(int(i))[2:].ljust(2, '0') for i in self.request.getpeername()[0].split('.')))+hex(self.request.getpeername()[1])[2:])


class ThreadedTCPRequestHandler(TCPRequestHandler):

    def handle(self):
        try:
            self._set_name()
            buff = self.request.recv(self.server.buffer_size)
            item = pickle.loads(buff)
            LOG.debug(str(self.request.getsockname())+" <- "+str(self.request.getpeername())+" Received: " + str(item))
            self._send((self.server.callback(item)))
            self.request.close()
        except Exception as e:
            LOG.error("Failure : "+str(e))

    def _send(self,msg):
        LOG.debug(str(self.request.getsockname())+" -> "+str(self.request.getpeername())+" Sending: " + str(msg))
        self.request.sendall(pickle.dumps(msg))

class ThreadedTCPPersistentRequestHandler(ThreadedTCPRequestHandler):

    def keep_alive(self):
        return (time.time() - self.start_time) < self.server.cnx_duration

    def handle(self):
        try:
            self._set_name()
            self.start_time = time.time()
            self.request.settimeout(self.server.cnx_timeout)
            while self.keep_alive():
                try:
                    buff = self.request.recv(self.server.buffer_size)
                except socket.timeout:
                    LOG.warning("Timeout : "+str(self.request.getpeername()))
                    continue
                item = pickle.loads(buff)
                LOG.debug(str(self.request.getsockname())+" <- "+str(self.request.getpeername())+" Received: " + str(item))
                self._send((self.server.callback(item)))
            LOG.debug("Killing connection : keep_alive Timeout : "+str(self.server.cnx_duration))
        except Exception as e:
            LOG.info("Connection closed from "+str(self.request.getpeername())+" : "+str(e))
        finally:
            self.request.close()
