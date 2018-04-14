import argparse
import threading

from connection import Connection
import clientUI

DEFAULT_CLIENT_IP_ADDRESS = '0.0.0.0'
DEFAULT_CLIENT_PORT_NUMBER = 1123

DEFAULT_CONTROLLER_IP_ADDRESS = '192.168.1.3'
DEFAULT_CONTROLLER_PORT_NUMBER = 5813

DEFAULT_BUFFER_SIZE = 1024


class Client:
    def __init__(self, client_ip_address, client_port_number,
                 controller_ip_address, controller_port_number,
                 buffer_size):
        self.client_ip_address = client_ip_address
        self.client_port_number = client_port_number

        self.controller_ip_address = controller_ip_address
        self.controller_port_number = controller_port_number

        self.buffer_size = buffer_size

        self.connection = None
        self.connection_thread = None

        clientUI.main(self)

    def open_connection(self):
        self.connection = Connection(self.client_ip_address, self.client_port_number,
                                     self.controller_ip_address, self.controller_port_number,
                                     self.buffer_size)

        self.connection_thread = threading.Thread(name='connectionThread', target=self.run)
        self.connection_thread.daemon = True
        self.connection_thread.start()

    def send_message(self, message):
        self.connection.send(message)

    def run(self):
        while True:
            message_received = self.connection.get_message()
            if message_received is not None:
                pass

    def close_connection(self):
        try:
            self.connection_thread.stop = True
            self.connection.close_local_socket()
        except AttributeError:
            pass

    def shutdown(self):
        try:
            self.connection_thread.stop = True
            self.connection.close_local_socket()
        except AttributeError:
            pass


def main(client_ip_address, client_port_number,
         controller_ip_address, controller_port_number,
         buffer_size):
        return Client(client_ip_address, client_port_number,
                      controller_ip_address, controller_port_number,
                      buffer_size)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-cip', '--clientIPAddress', help='client IP address',
                        required=False, default=DEFAULT_CLIENT_IP_ADDRESS)
    parser.add_argument('-cpn', '--clientPortNumber', help='client port number',
                        required=False, type=int, default=str(DEFAULT_CLIENT_PORT_NUMBER))
    parser.add_argument('-kip', '--controllerIPAddress', help='controller IP address',
                        required=False, default=DEFAULT_CONTROLLER_IP_ADDRESS)
    parser.add_argument('-kpn', '--controllerPortNumber', help='controller port number',
                        required=False, type=int, default=str(DEFAULT_CONTROLLER_PORT_NUMBER))
    parser.add_argument('-bs', '--bufferSize', help='buffer size',
                        required=False, type=int, default=str(DEFAULT_BUFFER_SIZE))
    args = parser.parse_args()

    print 'clientIpAddress:', args.clientIPAddress
    print 'clientPortNumber:', args.clientPortNumber
    print 'controllerIpAddress:', args.controllerIPAddress
    print 'controllerPortNumber:', args.controllerPortNumber
    print 'bufferSize:', args.bufferSize

    main(args.clientIPAddress, args.clientPortNumber,
         args.controllerIPAddress, args.controllerPortNumber,
         args.bufferSize)
