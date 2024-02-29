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

from og_messaging.net.svr.tcp.server import ThreadedPersistentTCPServer
from og_messaging.net.client.tcp.client import PersistentTCPClient
from og_messaging.msg.ping import PingQuery

LOG.start()

if __name__ == '__main__':

    server_addr = ('172.16.2.7', 9212)

    server = ThreadedPersistentTCPServer(server_addr,name="Svr",cnx_duration=30,cnx_timeout=5)
    server.do_start()
    client = PersistentTCPClient(server_addr,buffer_size = 1024)

    LOG.info("Test case : TCP Persistent connection : suspended/nonsuspended")

    try:
        while True:

            msg = PingQuery()            
            LOG.debug("Send nonsuspended")
            client.send_nonsuspended(msg)

            LOG.debug("Send suspended")
            client.send_suspended(msg)

            time.sleep(3)
    except KeyboardInterrupt:
        LOG.info("Keyboard Interrupt")
        client.disconnect()

    server.do_shutdown()
