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
from PyQt5 import Qt, QtCore, QtGui, QtWidgets

forwardToTangoString = '-t'
forwardToMotorString = '-m'

class Window(QWidget):
    def __init__(self, client):
        super(Window, self).__init__()

        self.client = client

        self.initUI()
        
    def initUI(self):
        clientStatusLabel = QtWidgets.QLabel('Client status:')
        self.clientStatusBar = QtWidgets.QStatusBar()

        serverStatusLabel = QtWidgets.QLabel('Server Status:')
        self.serverStatusBar = QtWidgets.QStatusBar()

        self.openConnectionButton = QtWidgets.QPushButton('Open Connection', self)
        self.openConnectionButton.clicked.connect(self.openConnection)

        self.closeConnectionButton = QtWidgets.QPushButton('Close Connection', self)
        self.closeConnectionButton.clicked.connect(self.closeConnection)
        self.closeConnectionButton.setEnabled(False)

        grid =  QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(clientStatusLabel, 1, 0)
        grid.addWidget(self.clientStatusBar, 1, 1)

        grid.addWidget(serverStatusLabel, 2, 0)
        grid.addWidget(self.serverStatusBar, 2, 1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
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

    def keyPressEvent(self, QKeyEvent):
        if not self.openConnectionButton.isEnabled():
            if QKeyEvent.key() == QtCore.Qt.Key_W:
                self.client.sendMessage(forwardToMotorString + 'W500')
            elif QKeyEvent.key() == QtCore.Qt.Key_S:
                self.client.sendMessage(forwardToMotorString + 'S500')
            elif QKeyEvent.key() == QtCore.Qt.Key_A:
                self.client.sendMessage(forwardToMotorString + 'A')
            elif QKeyEvent.key() == QtCore.Qt.Key_D:
                self.client.sendMessage(forwardToMotorString + 'D')

    def openConnection(self):
        self.client.openConnection()

        self.openConnectionButton.setEnabled(False)
        self.closeConnectionButton.setEnabled(True)

    def closeConnection(self):
        quit_msg = 'Are you sure you want to close the connection?'
        reply = QtWidgets.QMessageBox.question(self, 'Message', \
                                               quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.client.closeConnection()

            self.openConnectionButton.setEnabled(True)
            self.closeConnectionButton.setEnabled(False)


    def closeEvent(self, QCloseEvent):
        quit_msg = 'Are you sure you want to exit the client?'
        reply = QtWidgets.QMessageBox.question(self, 'Message', \
                                               quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.client.shutdown()
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

def main(client):
    app = QApplication(sys.argv)
    window = Window(client)
    sys.exit(app.exec_())
    return window

if __name__ == '__main__':
    main()
