from PyQt5 import QtCore, QtGui, QtWidgets
import sys, res

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(586, 601)
        MainWindow.setStyleSheet("*{\n"
"    font-family: century gothic;\n"
"    font-size:24px\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(50, 20, 441, 541))
        self.frame.setStyleSheet("QFrame{\n"
"background-image: url(:/images/photo-1570735821643-6d4126137675.jpg);\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(190, 20, 81, 71))
        self.label.setStyleSheet("*{\n"
"    color:rgb(255, 255, 255);\n"
"    font-size: 24pt; \n"
"    font-family: century gothic;\n"
"\n"
"}")
        self.label.setObjectName("label")
        self.password = QtWidgets.QLineEdit(self.frame)
        self.password.setGeometry(QtCore.QRect(60, 160, 351, 41))
        self.password.setStyleSheet("QLineEdit\n"
"{\n"
"background:transparent;\n"
"border:none;\n"
"color:#717072\n"
"}")
        self.password.setObjectName("password")
        self.email = QtWidgets.QLineEdit(self.frame)
        self.email.setGeometry(QtCore.QRect(60, 290, 361, 41))
        self.email.setStyleSheet("QLineEdit\n"
"{\n"
"background:transparent;\n"
"border:none;\n"
"color:#717072\n"
"}")
        self.email.setObjectName("email")
        self.invalid = QtWidgets.QLabel(self.frame)
        self.invalid.setGeometry(QtCore.QRect(230, 330, 161, 41))
        self.invalid.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font-size: 14px;\n"
"}")
        self.invalid.setObjectName("invalid")
        self.enterButton = QtWidgets.QPushButton(self.frame)
        self.enterButton.setGeometry(QtCore.QRect(180, 420, 81, 31))
        self.enterButton.setStyleSheet("QPushButton{\n"
"    background: white;\n"
"    border-radius: 60px;\n"
"    font-family: century gothic;\n"
"}")
        self.enterButton.setObjectName("enterButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Login"))
        self.password.setText(_translate("MainWindow", "Email"))
        self.email.setText(_translate("MainWindow", "Password "))
        self.invalid.setText(_translate("MainWindow", "Invalid email or password"))
        self.enterButton.setText(_translate("MainWindow", "Enter"))

