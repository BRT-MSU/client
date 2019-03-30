import sys
from client_simulation import *
from message import *
import enum
import sip
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
 
# Use the more modern PyQt API (not enabled by default in Python 2.x);   
# must precede importing any module that provides the API specified
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QString', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QVariant', 2)

# Default motor speeds {DRIVE_MOTORS, ACTUATOR, BUCKET}
MOTOR_SPEEDS = {0: 100, 1: 100, 2: 100}

MAX_MOTOR_SPEED = 100
BUFFER = []

class Motor(enum.Enum):
    DRIVE_MOTORS = 0
    ACTUATOR = 1
    BUCKET = 2


class Window(QWidget):
    def __init__(self, client):
        super(Window, self).__init__()

        self.client = client

        self.drive_keys_pressed = []

        self.actuator_keys_pressed = []

        self.bucket_keys_pressed = []

        self.motor_speed_to_adjust = Motor.DRIVE_MOTORS.value

        self.init_ui()
        
    def init_ui(self):
        # Button to open the connection
        self.open_connection_button = QtWidgets.QPushButton('Open Connection', self)
        self.open_connection_button.clicked.connect(self.open_connection_event)
        self.open_connection_button.setFocusPolicy(QtCore.Qt.NoFocus)

        # Button to close the connection
        self.close_connection_button = QtWidgets.QPushButton('Close Connection', self)
        self.close_connection_button.clicked.connect(self.close_connection_event)
        self.close_connection_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.close_connection_button.setEnabled(False)

        # Button to activate autonomy
        self.activate_autonomy_button = QtWidgets.QPushButton('Activate Autonomy', self)
        self.activate_autonomy_button.clicked.connect(self.activate_autonomy_event)
        self.activate_autonomy_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.activate_autonomy_button.setEnabled(False)

        # Button to deactivate autonomy
        self.deactivate_autonomy_button = QtWidgets.QPushButton('Deactivate Autonomy', self)
        self.deactivate_autonomy_button.clicked.connect(self.deactivate_autonomy_event)
        self.deactivate_autonomy_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.deactivate_autonomy_button.setEnabled(False)

        # Button to run simulation
        self.simulation_button = QtWidgets.QPushButton('Simulation', self)
        self.simulation_button.move(0, 30)
        self.simulation_button.clicked.connect(self.simulation_event)
        self.simulation_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.simulation_button.setEnabled(True)

        # Button to run real time tracking
        self.real_time_tracking_button = QtWidgets.QPushButton('Real Time Tracking', self)
        self.real_time_tracking_button.clicked.connect(self.real_time_tracking_event)
        self.real_time_tracking_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.real_time_tracking_button.setEnabled(False)

        grid =  QtWidgets.QGridLayout()
        grid.setSpacing(10)

        h_box_0 = QtWidgets.QHBoxLayout()
        h_box_0.addStretch(1)
        h_box_0.addWidget(self.open_connection_button)
        h_box_0.addWidget(self.close_connection_button)

        h_box_1 = QtWidgets.QHBoxLayout()
        h_box_1.addStretch(1)
        h_box_1.addWidget(self.activate_autonomy_button)
        h_box_1.addWidget(self.deactivate_autonomy_button)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch(1)
        v_box.addLayout(grid)
        v_box.addLayout(h_box_0)
        v_box.addLayout(h_box_1)
        
        self.setLayout(v_box)
        
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
        if self.open_connection_button.isEnabled() \
                or self.deactivate_autonomy_button.isEnabled():
            return

        key = event.key()

        if not event.isAutoRepeat():
            # Driving logic
            if key == QtCore.Qt.Key_W:
                #BUFFER.append('W\n')
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value],
                                'r': MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_S:
                #BUFFER.append('S\n')
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': -1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value],
                                'r': -1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_A:
                #BUFFER.append('A\n')
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': -1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value],
                                'r': 1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_D:
                #BUFFER.append('D\n')
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': 1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value],
                                'r': -1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)

            # Motor speed adjustment mode logic
            elif key == QtCore.Qt.Key_1:
                #BUFFER.append('1\n')
                self.motor_speed_to_adjust = Motor.DRIVE_MOTORS.value
                print ('Motor speed adjustment mode:'), str(self.motor_speed_to_adjust)
            elif key == QtCore.Qt.Key_2:
                #BUFFER.append('2\n')
                self.motor_speed_to_adjust = Motor.ACTUATOR.value
                print ('Motor speed adjustment mode:'), str(self.motor_speed_to_adjust)
            elif key == QtCore.Qt.Key_3:
                #BUFFER.append('3\n')
                self.motor_speed_to_adjust = Motor.BUCKET.value
                print ('Motor speed adjustment mode:'), str(self.motor_speed_to_adjust)

            # Actuator logic
            elif key == QtCore.Qt.Key_U:
                #BUFFER.append('U\n')
                if key not in self.actuator_keys_pressed:
                    self.actuator_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'a': MOTOR_SPEEDS[Motor.ACTUATOR.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_J:
                #BUFFER.append('J\n')
                if key not in self.actuator_keys_pressed:
                    self.actuator_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'a': -1 * MOTOR_SPEEDS[Motor.ACTUATOR.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)

            # Bucket logic
            elif key == QtCore.Qt.Key_I:
                #BUFFER.append('I\n')
                if key not in self.bucket_keys_pressed:
                    self.bucket_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'b': MOTOR_SPEEDS[Motor.BUCKET.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_K:
                #BUFFER.append('K\n')
                if key not in self.bucket_keys_pressed:
                    self.bucket_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'b': -1 * MOTOR_SPEEDS[Motor.BUCKET.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)

        # Motor speed adjustment logic
        if key == QtCore.Qt.Key_Up:
            #BUFFER.append('Up\n')
            if MOTOR_SPEEDS[self.motor_speed_to_adjust] < MAX_MOTOR_SPEED:
                MOTOR_SPEEDS[self.motor_speed_to_adjust] += 1
                print (MOTOR_SPEEDS[self.motor_speed_to_adjust])
                if len(self.drive_keys_pressed):
                    self.keyPressEvent(Qt.QKeyEvent(Qt.QEvent.KeyPress, self.drive_keys_pressed[-1], 
                                                    QtCore.Qt.NoModifier))
        elif key == QtCore.Qt.Key_Down:
            #BUFFER.append('Down\n')
            if MOTOR_SPEEDS[self.motor_speed_to_adjust] > 0:
                MOTOR_SPEEDS[self.motor_speed_to_adjust] -= 1
                print (MOTOR_SPEEDS[self.motor_speed_to_adjust])
                if len(self.drive_keys_pressed):
                    self.keyPressEvent(Qt.QKeyEvent(Qt.QEvent.KeyPress, self.drive_keys_pressed[-1], 
                                                    QtCore.Qt.NoModifier))
    def keyReleaseEvent(self, event):
        if event.isAutoRepeat() or self.open_connection_button.isEnabled() \
                or self.deactivate_autonomy_button.isEnabled():
            return

        key = event.key()

        if key in self.drive_keys_pressed:
            self.drive_keys_pressed.remove(key)

        if key in self.actuator_keys_pressed:
            self.actuator_keys_pressed.remove(key)

        if key in self.bucket_keys_pressed:
            self.bucket_keys_pressed.remove(key)

        # Driving logic
        if not len(self.drive_keys_pressed):
            if key == QtCore.Qt.Key_W:
                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': 0, 'r': 0}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_S:
                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': 0, 'r': 0}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_A:
                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': 0, 'r': 0}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_D:
                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': 0, 'r': 0}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)

        # Actuator logic
        if not len(self.actuator_keys_pressed):
            if key == QtCore.Qt.Key_U:
                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'a': 0}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_J:
                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'a': 0}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)

        # Bucket logic
        if not len(self.bucket_keys_pressed):
            if key == QtCore.Qt.Key_I:
                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'b': 0}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_K:
                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'b': 0}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)


    def open_connection_event(self):
        self.client.open_connection()
        self.open_connection_button.setEnabled(False)
        self.close_connection_button.setEnabled(True)
        self.real_time_tracking_button.setEnabled(True)
        self.simulation_button.setEnabled(False)
        self.activate_autonomy_button.setEnabled(True)

    def close_connection_event(self):
        if self.deactivate_autonomy_button.isEnabled():
            autonomy_message = 'Please deactivate autonomy first.'
            QtWidgets.QMessageBox.question(self, 'Message',
                                           autonomy_message, QtWidgets.QMessageBox.Ok)
            return

        quit_message = 'Are you sure you want to close the connection?'
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               quit_message,
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.client.close_connection()

            self.open_connection_button.setEnabled(True)
            self.close_connection_button.setEnabled(False)

            self.activate_autonomy_button.setEnabled(False)
            self.deactivate_autonomy_button.setEnabled(False)


    def activate_autonomy_event(self):
        quit_message = 'Are you sure you want to activate autonomy?'
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               quit_message,
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.activate_autonomy()

    def activate_autonomy(self):
        self.client.send_message(ForwardingPrefix.CONTROLLER.value + AUTONOMY_ACTIVATION_MESSAGE)

        self.activate_autonomy_button.setEnabled(False)
        self.deactivate_autonomy_button.setEnabled(True)

    def deactivate_autonomy_event(self):
        deactivateMessage = 'Are you sure you want to deactivate autonomy?'
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               deactivateMessage,
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.deactivate_autonomy()

    def deactivate_autonomy(self):
        self.client.send_message(ForwardingPrefix.CONTROLLER.value + AUTONOMY_DEACTIVATION_MESSAGE)

        self.activate_autonomy_button.setEnabled(True)
        self.deactivate_autonomy_button.setEnabled(False)

    def simulation_event(self):
        sim = Setup()
        sim.start()

    def real_time_tracking_event(self):
        print()

    def closeEvent(self, QCloseEvent):
        quit_message = 'Are you sure you want to exit the client?'
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               quit_message,
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            if self.deactivate_autonomy_button.isEnabled():
                self.deactivate_autonomy()
            self.client.shutdown()
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


def main(client):
    app = QApplication(sys.argv)
    window = Window(client)
    # log = open('key_press_log.txt', 'w')
    # log.write('Key Press Log: \n')
    # for i in BUFFER:
    #     log.write(i)
    # log.close()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
