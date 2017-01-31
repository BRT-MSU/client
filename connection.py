import sys
import signal
import atexit
import argparse
import socket

SERVER_IP_ADDRESS = '0.0.0.0'
SERVER_PORT_NUMBER = 8887
CLIENT_IP_ADDRESS = 'localhost'
CLIENT_PORT_NUMBER = 9996
DEFAULT_BUFFER_SIZE = 1024

def endSignalHandler():
    sys.exit()

class Connection():
    def __init__(self, serverIPAddress, serverPortNumber, clientIPAddress, \
                 clientPortNumber, bufferSize):
        self.serverIPAddress = serverIPAddress
        self.serverPortNumber = serverPortNumber
        self.clientIPAddress = clientIPAddress
        self.clientPortNumber = clientPortNumber
        self.bufferSize = bufferSize

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send(self, message):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            clientSocket.connect((self.clientIPAddress, self.clientPortNumber))
            print 'Sent message:', message
            clientSocket.send(message)
            clientSocket.shutdown(socket.SHUT_RDWR)
            clientSocket.close()
        except socket.error:
            'Client socket unsuccessful.'
            pass

    def openServerSocket(self):
        self.serverSocket.bind((self.serverIPAddress, self.serverPortNumber))
        self.serverSocket.listen(1)
        while True:
            try:
                print 'Server listening.'
                connection, address = self.serverSocket.accept()
                data = connection.recv(self.bufferSize)
                if data:
                    print 'Received data:', data
            except socket.error:
                break

    @atexit.register
    def closeServerSocket(self):
        self.serverSocket.shutdown(socket.SHUT_RD)
        self.serverSocket.close()
        print 'Connection closed.'

def main(serverIPAddress = SERVER_IP_ADDRESS, serverPortNumber = SERVER_PORT_NUMBER, \
        clientIPAddress = CLIENT_IP_ADDRESS, clientPortNumber = CLIENT_PORT_NUMBER, \
         bufferSize = DEFAULT_BUFFER_SIZE):
    connection = Connection(serverIPAddress, serverPortNumber, \
                              clientIPAddress, clientPortNumber, \
                                bufferSize)
    connection.openServerSocket()

if __name__ == '__main__':
    signal.signal(signal.SIGTSTP, endSignalHandler)

    parser = argparse.ArgumentParser()
    parser.add_argument('-sip', '--serverIPAddress', help='server IP address argument', \
                        required=False, default=SERVER_IP_ADDRESS)
    parser.add_argument('-spn', '--serverPortNumber', help='server port number argument', \
                        required=False, default=str(SERVER_PORT_NUMBER))
    parser.add_argument('-cip', '--clientIPAddress', help = 'client IP address argument', \
                        required = False, default = CLIENT_IP_ADDRESS)
    parser.add_argument('-cpn', '--clientPortNumber', help = 'client port number argument', \
                        required = False, default = str(CLIENT_PORT_NUMBER))
    parser.add_argument('-bs', '--bufferSize', help='buffer size argument', \
                        required=False, default=str(DEFAULT_BUFFER_SIZE))
    args = parser.parse_args()

    serverIPAddress = args.serverIPAddress
    serverPortNumber = int(args.serverPortNumber)
    clientIPAddress = args.clientIPAddress
    clientPortNumber = int(args.clientPortNumber)
    bufferSize = int(args.bufferSize)

    print 'serverIpAddress:', serverIPAddress
    print 'serverPortNumber:', serverPortNumber
    print 'clientIpAddress:', clientIPAddress
    print 'clientPortNumber:', clientPortNumber
    print 'bufferSize:', bufferSize

    main(serverIPAddress, serverPortNumber, clientIPAddress, clientPortNumber, bufferSize)
