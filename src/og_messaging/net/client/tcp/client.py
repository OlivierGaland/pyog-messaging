import socket,pickle
from og_log import LOG
from og_messaging.net.client.client import Client

class TCPClient(Client):
    DEFAULT_BUFFER_SIZE = 4096

    def __init__(self,server_addr,**kwargs):
        self.buffer_size = TCPClient.DEFAULT_BUFFER_SIZE if 'buffer_size' not in kwargs.keys() else kwargs['buffer_size']
        super().__init__(server_addr,**kwargs)

    def _get_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server_addr)
        return sock
    
    def _send(self,sock,msg):
        LOG.debug(str(sock.getsockname())+" -> "+str(sock.getpeername())+" Sending: " + str(msg))
        sock.sendall(pickle.dumps(msg))

    def _receive(self,sock):
        reply = pickle.loads(sock.recv(self.buffer_size))
        LOG.debug(str(sock.getsockname())+" <- "+str(sock.getpeername())+" Received: " + str(reply))
        return reply

    def send_suspended(self,msg):
        sock = self._get_socket()
        self._send(sock,msg)
        reply = self._receive(sock)
        self.callback(reply)
        return reply

class PersistentTCPClient(TCPClient):

    def __init__(self,server_addr,**kwargs):
        super().__init__(server_addr,**kwargs)
        self.sock = None
        self.connect()

    def __del__(self):
        if self.sock is not None:
            self.disconnect()

    def _get_socket(self):
        return self.sock
    
    def connect(self):
        if self.sock is None:
            self.reconnect()

    def reconnect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.server_addr)

    def disconnect(self):
        if self.sock is not None:
            self.sock.close()

    def send_suspended(self,msg):
        sock = self._get_socket()
        self._send(sock,msg)

        try:
            reply = self._receive(sock)
            self.callback(reply)
            return reply
        except Exception as e:
            LOG.warning("Cannot send message, reconnecting : "+str(e))
            self.reconnect()
            return self.send_suspended(msg)
