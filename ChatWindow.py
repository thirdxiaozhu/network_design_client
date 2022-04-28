# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/chatWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(653, 460)
        Form.setMinimumSize(QtCore.QSize(653, 460))
        Form.setMaximumSize(QtCore.QSize(653, 460))
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 631, 442))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.messageList = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.messageList.setMinimumSize(QtCore.QSize(629, 292))
        self.messageList.setMaximumSize(QtCore.QSize(629, 292))
        self.messageList.setObjectName("messageList")
        self.verticalLayout.addWidget(self.messageList)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.emojiWidget = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.emojiWidget.setMinimumSize(QtCore.QSize(50, 0))
        self.emojiWidget.setMaximumSize(QtCore.QSize(50, 16777215))
        self.emojiWidget.setObjectName("emojiWidget")
        self.horizontalLayout_2.addWidget(self.emojiWidget)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pictureButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pictureButton.setMinimumSize(QtCore.QSize(50, 0))
        self.pictureButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pictureButton.setObjectName("pictureButton")
        self.horizontalLayout_2.addWidget(self.pictureButton)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.fileButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.fileButton.setMinimumSize(QtCore.QSize(50, 0))
        self.fileButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.fileButton.setObjectName("fileButton")
        self.horizontalLayout_2.addWidget(self.fileButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.messageEditer = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageEditer.sizePolicy().hasHeightForWidth())
        self.messageEditer.setSizePolicy(sizePolicy)
        self.messageEditer.setMinimumSize(QtCore.QSize(0, 0))
        self.messageEditer.setMaximumSize(QtCore.QSize(16777215, 70))
        self.messageEditer.setLineWidth(1)
        self.messageEditer.setObjectName("messageEditer")
        self.verticalLayout.addWidget(self.messageEditer)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.sendButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.sendButton.setMinimumSize(QtCore.QSize(100, 0))
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout.addWidget(self.sendButton)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.closeButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.closeButton.setMinimumSize(QtCore.QSize(100, 0))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.emojiWidget.setText(_translate("Form", "😍"))
        self.pictureButton.setText(_translate("Form", "img"))
        self.fileButton.setText(_translate("Form", "文件"))
        self.sendButton.setText(_translate("Form", "发送"))
        self.closeButton.setText(_translate("Form", "关闭"))
