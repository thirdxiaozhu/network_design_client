from datetime import datetime
from PIL import Image
from numpy import broadcast
import Register
import List
import ChatWindow
import os
import threading
import Dialogs
import SubUnit
import EmojiTable
import base64
import PersonalInfo
from Protocol import *
from PyQt5.QtWidgets import *
from Client import Client
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets


#登录窗口
class LoginEvent(QtCore.QObject):
    #全局变量信号，变量为字典类型
    startUpFriendList = QtCore.pyqtSignal(dict)

    def __init__(self, mainWindow, ui):
        super(LoginEvent, self).__init__()
        self.client = Client()
        self.mainWindow = mainWindow
        self.ui = ui
        self.initComponent()
        self.reinitUi()
        self.initEvent()

    # 点击登录按钮后，创建新线程：用非阻塞方式获取socket输入输出

    def Login(self):
        self.account = self.accountLine.text()
        self.password = self.passwordLine.text()

        dataDic = dict(msgType=Protocol.Login,
                       account=self.account, password=self.password)

        self.client.setupConnection(dataDic, self)

    #如果代码为1000，表示登录成功，显示好友列表widget

    def showupFriendList(self, msg):
        if msg.get("code") == 1000:
            self.mainWindow.hide()

            #如果登陆成功，启动epoll处理信息
            t = threading.Thread(target=self.client.initiateServer)
            t.start()
            self.client.registFileNo()
            #开启文件传输socket
            self.client.filetrans.start()

            widget = QDialog()
            listUi = List.Ui_Form()
            listUi.setupUi(widget)
            FriendsList(widget, msg, self.client)
            widget.show()
            widget.exec_()
            #self.mainWindow.show()  # 如果没有self.form.show()这一句，关闭Demo1界面后就会关闭程序
            self.setLogout()  # 退出登录
        else:
            QMessageBox.warning(self.mainWindow, "警告",
                                "用户名或密码错误", QMessageBox.Yes | QMessageBox.No)

    #注册

    def Regist(self):
        self.mainWindow.hide()
        form = QDialog()
        ui = Register.Ui_Form()
        ui.setupUi(form)
        RegisterEvent(self.mainWindow, form)
        form.show()
        form.exec_()
        self.mainWindow.show()

    def setLogout(self):
        dataDic = dict(msgType=Protocol.LOGOUT,
                       account=self.account)
        self.client.setLogout(dataDic)

    def initComponent(self):
        self.loginButton = self.mainWindow.findChild(
            QPushButton, "loginButton")
        self.accountLine = self.mainWindow.findChild(QLineEdit, "accountEdit")
        self.passwordLine = self.mainWindow.findChild(
            QLineEdit, "passwordEdit")
        self.registButton = self.mainWindow.findChild(
            QPushButton, "registButton")

    def reinitUi(self):
        self.ui.label.setFixedSize(150, 150)  # 设置头像区域大小为150x150

    def initEvent(self):
        self.startUpFriendList.connect(self.showupFriendList)
        self.loginButton.clicked.connect(lambda: self.Login())
        self.registButton.clicked.connect(lambda: self.Regist())


#注册窗口
class RegisterEvent:
    def __init__(self, father, ui) -> None:
        self.father = father
        self.ui = ui
        self.id = self.ui.findChild(QLineEdit, "idEdit")
        self.password = self.ui.findChild(QLineEdit, "passwordEdit")
        self.confirm = self.ui.findChild(QLineEdit, "confirmEdit")
        self.nickname = self.ui.findChild(QLineEdit, "nicknameEdit")
        self.acceptButton = self.ui.findChild(QPushButton, "acceptButton")
        self.cancleButton = self.ui.findChild(QPushButton, "cancleButton")
        self.initEvent()

    def initEvent(self):
        self.acceptButton.clicked.connect(self.submitRegist)
        self.cancleButton.clicked.connect(lambda: self.cancleRegist())

    def submitRegist(self):
        if self.confirm.text() == self.password.text():
            dataDic = dict(msgType=Protocol.Regist, id=self.id.text(
            ), password=self.password.text(), nickname=self.nickname.text())
            client = Client()
            res = client.registConnection(dataDic)
            if res == 1000:
                QMessageBox.information(self.ui, "成功", "添加成功", QMessageBox.Yes)
                self.cancleRegist()
            else:
                QMessageBox.warning(self.ui, "警告", "账号已被注册", QMessageBox.Yes)
        else:
            QMessageBox.warning(self.ui, "警告", "密码不一致", QMessageBox.Yes)

    def cancleRegist(self):
        self.ui.exec_()
        self.ui.close()
        self.father.show()


