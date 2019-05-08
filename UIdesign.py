
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(526, 373)

        self.setWindowTitle('Client')
        self.setWindowIcon(QtGui.QIcon('mars.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.toolbar = self.addToolBar("tool bar")
        self.connection_button = QAction("open connection", self)
        self.toolbar.addAction(self.connection_button)
        self.autonomy_button = QAction("activate autonomy", self)
        self.toolbar.addAction(self.autonomy_button)
        self.controller_button = QAction("enable controller", self)
        self.toolbar.addAction(self.controller_button)

        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        plot = PlotUI(MainWindow)
        self.verticalLayout.addWidget(plot)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.create_motor_enable())
        self.verticalLayout.addWidget(self.create_target_motor_speeds())
        self.verticalLayout.addWidget(self.create_connection_info())

        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_connection_info(self):
        group = QGroupBox("connection info")
        hbox = QHBoxLayout()

        client_address = QLabel("client ip: " + self.client.client_ip_address)
        client_port = QLabel("client port: " + str(self.client.client_port_number))
        controller_addres = QLabel("controller ip: " + self.client.controller_ip_address)

        controller_port = QLabel("client port: " + str(self.client.controller_port_number))

        hbox.addWidget(client_address)
        hbox.addWidget(client_port)
        hbox.addWidget(controller_addres)
        hbox.addWidget(controller_port)

        group.setLayout(hbox)
        return group

    def create_target_motor_speeds(self):
        group = QGroupBox("target motor speeds")
        hbox = QHBoxLayout()

        self.left_motor_target_speed = QLabel("left motor: " + str(self.client.get_drive_speed()))
        self.right_motor_target_speed = QLabel("right motor: " + str(self.client.get_drive_speed()))
        self.actuator_target_speed = QLabel("actuator: " + str(self.client.get_actuator_speed()))
        self.bucket_target_speed = QLabel("bucket: " + str(self.client.get_bucket_speed()))

        hbox.addWidget(self.left_motor_target_speed)
        hbox.addWidget(self.right_motor_target_speed)
        hbox.addWidget(self.actuator_target_speed)
        hbox.addWidget(self.bucket_target_speed)

        group.setLayout(hbox)
        return group

    def create_motor_enable(self):
        group = QGroupBox("Driving Speed                            Digging Wheel Speed                         Actuator Speed")
        group.setCheckable(True)
        group.setChecked(False)
        hbox1 = QHBoxLayout()
        hbox = QHBoxLayout()

        self.left_motor_enable_checkbox = QCheckBox("left motor")
        self.left_motor_enable_checkbox.setChecked(True)
        self.right_motor_enable_checkbox = QCheckBox("right motor")
        self.right_motor_enable_checkbox.setChecked(True)
        self.actuator_enable_checkbox = QCheckBox("actuators")
        self.actuator_enable_checkbox.setChecked(True)
        self.bucket_enable_checkbox = QCheckBox("bucket")
        self.bucket_enable_checkbox.setChecked(True)
        self.bucket_enable_checkbox.setTristate(False)

        # Driving speed
        self.l1 = QLabel()
        self.l1.setText("Driving Speed")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)

        # Digging Wheel speed
        self.l2 = QLabel()
        self.l2.setText("Digging Wheel Speed")
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.setFocusPolicy(Qt.StrongFocus)
        self.slider1.setTickPosition(QSlider.TicksBothSides)
        self.slider1.setTickInterval(10)
        self.slider1.setSingleStep(1)

        # Actuator speed
        self.l3 = QLabel()
        self.l3.setText("Actuator Speed")
        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.setFocusPolicy(Qt.StrongFocus)
        self.slider2.setTickPosition(QSlider.TicksBothSides)
        self.slider2.setTickInterval(10)
        self.slider2.setSingleStep(1)

        hbox.addWidget(self.slider)
        hbox.addWidget(self.slider1)
        hbox.addWidget(self.slider2)

        hbox1.addWidget(self.l1)
        hbox1.addWidget(self.l2)
        hbox1.addWidget(self.l3)
        # hbox.addWidget(self.left_motor_enable_checkbox)
        # hbox.addWidget(self.right_motor_enable_checkbox)
        # hbox.addWidget(self.actuator_enable_checkbox)
        # hbox.addWidget(self.bucket_enable_checkbox)

        group.setLayout(hbox)

        return group

class PlotUI(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        #self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.plot()

    def plot(self):
        #ax = self.figure.add_subplot(111)
        self.axes.set_title('Position')
        self.draw()




