import socket,pickle
from og_log import LOG
from og_messaging.net.client.client import Client

class UDPClient(Client):
    DEFAULT_BUFFER_SIZE = 512

    def __init__(self,server_addr,**kwargs):
        self.buffer_size = UDPClient.DEFAULT_BUFFER_SIZE if 'buffer_size' not in kwargs.keys() else kwargs['buffer_size']
        super().__init__(server_addr,**kwargs)

    def _get_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _send(self,sock,msg):
        LOG.debug("('',?) -> "+str(self.server_addr)+" Sending: " + str(msg))
        sock.sendto(pickle.dumps(msg), self.server_addr)

    def _receive(self,sock):
        reply = pickle.loads(sock.recv(self.buffer_size))
        LOG.debug(str(sock.getsockname())+" <- "+str(self.server_addr)+" Received: " + str(reply))
        return reply    
    
    def send_suspended(self,msg):
        sock = self._get_socket() 
        self._send(sock,msg)
        reply = self._receive(sock)
        self.callback(reply)
        return reply        
