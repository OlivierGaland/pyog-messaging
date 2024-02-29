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

from og_messaging.net.svr.tcp.server import ThreadedTCPServer,ThreadedPersistentTCPServer
from og_messaging.net.client.tcp.client import TCPClient,PersistentTCPClient
from og_messaging.msg.ping import PingQuery

LOG.start()

if __name__ == '__main__':

    server_addr = ('172.16.2.7', 9212)

    server = ThreadedTCPServer(server_addr,name="Svr")
    server.do_start()
    client = TCPClient(server_addr,buffer_size = 1024)

    try:
        while True:
            msg = PingQuery()
            client.send_nonsuspended(msg)

            time.sleep(3)
    except KeyboardInterrupt:
        LOG.info("Keyboard Interrupt")
        client.disconnect()

    server.do_shutdown()
