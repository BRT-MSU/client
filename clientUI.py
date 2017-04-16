import sys
import messageLib
import enum
 
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

class motor(enum.Enum):
    DRIVE_MOTORS = 0
    ACTUATOR = 1
    BUCKET = 2
    SERVO = 3

# Default motor speeds {DRIVE_MOTORS, ACTUATOR, BUCKET, SERVO}
MOTOR_SPEEDS = {0: 25, 1: 25, 2: 25, 3: 25}
MAX_MOTOR_SPEED = 100

class Window(QWidget):
    def __init__(self, client):
        super(Window, self).__init__()

        self.client = client

        self.driveKeysPressed = []

        self.actuatorKeysPressed = []

        self.bucketKeysPressed = []

        self.motorSpeedToAdjust = motor.DRIVE_MOTORS

        self.initUI()
        
    def initUI(self):
        # Client status
        clientStatusLabel = QtWidgets.QLabel('Client status:')
        self.clientStatusBar = QtWidgets.QStatusBar()

        # Server status
        serverStatusLabel = QtWidgets.QLabel('Server Status:')
        self.serverStatusBar = QtWidgets.QStatusBar()

        # Button to open the connection
        self.openConnectionButton = QtWidgets.QPushButton('Open Connection', self)
        self.openConnectionButton.clicked.connect(self.openConnectionEvent)
        self.openConnectionButton.setFocusPolicy(QtCore.Qt.NoFocus)

        # Button to close the connection
        self.closeConnectionButton = QtWidgets.QPushButton('Close Connection', self)
        self.closeConnectionButton.clicked.connect(self.closeConnectionEvent)
        self.closeConnectionButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.closeConnectionButton.setEnabled(False)

        # Button to activate autonomy
        self.activateAutonomyButton = QtWidgets.QPushButton('Activate Autonomy', self)
        self.activateAutonomyButton.clicked.connect(self.activateAutonomyEvent)
        self.activateAutonomyButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.activateAutonomyButton.setEnabled(False)

        # Button to deactivate autonomy
        self.deactivateAutonomyButton = QtWidgets.QPushButton('Deactivate Autonomy', self)
        self.deactivateAutonomyButton.clicked.connect(self.deactivateAutonomyEvent)
        self.deactivateAutonomyButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.deactivateAutonomyButton.setEnabled(False)

        grid =  QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(clientStatusLabel, 1, 0)
        grid.addWidget(self.clientStatusBar, 1, 1)

        grid.addWidget(serverStatusLabel, 2, 0)
        grid.addWidget(self.serverStatusBar, 2, 1)

        hBox0 = QtWidgets.QHBoxLayout()
        hBox0.addStretch(1)
        hBox0.addWidget(self.openConnectionButton)
        hBox0.addWidget(self.closeConnectionButton)

        hBox1 = QtWidgets.QHBoxLayout()
        hBox1.addStretch(1)
        hBox1.addWidget(self.activateAutonomyButton)
        hBox1.addWidget(self.deactivateAutonomyButton)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(grid)
        vbox.addLayout(hBox0)
        vbox.addLayout(hBox1)
        
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

    def keyPressEvent(self, event):
        if self.openConnectionButton.isEnabled() \
                or self.deactivateAutonomyButton.isEnabled():
            return

        key = event.key()

        if not event.isAutoRepeat():
            # Driving logic
            if key == QtCore.Qt.Key_W:
                if key not in self.driveKeysPressed:
                    self.driveKeysPressed.append(key)

                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'l': MOTOR_SPEEDS[motor.DRIVE_MOTORS], 'r': MOTOR_SPEEDS[motor.DRIVE_MOTORS]}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)
            elif key == QtCore.Qt.Key_S:
                if key not in self.driveKeysPressed:
                    self.driveKeysPressed.append(key)

                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'l': -1 * MOTOR_SPEEDS[motor.DRIVE_MOTORS], 'r': -1 * MOTOR_SPEEDS[motor.DRIVE_MOTORS]}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)
            elif key == QtCore.Qt.Key_A:
                if key not in self.driveKeysPressed:
                    self.driveKeysPressed.append(key)

                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'l': -1 * MOTOR_SPEEDS[motor.DRIVE_MOTORS], 'r': 1 * MOTOR_SPEEDS[motor.DRIVE_MOTORS]}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)
            elif key == QtCore.Qt.Key_D:
                if key not in self.driveKeysPressed:
                    self.driveKeysPressed.append(key)

                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'l': 1 * MOTOR_SPEEDS[motor.DRIVE_MOTORS], 'r': -1 * MOTOR_SPEEDS[motor.DRIVE_MOTORS]}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)

            # Motor speed adjustment mode logic
            elif key == QtCore.Qt.Key_1:
                self.motorSpeedToAdjust = motor.DRIVE_MOTORS
                print 'Motor speed adjustment mode:', str(self.motorSpeedToAdjust)
            elif key == QtCore.Qt.Key_2:
                self.motorSpeedToAdjust = motor.ACTUATOR
                print 'Motor speed adjustment mode:', str(self.motorSpeedToAdjust)
            elif key == QtCore.Qt.Key_3:
                self.motorSpeedToAdjust = motor.BUCKET
                print 'Motor speed adjustment mode:', str(self.motorSpeedToAdjust)
            elif key == QtCore.Qt.Key_4:
                self.motorSpeedToAdjust = motor.SERVO
                print 'Motor speed adjustment mode:', str(self.motorSpeedToAdjust)

            # Actuator logic
            elif key == QtCore.Qt.Key_U:
                if key not in self.actuatorKeysPressed:
                    self.actuatorKeysPressed.append(key)

                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'a': MOTOR_SPEEDS[motor.ACTUATOR]}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)
            elif key == QtCore.Qt.Key_J:
                if key not in self.actuatorKeysPressed:
                    self.actuatorKeysPressed.append(key)

                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'a': -1 * MOTOR_SPEEDS[motor.ACTUATOR]}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)

            # Bucket logic
            elif key == QtCore.Qt.Key_I:
                if key not in self.bucketKeysPressed:
                    self.bucketKeysPressed.append(key)

                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'b': MOTOR_SPEEDS[motor.BUCKET]}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)
            elif key == QtCore.Qt.Key_K:
                if key not in self.bucketKeysPressed:
                    self.bucketKeysPressed.append(key)

                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'b': -1 * MOTOR_SPEEDS[motor.BUCKET]}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)

        # Motor speed adjustment logic
        if key == QtCore.Qt.Key_Up:
            if MOTOR_SPEEDS[self.motorSpeedToAdjust] < MAX_MOTOR_SPEED:
                MOTOR_SPEEDS[self.motorSpeedToAdjust] += 1
                print MOTOR_SPEEDS[self.motorSpeedToAdjust]
                if len(self.driveKeysPressed):
                    self.keyPressEvent(Qt.QKeyEvent(Qt.QEvent.KeyPress, self.driveKeysPressed[-1], QtCore.Qt.NoModifier))
        elif key == QtCore.Qt.Key_Down:
            if MOTOR_SPEEDS[self.motorSpeedToAdjust] > 0:
                MOTOR_SPEEDS[self.motorSpeedToAdjust] -= 1
                print MOTOR_SPEEDS[self.motorSpeedToAdjust]
                if len(self.driveKeysPressed):
                    self.keyPressEvent(Qt.QKeyEvent(Qt.QEvent.KeyPress, self.driveKeysPressed[-1], QtCore.Qt.NoModifier))

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat() or self.openConnectionButton.isEnabled() \
                or self.deactivateAutonomyButton.isEnabled():
            return

        key = event.key()

        if key in self.driveKeysPressed:
            self.driveKeysPressed.remove(key)

        if key in self.actuatorKeysPressed:
            self.actuatorKeysPressed.remove(key)

        if key in self.bucketKeysPressed:
            self.bucketKeysPressed.remove(key)

        # Driving logic
        if not len(self.driveKeysPressed):
            if key == QtCore.Qt.Key_W:
                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'l': 0, 'r': 0}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)
            elif key == QtCore.Qt.Key_S:
                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'l': 0, 'r': 0}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)
            elif key == QtCore.Qt.Key_A:
                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'l': 0, 'r': 0}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)
            elif key == QtCore.Qt.Key_D:
                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'l': 0, 'r': 0}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)

        # Actuator logic
        if not len(self.actuatorKeysPressed):
            if key == QtCore.Qt.Key_U:
                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'a': 0}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)
            elif key == QtCore.Qt.Key_J:
                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'a': 0}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)

        # Bucket logic
        if not len(self.bucketKeysPressed):
            if key == QtCore.Qt.Key_I:
                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'b': 0}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)
            elif key == QtCore.Qt.Key_K:
                forwardingPrefix = messageLib.forwardingPrefix.MOTOR
                subMessages = {'b': 0}
                message = messageLib.Message(forwardingPrefix, subMessages).message
                self.client.sendMessage(message)


    def openConnectionEvent(self):
        self.client.openConnection()

        self.openConnectionButton.setEnabled(False)
        self.closeConnectionButton.setEnabled(True)

        self.activateAutonomyButton.setEnabled(True)

    def closeConnectionEvent(self):
        if self.deactivateAutonomyButton.isEnabled():
            autonomyMessage = 'Please deactivate autonomy first.'
            QtWidgets.QMessageBox.question(self, 'Message', \
                                           autonomyMessage, QtWidgets.QMessageBox.Ok)
            return

        quitMessage = 'Are you sure you want to close the connection?'
        reply = QtWidgets.QMessageBox.question(self, 'Message', \
                                               quitMessage, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.client.closeConnection()

            self.openConnectionButton.setEnabled(True)
            self.closeConnectionButton.setEnabled(False)

            self.activateAutonomyButton.setEnabled(False)
            self.deactivateAutonomyButton.setEnabled(False)

    def activateAutonomyEvent(self):
        quit_msg = 'Are you sure you want to activate autonomy?'
        reply = QtWidgets.QMessageBox.question(self, 'Message', \
                                               quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.activateAutonomy()

    def activateAutonomy(self):
        self.client.sendMessage(messageLib.forwardingPrefix.CONTROLLER + messageLib.AUTONOMOY_ACTIVATION_MESSAGE)

        self.activateAutonomyButton.setEnabled(False)
        self.deactivateAutonomyButton.setEnabled(True)

    def deactivateAutonomyEvent(self):
        deactivateMessage = 'Are you sure you want to deactivate autonomy?'
        reply = QtWidgets.QMessageBox.question(self, 'Message', \
                                               deactivateMessage, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.deactivateAutonomy()

    def deactivateAutonomy(self):
        self.client.sendMessage(messageLib.forwardingPrefix.CONTROLLER + messageLib.AUTONOMY_DEACTIVATION_MESSAGE)

        self.activateAutonomyButton.setEnabled(True)
        self.deactivateAutonomyButton.setEnabled(False)

    def closeEvent(self, QCloseEvent):
        quitMessage = 'Are you sure you want to exit the client?'
        reply = QtWidgets.QMessageBox.question(self, 'Message', \
                                               quitMessage, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            if self.deactivateAutonomyButton.isEnabled():
                self.deactivateAutonomy()

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
