# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/MainForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(533, 292)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 511, 231))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.headsculLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.headsculLabel.setEnabled(True)
        self.headsculLabel.setSizeIncrement(QtCore.QSize(0, 0))
        self.headsculLabel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.headsculLabel.setObjectName("headsculLabel")
        self.horizontalLayout.addWidget(self.headsculLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.accountEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.accountEdit.setText("")
        self.accountEdit.setObjectName("accountEdit")
        self.horizontalLayout_2.addWidget(self.accountEdit)
        self.registButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.registButton.setObjectName("registButton")
        self.horizontalLayout_2.addWidget(self.registButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.passwordEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwordEdit.sizePolicy().hasHeightForWidth())
        self.passwordEdit.setSizePolicy(sizePolicy)
        self.passwordEdit.setText("")
        self.passwordEdit.setObjectName("passwordEdit")
        self.horizontalLayout_5.addWidget(self.passwordEdit)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.savePasswordBox = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.savePasswordBox.setObjectName("savePasswordBox")
        self.horizontalLayout_3.addWidget(self.savePasswordBox)
        self.autoLoginBox = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.autoLoginBox.setObjectName("autoLoginBox")
        self.horizontalLayout_3.addWidget(self.autoLoginBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.loginButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy)
        self.loginButton.setObjectName("loginButton")
        self.verticalLayout_2.addWidget(self.loginButton)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 533, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.headsculLabel.setText(_translate("MainWindow", "image"))
        self.registButton.setText(_translate("MainWindow", "注册账号"))
        self.label_3.setText(_translate("MainWindow", "找回密码"))
        self.savePasswordBox.setText(_translate("MainWindow", "记住密码"))
        self.autoLoginBox.setText(_translate("MainWindow", "自动登录"))
        self.loginButton.setText(_translate("MainWindow", "登录"))