class FriendsList(QObject):
    startUpFriendNodes = QtCore.pyqtSignal(dict)
    broadcastLoginSignal = QtCore.pyqtSignal(dict)

    def __init__(self, form, msg, client):
        super(FriendsList, self).__init__()
        self.ownerInfo = msg
        self.client = client
        self.form = form
        self.friendsNodes = []
        self.initComponent()
        self.initEvent()
        self.getFriendNodes()

    #双击node打开对应聊天窗口

    def doubleClicked(self):
        item = self.listWidget.selectedItems()[0]
        widget = self.listWidget.itemWidget(item)
        #从好友列表node中截取账号，有待修改
        targetAccount = widget.findChild(QLabel, "accountLabel").text()[2:-2]
        widget = Dialogs.ChatDialog()
        chatWindow = ChatWindow.Ui_Form()
        chatWindow.setupUi(widget)
        Chat(widget, self.ownerInfo.get("account"), targetAccount, self.client)
        widget.show()
        widget.exec_()

    #填充好友列表
    def getFriendNodes(self):
        dataDic = dict(msgType=Protocol.searchFriend,
                       account=self.ownerInfo.get("account"))
        self.client.searchFriend(dataDic, self)

    def searchFriendCallBack(self, all_data):
        if self.listWidget.count() > 0:
            for i in range(self.listWidget.count()-1, -1, -1):
                self.listWidget.removeItemWidget(self.listWidget.takeItem(i))

        for friend in all_data.get("friends"):
            item = SubUnit.FriendListItem(friend)  # 创建QListWidgetItem对象
            item.setSizeHint(QSize(200, 50))  # 设置QListWidgetItem大小
            widget = item.getItemWidget()  # 调用上面的函数获取对应
            self.listWidget.addItem(item)  # 添加item
            self.listWidget.setItemWidget(item, widget)  # 为item设置widget
            self.friendsNodes.append(item)


    def broadcastLoginCallBack(self, dict):
        for item in self.friendsNodes:
            if item.friend_account == dict.get("account"):
                item.changeLoginState(dict.get("flag"))

    def addFriend(self):
        text, ok = QInputDialog().getText(QWidget(), '添加好友', '输入好友账号:')
        if text and ok:
            dataDic = dict(msgType=Protocol.addFriend,
                           account=self.ownerInfo.get("account"), target=text)
            code = self.client.addFriend(dataDic)
            print(code)
            if code == 1000:
                self.deal()
                QMessageBox.information(None, "成功", "添加成功", QMessageBox.Yes)
            elif code == 1001:
                QMessageBox.warning(None, "警告", "用户不存在", QMessageBox.Yes)
            elif code == 1002:
                QMessageBox.warning(None, "警告", "你们已经成为好友", QMessageBox.Yes)

    def showInfoWidget(self):
        form = QDialog()
        ui = PersonalInfo.Ui_Form()
        ui.setupUi(form)
        PersonalInfoEvent(form, self.client, self.ownerInfo)
        form.show()
        form.exec_()

    def initComponent(self):
        self.listWidget = self.form.findChild(QListWidget, "FriendsList")
        self.infoButton = self.form.findChild(QPushButton, "infoButton")
        self.addFriendButton = self.form.findChild(QPushButton, "addFriendBtn")
        self.nicknameLabel = self.form.findChild(QLabel, "nicknameLabel")
        self.signatureLabel = self.form.findChild(QLabel, "signatureLabel")
        self.nicknameLabel.setText(self.ownerInfo.get("nickname"))
        self.signatureLabel.setText(self.ownerInfo.get("signature"))

    def initEvent(self):
        self.infoButton.clicked.connect(lambda: self.showInfoWidget())
        self.addFriendButton.clicked.connect(lambda: self.addFriend())
        self.listWidget.itemDoubleClicked.connect(lambda: self.doubleClicked())
        self.startUpFriendNodes.connect(self.searchFriendCallBack)
        self.broadcastLoginSignal.connect(self.broadcastLoginCallBack)


#聊天窗口


