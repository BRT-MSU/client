import sys
import signal
import argparse
import socket
import threading
import Queue

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

        self.serverQueue = Queue.Queue()

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.serverThread = threading.Thread(name = 'serverThread', target = self.openServerSocket)
        self.serverThread.daemon = True
        self.serverThread.start()

        self.handshakeThread = threading.Thread(name = 'handshakeThread', target = self.initiateHandShake)
        self.handshakeThread.daemon = True
        self.handshakeThread.start()

    def initiateHandShake(self):
        print 'Initiating handshake.'
        while True:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                clientSocket.connect((self.clientIPAddress, self.clientPortNumber))
                print 'Client sent message: SYN'
                clientSocket.send('SYN')

                if clientSocket.recv(DEFAULT_BUFFER_SIZE) == 'ACK':
                    print 'Client received message: ACK'
                    clientSocket.shutdown(socket.SHUT_WR)
                    clientSocket.close()
                    self.send('SYN-ACK')
                    print 'Handshake successful.'
                else:
                    pass
                break
            except socket.error:
                continue

    def send(self, message):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            clientSocket.connect((self.clientIPAddress, self.clientPortNumber))
            print 'Client sent message:', message
            clientSocket.send(message)
            clientSocket.shutdown(socket.SHUT_WR)
            clientSocket.close()
        except socket.error:
            pass

    def getMessage(self):
        if not self.serverQueue.empty():
            return self.serverQueue.get()
        else:
            return None

    def openServerSocket(self):
        self.serverSocket.bind((self.serverIPAddress, self.serverPortNumber))
        self.serverSocket.listen(1)
        while True:
            try:
                connection, address = self.serverSocket.accept()
                data = connection.recv(self.bufferSize)
                if data == 'SYN':
                    print 'Server sent message: ACK'
                    connection.send('ACK')
                else:
                    print 'Server received message:', data
                    self.serverQueue.put(data)
            except socket.error:
                break

    def closeServerSocket(self):
        try:
            self.serverSocket.shutdown(socket.SHUT_RD)
            self.serverSocket.close()
        except socket.error:
            pass

        self.serverThread.stop = True
        self.handshakeThread.stop = True
        print 'Connection closed.'

def main(serverIPAddress = SERVER_IP_ADDRESS, serverPortNumber = SERVER_PORT_NUMBER, \
        clientIPAddress = CLIENT_IP_ADDRESS, clientPortNumber = CLIENT_PORT_NUMBER, \
         bufferSize = DEFAULT_BUFFER_SIZE):
    return Connection(serverIPAddress, serverPortNumber, \
                              clientIPAddress, clientPortNumber, \
                                bufferSize)

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
