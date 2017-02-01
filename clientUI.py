import argparse
import sys
import atexit
import connection
 
# SIP allows us to select the API we wish to use
import sip
 
# use the more modern PyQt API (not enabled by default in Python 2.x);
# must precede importing any module that provides the API specified
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QString', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QVariant', 2)

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui, QtWidgets

SERVER_IP_ADDRESS = '0.0.0.0'
SERVER_PORT_NUMBER = 9996
CLIENT_IP_ADDRESS = 'localhost'
CLIENT_PORT_NUMBER = 8887
DEFAULT_BUFFER_SIZE = 1024

TEST_STRING = 'Hello, World!'

class Window(QWidget):
    def __init__(self, serverIPAddress, serverPortNumber, \
                       clientIPAddress, clientPortNumber, \
                        bufferSize):
        super(Window, self).__init__()

        self.serverIPAddress = serverIPAddress
        self.serverPortNumber = serverPortNumber
        self.clientIPAddress = clientIPAddress
        self.clientPortNumber = clientPortNumber
        self.bufferSize = bufferSize

        self.initUI()
        
    def initUI(self):
        connectionStatusLabel = QtWidgets.QLabel('Connection Status:')
        self.connectionStatusBar = QtWidgets.QStatusBar()

        self.sendMessageButton = QtWidgets.QPushButton('Send Message', self)
        self.sendMessageButton.clicked.connect(self.sendMessage)
        self.sendMessageButton.setEnabled(False)

        self.openConnectionButton = QtWidgets.QPushButton('Open Connection', self)
        self.openConnectionButton.clicked.connect(self.openConnection)

        self.closeConnectionButton = QtWidgets.QPushButton('Close Connection', self)
        self.closeConnectionButton.clicked.connect(self.closeConnection)
        self.closeConnectionButton.setEnabled(False)

        grid =  QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(connectionStatusLabel, 1, 0)
        grid.addWidget(self.connectionStatusBar, 1, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.sendMessageButton)
        hbox.addWidget(self.openConnectionButton)
        hbox.addWidget(self.closeConnectionButton)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(grid)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.resize(500, 400)
        self.center()
        
        self.setWindowTitle('Client')
        self.setWindowIcon(QtGui.QIcon('mars.png'))
    
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def sendMessage(self):
        self.connection.send(TEST_STRING)

    def openConnection(self):
        self.connection = connection.Connection(serverIPAddress = self.serverIPAddress, \
                                                serverPortNumber = self.serverPortNumber, \
                                                clientIPAddress = self.clientIPAddress, \
                                                clientPortNumber = self.clientPortNumber,
                                                bufferSize = self.bufferSize)
        atexit.register(self.connection.closeServerSocket)

        self.connectionStatusBar.showMessage('Connection opened...')

        self.openConnectionButton.setEnabled(False)
        self.sendMessageButton.setEnabled(True)
        self.closeConnectionButton.setEnabled(True)

    def closeConnection(self):
        self.connection.closeServerSocket()
        self.connectionStatusBar.showMessage('Connection closed...')

        self.openConnectionButton.setEnabled(True)
        self.sendMessageButton.setEnabled(False)
        self.closeConnectionButton.setEnabled(False)


    def closeEvent(self, QCloseEvent):
        if self.closeConnectionButton.isEnabled() is True:
            self.connection.closeServerSocket()

def main(serverIPAddress=SERVER_IP_ADDRESS, serverPortNumber=SERVER_PORT_NUMBER, \
             clientIPAddress=CLIENT_IP_ADDRESS, clientPortNumber=CLIENT_PORT_NUMBER, \
                bufferSize = DEFAULT_BUFFER_SIZE):
    app = QApplication(sys.argv)
    ex = Window(serverIPAddress, serverPortNumber, \
                clientIPAddress, clientPortNumber, \
                bufferSize)
    sys.exit(app.exec_())

if __name__ == '__main__':
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