class Chat(QObject):
    #获取消息信号，绑定消息展示槽
    getMessage = QtCore.pyqtSignal(dict)

    def __init__(self, widget, ownerAccount, targetAccount, client) -> None:
        super(Chat, self).__init__()
        self.widget = widget
        self.ownerAccount = ownerAccount
        self.targetAccount = targetAccount
        self.client = client
        self.initComponent()
        self.initEvent()
        self.initMessageRecord()

    def initMessageRecord(self):
        dataDic = dict(msgType=Protocol.getMessageRecord,
                       account=self.ownerAccount, target=self.targetAccount)
        self.client.getMessageRecord(dataDic, self)

    def initComponent(self):
        self.messageReceiver = self.widget.findChild(
            QListWidget, "messageList")
        self.messageEditer = self.widget.findChild(QTextEdit, "messageEditer")
        self.sendButton = self.widget.findChild(QPushButton, "sendButton")
        self.closeButton = self.widget.findChild(QPushButton, "closeButton")
        self.emojiWidget = self.widget.findChild(QPushButton, "emojiWidget")
        self.pictureButton = self.widget.findChild(
            QPushButton, "pictureButton")

        self.widget.targetAccount = self.targetAccount
        self.widget.client = self.client

    def initEvent(self):
        self.getMessage.connect(self.messageCallBack)
        self.sendButton.clicked.connect(lambda: self.sendMessage())
        self.emojiWidget.clicked.connect(lambda: self.setupEmojiWidget())
        self.pictureButton.clicked.connect(lambda: self.chooseImg())

    #发送消息
    def sendMessage(self):
        dataDic = dict(msgType=Protocol.sendMessage,
                       account=self.ownerAccount, target=self.targetAccount, message=self.messageEditer.toPlainText(), form=MessageFormat.NORMAL)

        print(dataDic)
        self.client.sendMessage(dataDic)
        self.messageEditer.clear()

    def messageCallBack(self, dict):
        for msg in dict.get("messages"):
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            html = '<div align=%s> <font color=%s>%s   </font><font color=%s>( %s )<br></font> <font color=\"#000000\">%s</font></div>'
            if msg.get("sender") == self.ownerAccount:
                color = "#00CC00"
                align = "right"
                node = SubUnit.NodeItem("own")  # 调用上面的函数获取对应
            else:
                color = "#0000FF"
                align = "left"
                node = SubUnit.NodeItem("opposite")  # 调用上面的函数获取对应

            message = (html % (align, color, msg.get("sender"),
                       color, msg.get("time"), msg.get("message")))
            node.setMessage(message)
            widget = node.horizontalLayoutWidget

            itemheight = widget.findChild(
                QTextEdit, "messageText").document().size().height() * 2 + 10
            #item.setSizeHint(QSize(self.messageReceiver.width(), itemheight))  # 设置QListWidgetItem大小
            item.setSizeHint(QSize(500, itemheight))  # 设置QListWidgetItem大小

            self.messageReceiver.addItem(item)  # 添加item
            self.messageReceiver.setItemWidget(item, widget)  # 为item设置widget

    def setupEmojiWidget(self):
        print(self.emojiWidget.text())
        emojiWidget = QDialog()
        chatWindow = EmojiTable.Ui_Form()
        chatWindow.setupUi(emojiWidget)
        SubUnit.EmojiTab(emojiWidget, self)
        emojiWidget.show()
        emojiWidget.exec_()

    def chooseImg(self):
        imgNames, imgType = QFileDialog.getOpenFileNames(
            None, "打开图片", "/home/jiaxv/Pictures", "*.jpg;;*.png;;*.jpeg;;All Files(*)")


class PersonalInfoEvent:
    def __init__(self, form, client, ownerInfo) -> None:
        self.form = form
        self.client = client
        self.ownerInfo = ownerInfo
        self.initComponent()
        self.initEvent()
        self.initInfos()

    def initComponent(self):
        self.accountLabel = self.form.findChild(QLabel, "accountLabel")
        self.passwordEdit = self.form.findChild(QLineEdit, "passwordEdit")
        self.nicknameEdit = self.form.findChild(QLineEdit, "nicknameEdit")
        self.signatureEdit = self.form.findChild(QLineEdit, "signatureEdit")
        self.pictureButton = self.form.findChild(QPushButton, "pictureButton")
        self.confirmButton = self.form.findChild(QPushButton, "confirmButton")
        self.cancelButton = self.form.findChild(QPushButton, "cancelButton")

    def initEvent(self):
        self.pictureButton.clicked.connect(lambda: self.uploadHead())

    def initInfos(self):
        self.accountLabel.setText(self.ownerInfo.get("account"))
        self.passwordEdit.setText(self.ownerInfo.get("password"))
        self.nicknameEdit.setText(self.ownerInfo.get("nickname"))
        self.signatureEdit.setText(self.ownerInfo.get("signature"))

    def uploadHead(self):
        imgName, imgType = QFileDialog.getOpenFileName(None, "打开图片", "/home/jiaxv/Pictures", "*.jpg;;*.png;;*.jpeg;;All Files(*)")
        self.client.filetrans.putFilePath(imgName)
