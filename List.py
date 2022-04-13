# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(292, 702)
        Form.setMinimumSize(QtCore.QSize(260, 700))
        Form.setMaximumSize(QtCore.QSize(100000, 100000))
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 681))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.nicknameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.nicknameLabel.setObjectName("nicknameLabel")
        self.verticalLayout_2.addWidget(self.nicknameLabel)
        self.signatureLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.signatureLabel.setObjectName("signatureLabel")
        self.verticalLayout_2.addWidget(self.signatureLabel)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.infoButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoButton.sizePolicy().hasHeightForWidth())
        self.infoButton.setSizePolicy(sizePolicy)
        self.infoButton.setMinimumSize(QtCore.QSize(0, 0))
        self.infoButton.setFocusPolicy(QtCore.Qt.TabFocus)
        self.infoButton.setObjectName("infoButton")
        self.horizontalLayout.addWidget(self.infoButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget.setStyleSheet("QTabBar::tab{width:134.4}\n"
"QTabBar::tab{height:25}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.friends = QtWidgets.QWidget()
        self.friends.setObjectName("friends")
        self.FriendsList = QtWidgets.QListWidget(self.friends)
        self.FriendsList.setGeometry(QtCore.QRect(0, 0, 269, 571))
        self.FriendsList.setObjectName("FriendsList")
        self.tabWidget.addTab(self.friends, "")
        self.group = QtWidgets.QWidget()
        self.group.setObjectName("group")
        self.GroupList = QtWidgets.QListWidget(self.group)
        self.GroupList.setGeometry(QtCore.QRect(0, 0, 270, 571))
        self.GroupList.setObjectName("GroupList")
        self.tabWidget.addTab(self.group, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.addFriendBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addFriendBtn.setObjectName("addFriendBtn")
        self.verticalLayout.addWidget(self.addFriendBtn)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "TextLabel"))
        self.nicknameLabel.setText(_translate("Form", "TextLabel"))
        self.signatureLabel.setText(_translate("Form", "TextLabel"))
        self.infoButton.setText(_translate("Form", "个人资料"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.friends), _translate("Form", "好友"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.group), _translate("Form", "群聊"))
        self.addFriendBtn.setText(_translate("Form", "添加好友"))
