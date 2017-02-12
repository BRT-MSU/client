import argparse
import threading

import connection
import clientUI

class Client():
    def __init__(self, serverIPAddress, serverPortNumber, \
                 clientIPAddress, clientPortNumber, bufferSize):
        self.serverIPAddress = serverIPAddress
        self.serverPortNumber = serverPortNumber
        self.clientIPAddress = clientIPAddress
        self.clientPortNumber = clientPortNumber
        self.bufferSize = bufferSize

        self.messageToSend = 'Hello, World.'
        self.messageReceived = None

        self.clientUI = clientUI.main(self)

        self.connection = None

    def openConnection(self):
        self.connection = connection.main(self.serverIPAddress, self.serverPortNumber, \
                                          self.clientIPAddress, self.clientPortNumber, \
                                          self.bufferSize)

        self.connectionThread = threading.Thread(name='connectionThread', target=self.run)
        self.connectionThread.daemon = True
        self.connectionThread.start()

    def sendMessage(self):
        self.connection.send(self.messageToSend)

    def run(self):
        while True:
            messageReceived = self.connection.getMessage()
            if messageReceived is not None:
                self.messageReceived = messageReceived

    def closeConnection(self):
        try:
            self.connectionThread.stop = True
            self.connection.closeServerSocket()
        except AttributeError:
            pass

    def shutdown(self):
        try:
            self.connectionThread.stop = True
            self.connection.closeServerSocket()
        except AttributeError:
            pass

def main(serverIPAddress=connection.SERVER_IP_ADDRESS, serverPortNumber=connection.SERVER_PORT_NUMBER, \
            clientIPAddress=connection.CLIENT_IP_ADDRESS, clientPortNumber=connection.CLIENT_PORT_NUMBER, \
            bufferSize=connection.DEFAULT_BUFFER_SIZE):
        return Client(serverIPAddress, serverPortNumber, clientIPAddress, clientPortNumber, bufferSize)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-sip', '--serverIPAddress', help='server IP address argument', \
                        required=False, default=connection.SERVER_IP_ADDRESS)
    parser.add_argument('-spn', '--serverPortNumber', help='server port number argument', \
                        required=False, default=str(connection.SERVER_PORT_NUMBER))
    parser.add_argument('-cip', '--clientIPAddress', help='client IP address argument', \
                        required=False, default=connection.CLIENT_IP_ADDRESS)
    parser.add_argument('-cpn', '--clientPortNumber', help='client port number argument', \
                        required=False, default=str(connection.CLIENT_PORT_NUMBER))
    parser.add_argument('-bs', '--bufferSize', help='buffer size argument', \
                        required=False, default=str(connection.DEFAULT_BUFFER_SIZE))
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