# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(560, 272)
        horizontalLayoutWidget = QtWidgets.QWidget()
        horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 60, 501, 61))
        horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setObjectName("horizontalLayout")
        friendphoto = QtWidgets.QLabel(self.horizontalLayoutWidget)
        friendphoto.setObjectName("friendphoto")
        horizontalLayout.addWidget(self.friendphoto)
        messageText = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        messageText.setMinimumSize(QtCore.QSize(50, 0))
        messageText.setMaximumSize(QtCore.QSize(300, 16777215))
        messageText.setLayoutDirection(QtCore.Qt.LeftToRight)
        messageText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        messageText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        messageText.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        messageText.setObjectName("messageText")
        horizontalLayout.addWidget(self.messageText)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem)
        return horizontalLayoutWidget

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.friendphoto.setText(_translate("Form", "TextLabel"))
