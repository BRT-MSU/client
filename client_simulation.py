import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class Setup(object):
    def __init__(self, width=800, height=600, spacing=50):
        self.width = width
        self.height = height
        self.spacing = spacing

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.width, self.height)
        MainWindow.setWindowIcon(QtGui.QIcon('robotic_arm.png'))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(710, 230, 82, 17))
        self.radioButton.setObjectName("radioButton")

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(710, 260, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(704, 300, 71, 41))
        self.pushButton.setObjectName("pushButton")

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simulation"))
        self.radioButton.setText(_translate("MainWindow", "Obstacle"))
        self.radioButton_2.setText(_translate("MainWindow", "Start/End"))
        self.pushButton.setText(_translate("MainWindow", "Start"))

    def gridSetup(self):
        n = 1

    def start(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Setup()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())