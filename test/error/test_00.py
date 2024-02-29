# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# https://pypi.org/classifiers/
#
# build : python -m build
# upload :
# twine check dist/*

import sys,time
sys.path.append('src')
from og_log import LOG

from og_messaging.net.svr.tcp.server import ThreadedTCPServer
from og_messaging.net.client.tcp.client import TCPClient
from og_messaging.msg.message import QueryMessage,ErrorMessage


class ErrorQuery(QueryMessage):

    def execute(self,**kwargs):
        return ErrorMessage(255,"Requested ErrorMessage")


LOG.start()

if __name__ == '__main__':

    server_addr = ('172.16.2.7', 9212)

    server = ThreadedTCPServer(server_addr,name="Svr")
    server.do_start()
    client = TCPClient(server_addr,buffer_size = 1024)

    try:
        while True:

            try:
                msg = ErrorQuery()
                client.send_suspended(msg)
            except Exception as e:
                LOG.info("Exception : "+str(e))

            time.sleep(3)
    except KeyboardInterrupt:
        LOG.info("Keyboard Interrupt")

    server.do_shutdown()
