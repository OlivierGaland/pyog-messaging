import socket,pickle
from og_log import LOG
from og_messaging.net.client.client import Client

class TCPClient(Client):
    DEFAULT_BUFFER_SIZE = 4096

    def __init__(self,server_addr,**kwargs):
        self.buffer_size = TCPClient.DEFAULT_BUFFER_SIZE if 'buffer_size' not in kwargs.keys() else kwargs['buffer_size']
        super().__init__(server_addr,**kwargs)

    def send_suspended(self,msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server_addr)
        LOG.debug(str(sock.getsockname())+" -> "+str(sock.getpeername())+" Sending: " + str(msg))

        sock.sendall(pickle.dumps(msg))
        response = sock.recv(self.buffer_size)
        item = pickle.loads(response)

        LOG.debug(str(sock.getsockname())+" <- "+str(sock.getpeername())+" Received: " + str(item))
        return item

class PersistentTCPClient(TCPClient):

    def __init__(self,server_addr,**kwargs):
        super().__init__(server_addr,**kwargs)
        self.sock = None
        self.connect()

    def connect(self):
        if self.sock is None:
            self.reconnect()

    def reconnect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.server_addr)

    def disconnect(self):
        if self.sock is not None:
            self.sock.close()

    def __del__(self):
        if self.sock is not None:
            self.disconnect()

    def send_suspended(self,msg):
        LOG.debug(str(self.sock.getsockname())+" -> "+str(self.sock.getpeername())+" Sending: " + str(msg))

        self.sock.sendall(pickle.dumps(msg))
        try:
            response = self.sock.recv(self.buffer_size)
        except Exception as e:
            LOG.warning("Cannot send message, reconnecting : "+str(e))
            self.reconnect()
            self.sock.sendall(pickle.dumps(msg))
            response = self.sock.recv(self.buffer_size)
        item = pickle.loads(response)

        LOG.debug(str(self.sock.getsockname())+" <- "+str(self.sock.getpeername())+" Received: " + str(item))
        return item
