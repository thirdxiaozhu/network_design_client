# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/untitled.ui'
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
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 60, 501, 105))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.friendphoto = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.friendphoto.setObjectName("friendphoto")
        self.horizontalLayout.addWidget(self.friendphoto)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.messageText = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.messageText.setEnabled(True)
        self.messageText.setMinimumSize(QtCore.QSize(50, 0))
        self.messageText.setMaximumSize(QtCore.QSize(300, 16777215))
        self.messageText.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.messageText.setAutoFillBackground(False)
        self.messageText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.messageText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.messageText.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.messageText.setLineWrapColumnOrWidth(0)
        self.messageText.setObjectName("messageText")
        self.verticalLayout.addWidget(self.messageText)
        self.fileProcessBar = QtWidgets.QProgressBar(self.horizontalLayoutWidget)
        self.fileProcessBar.setProperty("value", 24)
        self.fileProcessBar.setObjectName("fileProcessBar")
        self.verticalLayout.addWidget(self.fileProcessBar)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.friendphoto.setText(_translate("Form", "TextLabel"))
        self.messageText.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">casd</p></body></html>"))