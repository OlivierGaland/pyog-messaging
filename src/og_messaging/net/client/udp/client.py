import socket,pickle
from og_log import LOG
from og_messaging.net.client.client import Client

class UDPClient(Client):
    DEFAULT_BUFFER_SIZE = 512

    def __init__(self,server_addr,**kwargs):
        self.buffer_size = UDPClient.DEFAULT_BUFFER_SIZE if 'buffer_size' not in kwargs.keys() else kwargs['buffer_size']
        super().__init__(server_addr,**kwargs)

    def send_suspended(self,msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        LOG.debug("('',?) -> "+str(self.server_addr)+" Sending: " + str(msg))
        sock.sendto(pickle.dumps(msg), self.server_addr)
        response = sock.recv(self.buffer_size)
        item = pickle.loads(response)
        LOG.debug(str(sock.getsockname())+" <- "+str(self.server_addr)+" Received: " + str(item))
        return item
