import threading
from og_log import LOG


class Server():
    DEFAULT_BUFFER_SIZE = 4096
    DEFAULT_SERVER_NAME = 'Server'
 
    def __init__(self,addr,handler_cls,**kwargs):
        self.name = Server.DEFAULT_SERVER_NAME if 'name' not in kwargs.keys() else kwargs['name']
        self.buffer_size = Server.DEFAULT_BUFFER_SIZE if 'buffer_size' not in kwargs.keys() else kwargs['buffer_size']
        self.server_thread = None
        super().__init__(addr,handler_cls)

    def do_start(self):
        LOG.info("Starting server : "+self.name)
        self.server_thread = threading.Thread(target=self.serve_forever,name=self.name)
        self.server_thread.daemon = True
        self.server_thread.start()
        
    def do_shutdown(self):
        if self.server_thread is not None:
            LOG.info("Stopping server : "+self.name)
            self.shutdown()
            self.server_thread.join()
            self.server_thread = None

    def __del__(self):
        self.do_shutdown()     

    def _process_msg(self,msg):
        return msg.execute()          

#class ThreadedUDPServer(socketserver.ThreadingMixIn, ThreadedUDPServer, socketserver.UDPServer): pass

