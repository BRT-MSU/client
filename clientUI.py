# -*- coding: utf-8 -*-

import sys
from message import *
import enum

import sip

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
 
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
MOTOR_SPEEDS = {0: 25, 1: 100, 2: 40}

MAX_MOTOR_SPEED = 100
MAX_SERVO_ANGLE = 180


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

        # Text box to display telemetry data
        telemetry_box = QtWidgets.QHBoxLayout()
        network_box = QtWidgets.QHBoxLayout()
        controller_status_box = QtWidgets.QVBoxLayout()
        speed_box = QtWidgets.QVBoxLayout()
        power_box = QtWidgets.QVBoxLayout()
        connection_box = QtWidgets.QVBoxLayout()

        self.roboclaw_status_label = QLabel()
        self.roboclaw_status_label.setAlignment(Qt.Qt.AlignLeft)
        self.roboclaw_status_label.setText("Roboclaw: disconnected")
        controller_status_box .addWidget(self.roboclaw_status_label)

        self.left_motor_status_label = QLabel()
        self.left_motor_status_label.setAlignment(Qt.Qt.AlignLeft)
        self.left_motor_status_label.setText("Left motor: disconnected")
        controller_status_box .addWidget(self.left_motor_status_label)

        self.right_motor_status_label = QLabel()
        self.right_motor_status_label.setAlignment(Qt.Qt.AlignLeft)
        self.right_motor_status_label.setText("Right motor: disconnected")
        controller_status_box .addWidget(self.right_motor_status_label)

        self.left_motor_speed = QLabel()
        self.left_motor_speed.setAlignment(Qt.Qt.AlignCenter)
        self.left_motor_speed.setText("Left motor rpm: " + "0")
        speed_box.addWidget(self.left_motor_speed)

        self.right_motor_speed = QLabel()
        self.right_motor_speed.setAlignment(Qt.Qt.AlignCenter)
        self.right_motor_speed.setText("Right motor rpm: " + "0")
        speed_box.addWidget(self.right_motor_speed)

        self.actuator_length_label = QLabel()
        self.actuator_length_label.setAlignment(Qt.Qt.AlignCenter)
        self.actuator_length_label.setText("Actuator length: " + "0" + "\"")
        speed_box.addWidget(self.actuator_length_label)

        self.bucket_angle_label = QLabel()
        self.bucket_angle_label.setAlignment(Qt.Qt.AlignCenter)
        self.bucket_angle_label.setText("Bucket Angle: " + "0" + "°")
        speed_box.addWidget(self.bucket_angle_label)

        self.actuator_current_label = QLabel()
        self.actuator_current_label.setAlignment(Qt.Qt.AlignCenter)
        self.actuator_current_label.setText("Actuator current: " + "0" + "A")
        power_box.addWidget(self.actuator_current_label)

        self.bucket_current_label = QLabel()
        self.bucket_current_label.setAlignment(Qt.Qt.AlignCenter)
        self.bucket_current_label.setText("Bucket current: " + "0" + "A")
        power_box.addWidget(self.bucket_current_label)

        self.battery_voltage_label = QLabel()
        self.battery_voltage_label.setAlignment(Qt.Qt.AlignCenter)
        self.battery_voltage_label.setText("Battery Voltage: " + "0" + "V")
        power_box.addWidget(self.battery_voltage_label)

        telemetry_box.addLayout(controller_status_box)
        telemetry_box.addLayout(speed_box)
        telemetry_box.addLayout(power_box)

        self.client_ip_address_label = QLabel()
        self.client_ip_address_label.setAlignment(Qt.Qt.AlignLeft)
        self.client_ip_address_label.setText("Client IP: " + str(self.client.client_ip_address))
        connection_box.addWidget(self.client_ip_address_label)

        self.client_port_label = QLabel()
        self.client_port_label.setAlignment(Qt.Qt.AlignLeft)
        self.client_port_label.setText("Client Port: " + str(self.client.client_port_number))
        connection_box.addWidget(self.client_port_label)

        self.controller_ip_address_label = QLabel()
        self.controller_ip_address_label.setAlignment(Qt.Qt.AlignLeft)
        self.controller_ip_address_label.setText("Controller address: " + str(self.client.controller_ip_address))
        connection_box.addWidget(self.controller_ip_address_label)

        self. controller_port_label = QLabel()
        self.controller_port_label.setAlignment(Qt.Qt.AlignLeft)
        self.controller_port_label.setText("Controller port: " + str(self.client.controller_port_number))
        connection_box.addWidget(self.controller_port_label)

        network_box.addLayout(connection_box)

        grid = QtWidgets.QGridLayout()
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

        #v_box.addLayout(telemetry_box)
        v_box.addStretch(1)
        v_box.addLayout(network_box)
        v_box.addStretch(10)
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

    def update_telemetry(self, message):
        self.battery_voltage_label.setText("Battery Voltage: " + "10" + "V")
        print "1!11"
        if message is not None:
            print message

        #  TODO: Finish this logic to parse and update incoming data.

    def keyPressEvent(self, event):
        if self.open_connection_button.isEnabled() \
                or self.deactivate_autonomy_button.isEnabled():
            return

        key = event.key()

        if not event.isAutoRepeat():
            # Driving logic
            if key == QtCore.Qt.Key_W:
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value],
                                'r': MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_S:
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': -1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value],
                                'r': -1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_A:
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': -1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value],
                                'r': 1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_D:
                if key not in self.drive_keys_pressed:
                    self.drive_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'l': 1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value],
                                'r': -1 * MOTOR_SPEEDS[Motor.DRIVE_MOTORS.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)

            # Motor speed adjustment mode logic
            elif key == QtCore.Qt.Key_1:
                self.motor_speed_to_adjust = Motor.DRIVE_MOTORS.value
                print 'Motor speed adjustment mode:', str(self.motor_speed_to_adjust)
            elif key == QtCore.Qt.Key_2:
                self.motor_speed_to_adjust = Motor.ACTUATOR.value
                print 'Motor speed adjustment mode:', str(self.motor_speed_to_adjust)
            elif key == QtCore.Qt.Key_3:
                self.motor_speed_to_adjust = Motor.BUCKET.value
                print 'Motor speed adjustment mode:', str(self.motor_speed_to_adjust)

            # Actuator logic
            elif key == QtCore.Qt.Key_U:
                if key not in self.actuator_keys_pressed:
                    self.actuator_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'a': MOTOR_SPEEDS[Motor.ACTUATOR.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_J:
                if key not in self.actuator_keys_pressed:
                    self.actuator_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'a': -1 * MOTOR_SPEEDS[Motor.ACTUATOR.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)

            # Bucket logic
            elif key == QtCore.Qt.Key_I:
                if key not in self.bucket_keys_pressed:
                    self.bucket_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'b': MOTOR_SPEEDS[Motor.BUCKET.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)
            elif key == QtCore.Qt.Key_K:
                if key not in self.bucket_keys_pressed:
                    self.bucket_keys_pressed.append(key)

                forwarding_prefix = ForwardingPrefix.MOTOR.value
                sub_messages = {'b': -1 * MOTOR_SPEEDS[Motor.BUCKET.value]}
                message = Message(forwarding_prefix, sub_messages).message
                self.client.send_message(message)

        # Motor speed adjustment logic
        if key == QtCore.Qt.Key_Up:
            if MOTOR_SPEEDS[self.motor_speed_to_adjust] < MAX_MOTOR_SPEED:
                MOTOR_SPEEDS[self.motor_speed_to_adjust] += 1
                print MOTOR_SPEEDS[self.motor_speed_to_adjust]
                if len(self.drive_keys_pressed):
                    self.keyPressEvent(Qt.QKeyEvent(Qt.QEvent.KeyPress, self.drive_keys_pressed[-1], 
                                                    QtCore.Qt.NoModifier))
        elif key == QtCore.Qt.Key_Down:
            if MOTOR_SPEEDS[self.motor_speed_to_adjust] > 0:
                MOTOR_SPEEDS[self.motor_speed_to_adjust] -= 1
                print MOTOR_SPEEDS[self.motor_speed_to_adjust]
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
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
