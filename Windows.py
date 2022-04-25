import time
import Register
import List
import ChatWindow
import GroupChatWindow
import os
import threading
import Dialogs
import SubUnit
import EmojiTable
import PersonalInfo
import SetGroup
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
        #读取配置文件
        self.readLocalProfile()

    # 点击登录按钮后，创建新线程：用非阻塞方式获取socket输入输出

    def Login(self):
        self.account = self.accountLine.text()
        self.password = self.passwordLine.text()

        dataDic = dict(msgType=Protocol.Login,
                       account=self.account, password=self.password)

        self.client.setupConnection(dataDic, self)

    #记录最近一次账号密码和勾选状态
    def setLocalProfile(self, headscul):
        data = dict(account=self.account, password=self.password, isSavePassword=self.savePasswordBox.isChecked(),
                    isAutoLogin=self.autoLoginBox.isChecked(), headscul=headscul)
        with open('profile/profile.sav', 'w', encoding='utf-8') as f:
            f.write(json.dumps(data))
        f.close()

    def readLocalProfile(self):
        with open('profile/profile.sav', 'r', encoding='utf-8') as f:
            dict = f.readline()
        infos = json.loads(dict)
        self.accountLine.setText(infos.get("account"))
        if infos.get("isSavePassword"):
            self.passwordLine.setText(infos.get("password"))
            self.savePasswordBox.setChecked(True)
        if infos.get("isAutoLogin"):
            self.autoLoginBox.setChecked(True)
            self.Login()

        if infos.get("headscul") is not None and os.path.exists(infos.get("headscul")):
            jpg = QtGui.QPixmap(infos.get("headscul")).scaled(
                self.headsculLabel.width(), self.headsculLabel.height())
        else:
            jpg = QtGui.QPixmap("picture/default_headscul.jpg").scaled(
                self.headsculLabel.width(), self.headsculLabel.height())

        self.headsculLabel.setPixmap(jpg)
        f.close()

    def autoLoginJudge(self):
        if self.autoLoginBox.isChecked():
            self.savePasswordBox.setChecked(True)

    #如果代码为1000，表示登录成功，显示好友列表widget

    def showupFriendList(self, msg):
        if msg.get("code") == 1000:

            self.setLocalProfile(msg.get("headscul"))

            self.mainWindow.hide()
            print(msg)
            #如果登陆成功，启动epoll处理信息
            t = threading.Thread(target=self.client.initiateServer)
            t.start()
            #注册fileno，表示可以开始进行epoll
            self.client.registFileNo()
            #开启文件传输socket
            self.client.filetrans.start(msg.get("fd"))

            widget = QDialog()
            listUi = List.Ui_Form()
            listUi.setupUi(widget)
            FriendsList(widget, msg, self.client)
            widget.show()
            widget.exec_()
            #self.mainWindow.show()  # 如果没有self.form.show()这一句，关闭Demo1界面后就会关闭程序
            self.setLogout()  # 退出登录
        else:
            self.client.p.shutdown(2)
            self.client.p.close()
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
        self.savePasswordBox = self.mainWindow.findChild(
            QCheckBox, "savePasswordBox")
        self.autoLoginBox = self.mainWindow.findChild(
            QCheckBox, "autoLoginBox")
        self.headsculLabel = self.mainWindow.findChild(QLabel, "headsculLabel")

    def reinitUi(self):
        self.headsculLabel.setFixedSize(150, 150)  # 设置头像区域大小为150x150

    def initEvent(self):
        self.startUpFriendList.connect(self.showupFriendList)
        self.loginButton.clicked.connect(lambda: self.Login())
        self.registButton.clicked.connect(lambda: self.Regist())
        self.autoLoginBox.toggled.connect(lambda: self.autoLoginJudge())


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
    startUpGroupNodes = QtCore.pyqtSignal(dict)
    broadcastLoginSignal = QtCore.pyqtSignal(dict)
    fileRecivedSignal = QtCore.pyqtSignal(str, QLabel)
    friendHeadsculSignal = QtCore.pyqtSignal(str, QLabel)
    addFriendSignal = QtCore.pyqtSignal(dict)
    addGroupSignal = QtCore.pyqtSignal(dict)
    deleteFriendSignal = QtCore.pyqtSignal(dict)
    deleteGroupSignal = QtCore.pyqtSignal(dict)
    dismissGroupSignal = QtCore.pyqtSignal(dict)

    def __init__(self, form, msg, client):
        super(FriendsList, self).__init__()
        self.ownerInfo = msg
        self.client = client
        self.form = form
        self.friendsNodes = []
        self.initComponent()
        self.initEvent()
        self.initInfos()

    #双击node打开对应聊天窗口

    def friendDoubleClicked(self):
        item = self.friendListWidget.selectedItems()[0]
        widget = self.friendListWidget.itemWidget(item)
        #从好友列表node中截取账号，有待修改
        targetAccount = widget.findChild(QLabel, "accountLabel").text()[2:-2]
        widget = Dialogs.ChatDialog()
        chatWindow = ChatWindow.Ui_Form()
        chatWindow.setupUi(widget)
        Chat(widget, self.ownerInfo.get("account"), targetAccount, self.client)
        widget.show()
        widget.exec_()

    def groupDoubleClicked(self):
        item = self.groupListWidget.selectedItems()[0]
        widget = self.groupListWidget.itemWidget(item)
        #从好友列表node中截取账号，有待修改
        targetAccount = widget.findChild(QLabel, "accountLabel").text()[2:-2]
        widget = Dialogs.GroupChatDialog()
        chatWindow = GroupChatWindow.Ui_Form()
        chatWindow.setupUi(widget)
        GroupChat(widget, self.ownerInfo.get(
            "account"), targetAccount, self.client, item.group_master)
        widget.show()
        widget.exec_()

    #填充好友列表
    def getFriendNodes(self):
        dataDic = dict(msgType=Protocol.searchFriend,
                       account=self.ownerInfo.get("account"))
        self.client.searchFriend(dataDic, self)

    def getGroupNodes(self):
        dataDic = dict(msgType=Protocol.GETGROUPS,
                       account=self.ownerInfo.get("account"))
        self.client.getGroups(dataDic)

    def searchFriendCallBack(self, all_data):
        print(all_data)
        if self.friendListWidget.count() > 0:
            for i in range(self.friendListWidget.count()-1, -1, -1):
                self.friendListWidget.removeItemWidget(
                    self.friendListWidget.takeItem(i))

        if all_data.get("code") == 1000:
            for friend in all_data.get("friends"):
                item = SubUnit.FriendListItem(
                    friend, self.client, self.fileRecivedSignal)  # 创建QListWidgetItem对象
                item.setSizeHint(QSize(200, 70))  # 设置QListWidgetItem大小
                widget = item.getItemWidget()  # 调用上面的函数获取对应

                self.friendListWidget.addItem(item)  # 添加item
                self.friendListWidget.setItemWidget(
                    item, widget)  # 为item设置widget
                self.friendsNodes.append(item)

    def getGroupsCallBack(self, all_data):
        if self.groupListWidget.count() > 0:
            for i in range(self.groupListWidget.count()-1, -1, -1):
                self.groupListWidget.removeItemWidget(
                    self.groupListWidget.takeItem(i))

        if all_data.get("code") == 1000:
            for group in all_data.get("groups"):
                item = SubUnit.GroupListItem(
                    group, self.client, self.fileRecivedSignal)  # 创建QListWidgetItem对象
                item.setSizeHint(QSize(200, 70))  # 设置QListWidgetItem大小
                widget = item.getItemWidget()  # 调用上面的函数获取对应

                self.groupListWidget.addItem(item)  # 添加item
                self.groupListWidget.setItemWidget(
                    item, widget)  # 为item设置widget
                #self.friendsNodes.append(item)

    def broadcastLoginCallBack(self, dict):
        for item in self.friendsNodes:
            if item.friend_account == dict.get("account"):
                item.changeLoginState(dict.get("flag"))

    def addFriend(self):
        text, ok = QInputDialog().getText(QWidget(), '添加好友', '输入好友账号:')
        if text and ok:
            dataDic = dict(msgType=Protocol.addFriend,
                           account=self.ownerInfo.get("account"), target=text)
            self.client.addFriend(dataDic)

    def addFriendCallBack(self, dict):
        code = dict.get("code")
        if code == 1000:
            self.getFriendNodes()
            QMessageBox.information(None, "成功", "添加成功", QMessageBox.Yes)
        elif code == 1001:
            QMessageBox.warning(None, "警告", "用户不存在", QMessageBox.Yes)
        elif code == 1002:
            QMessageBox.warning(None, "警告", "你们已经成为好友", QMessageBox.Yes)

    def addGroup(self):
        text, ok = QInputDialog().getText(QWidget(), '添加群', '输入群号:')
        if text and ok:
            dataDic = dict(msgType=Protocol.ADD_GROUP,
                           account=self.ownerInfo.get("account"), target=text)
            self.client.addGroup(dataDic)

    def addGroupCallBack(self, dict):
        code = dict.get("code")
        if code == 1000:
            self.getGroupNodes()
            QMessageBox.information(None, "成功", "添加成功", QMessageBox.Yes)
        elif code == 1001:
            QMessageBox.warning(None, "警告", "群号不存在", QMessageBox.Yes)
        elif code == 1002:
            QMessageBox.warning(None, "警告", "你已经加入该群", QMessageBox.Yes)

    def setGroup(self):
        form = QDialog()
        ui = SetGroup.Ui_Form()
        ui.setupUi(form)
        SetGroupEvent(form, self.client, self.ownerInfo, self)
        form.show()
        form.exec_()

    def deleteFriend(self):
        item = self.friendListWidget.selectedItems()[0]
        #widget = self.friendListWidget.itemWidget(item)
        #从好友列表node中截取账号，有待修改
        targetAccount = item.friend_account
        dataDict = dict(msgType=Protocol.DELETEFRIEND, account=self.ownerInfo.get(
            "account"), target=targetAccount)
        self.client.deleteFriend(dataDict)

    def deleteFriendCallBack(self, dict):
        code = dict.get("code")
        if code == 1000:
            self.getFriendNodes()
            QMessageBox.information(None, "成功", "删除成功", QMessageBox.Yes)
        elif code == 1001:
            QMessageBox.warning(None, "警告", "删除过程出现错误", QMessageBox.Yes)

    def deleteGroup(self):
        item = self.groupListWidget.selectedItems()[0]
        groupAccount = item.group_id
        dataDict = dict(msgType=Protocol.DELETEGROUP, account=self.ownerInfo.get(
            "account"), target=groupAccount)
        self.client.deleteGroup(dataDict)

    def deleteGroupCallBack(self, dict):
        code = dict.get("code")
        if code == 1000:
            self.getGroupNodes()
            QMessageBox.information(None, "成功", "退出成功", QMessageBox.Yes)
        elif code == 1001:
            QMessageBox.warning(None, "警告", "退出过程出现错误", QMessageBox.Yes)

    def dismissGroup(self):
        item = self.groupListWidget.selectedItems()[0]
        groupAccount = item.group_id
        dataDict = dict(msgType=Protocol.DISMISS_GROUP, target=groupAccount)
        self.client.dismissGroup(dataDict)

    def dismissGroupCallBack(self, dict):
        code = dict.get("code")
        if code == 1000:
            self.getGroupNodes()
            QMessageBox.information(None, "成功", "解散成功", QMessageBox.Yes)
        elif code == 1001:
            QMessageBox.warning(None, "警告", "解散过程出现错误", QMessageBox.Yes)

    #更新个人信息

    def changeOwnInfo(self, headscul=None, nickname=None, signature=None):
        if headscul is not None:
            try:
                #如果缓存中不存在这张图片文件，向服务器索取该文件
                if not os.path.exists(headscul):
                    if(headscul != ""):
                        self.client.getFile(headscul)
                        #文件接收线程
                        WaitFileThreading(
                            self.client, self.fileRecivedSignal, headscul, self.headsculLabel)
                    headscul = "picture/default_headscul.jpg"

                jpg = QtGui.QPixmap(headscul).scaled(
                    self.headsculLabel.width(), self.headsculLabel.height())
                self.headsculLabel.setPixmap(jpg)

            except Exception as e:
                print(e)
        if nickname is not None:
            self.nicknameLabel.setText(nickname)
        if signature is not None:
            self.signatureLabel.setText(signature)

    def showInfoWidget(self):
        form = QDialog()
        ui = PersonalInfo.Ui_Form()
        ui.setupUi(form)
        PersonalInfoEvent(form, self.client, self.ownerInfo)
        form.show()
        form.exec_()

    #改变label的图片
    def fileIsReceived(self, path, label):
        jpg = QtGui.QPixmap(path).scaled(
            label.width(), label.height())
        label.setPixmap(jpg)

    def initComponent(self):
        self.friendListWidget = self.form.findChild(QListWidget, "FriendsList")
        self.groupListWidget = self.form.findChild(QListWidget, "GroupList")
        self.infoButton = self.form.findChild(QPushButton, "infoButton")
        self.addFriendButton = self.form.findChild(QPushButton, "addFriendBtn")
        self.addGroupButton = self.form.findChild(QPushButton, "addGroupBtn")
        self.setGroupButton = self.form.findChild(QPushButton, "setGroupBtn")
        self.nicknameLabel = self.form.findChild(QLabel, "nicknameLabel")
        self.signatureLabel = self.form.findChild(QLabel, "signatureLabel")
        self.headsculLabel = self.form.findChild(QLabel, "headsculLabel")
        self.friendListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.friendListWidget.customContextMenuRequested.connect(
            self.friendCustomRightMenu)

        self.groupListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.groupListWidget.customContextMenuRequested.connect(
            self.groupCustomRightMenu)

    def initEvent(self):
        self.infoButton.clicked.connect(lambda: self.showInfoWidget())
        self.addFriendButton.clicked.connect(lambda: self.addFriend())
        self.addGroupButton.clicked.connect(lambda: self.addGroup())
        self.setGroupButton.clicked.connect(lambda: self.setGroup())
        self.friendListWidget.itemDoubleClicked.connect(
            lambda: self.friendDoubleClicked())
        self.groupListWidget.itemDoubleClicked.connect(
            lambda: self.groupDoubleClicked())
        self.startUpFriendNodes.connect(self.searchFriendCallBack)
        self.startUpGroupNodes.connect(self.getGroupsCallBack)
        self.broadcastLoginSignal.connect(self.broadcastLoginCallBack)
        self.fileRecivedSignal.connect(self.fileIsReceived)
        self.addFriendSignal.connect(self.addFriendCallBack)
        self.addGroupSignal.connect(self.addGroupCallBack)
        self.deleteFriendSignal.connect(self.deleteFriendCallBack)
        self.deleteGroupSignal.connect(self.deleteGroupCallBack)
        self.dismissGroupSignal.connect(self.dismissGroupCallBack)

    def initInfos(self):
        self.changeOwnInfo(headscul=self.ownerInfo.get("headscul"), nickname=self.ownerInfo.get(
            "nickname"), signature=self.ownerInfo.get("signature"))
        time.sleep(0.1)
        self.getFriendNodes()
        time.sleep(0.1)
        self.getGroupNodes()

    def friendCustomRightMenu(self, pos):
        menu = QtWidgets.QMenu()
        sendMessageAction = QAction(u'发送信息', self)
        deleteFriendAction = QAction(u'删除好友', self)
        sendMessageAction.triggered.connect(self.friendDoubleClicked)
        deleteFriendAction.triggered.connect(self.deleteFriend)
        menu.addAction(sendMessageAction)
        menu.addAction(deleteFriendAction)

        menu.exec_(self.friendListWidget.mapToGlobal(pos))

    def groupCustomRightMenu(self, pos):
        menu = QtWidgets.QMenu()
        sendMessageAction = QAction(u'发送信息', self)
        deleteGroupAction = QAction(u'退出此群', self)
        dismissGroupAction = QAction(u'解散此群', self)
        #sendMessageAction.triggered.connect(self.friendDoubleClicked)
        deleteGroupAction.triggered.connect(self.deleteGroup)
        dismissGroupAction.triggered.connect(self.dismissGroup)

        item = self.groupListWidget.selectedItems()[0]
        menu.addAction(sendMessageAction)
        if item.group_master == self.ownerInfo.get("account"):
            menu.addAction(dismissGroupAction)
        else:
            menu.addAction(deleteGroupAction)

        menu.exec_(self.groupListWidget.mapToGlobal(pos))


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

        self.client.sendMessage(dataDic)
        self.messageEditer.clear()

    def messageCallBack(self, dict):
        for msg in dict.get("messages"):
            if msg.get("sender") == self.ownerAccount:
                node = SubUnit.NodeItem("own", self.client)  # 调用上面的函数获取对应
            else:
                node = SubUnit.NodeItem("opposite", self.client)  # 调用上面的函数获取对应

            node.setMessage(msg)
            widget = node.getWidget()
            item = node.getItem()

            self.messageReceiver.addItem(item)  # 添加item
            self.messageReceiver.setItemWidget(item, widget)  # 为item设置widget

    def setupEmojiWidget(self):
        emojiWidget = QDialog()
        chatWindow = EmojiTable.Ui_Form()
        chatWindow.setupUi(emojiWidget)
        SubUnit.EmojiTab(emojiWidget, self)
        emojiWidget.show()
        emojiWidget.exec_()

    def chooseImg(self):
        imgNames, imgType = QFileDialog.getOpenFileNames(
            None, "打开图片", "/home/jiaxv/Pictures", "*.jpg;;*.png;;*.jpeg;;All Files(*)")

        for img in imgNames:
            path = self.client.filetrans.copyIntoTemp(img)
            print(path)
            self.client.filetrans.putFilePath(path)

            dataDic = dict(msgType=Protocol.sendMessage,
                           account=self.ownerAccount, target=self.targetAccount, message=path, form=MessageFormat.IMAGE)
            self.client.sendMessage(dataDic)

#聊天窗口


class GroupChat(QObject):
    getMessage = QtCore.pyqtSignal(dict)
    setGroupMembersSignal = QtCore.pyqtSignal(dict)

    def __init__(self, widget, ownerAccount, groupAccount, client, groupMaster) -> None:
        super(GroupChat, self).__init__()
        self.widget = widget
        self.ownerAccount = ownerAccount
        self.targetAccount = groupAccount
        self.groupMaster = groupMaster
        self.isMaster = True if ownerAccount == groupMaster else False
        self.client = client
        self.initComponent()
        self.initEvent()
        self.initMessageRecord()

    def initMessageRecord(self):
        dataDic = dict(msgType=Protocol.GETGROUPMESSAGERECORD,
                       account=self.ownerAccount, target=self.targetAccount)
        self.client.getGroupMessageRecord(dataDic, self)

    def initComponent(self):
        self.messageReceiver = self.widget.findChild(
            QListWidget, "messageList")
        self.groupMemberList = self.widget.findChild(
            QListWidget, "groupMemberList")
        self.messageEditer = self.widget.findChild(QTextEdit, "messageEditer")
        self.sendButton = self.widget.findChild(QPushButton, "sendButton")
        self.closeButton = self.widget.findChild(QPushButton, "closeButton")
        self.emojiWidget = self.widget.findChild(QPushButton, "emojiWidget")
        self.quitGroupButton = self.widget.findChild(QPushButton, "quitGroupButton")
        self.groupInfoButton = self.widget.findChild(QPushButton, "groupInfoButton")
        self.pictureButton = self.widget.findChild(
            QPushButton, "pictureButton")

        self.widget.targetAccount = self.targetAccount
        self.widget.client = self.client
        if self.isMaster:
            self.quitGroupButton.setText("解散此群")

    def initEvent(self):
        self.getMessage.connect(self.messageCallBack)
        self.setGroupMembersSignal.connect(self.setGroupMembers)
        self.sendButton.clicked.connect(lambda: self.sendMessage())
        self.emojiWidget.clicked.connect(lambda: self.setupEmojiWidget())
        self.pictureButton.clicked.connect(lambda: self.chooseImg())
        self.quitGroupButton.clicked.connect(lambda: self.quitGroup())

    #发送消息
    def sendMessage(self):
        dataDic = dict(msgType=Protocol.SENDGROUPMESSAGE,
                       account=self.ownerAccount, target=self.targetAccount, message=self.messageEditer.toPlainText(), form=MessageFormat.NORMAL)

        self.client.sendMessage(dataDic)
        self.messageEditer.clear()

    def messageCallBack(self, dict):
        for msg in dict.get("messages"):
            if msg.get("sender") == self.ownerAccount:
                node = SubUnit.NodeItem("own", self.client)  # 调用上面的函数获取对应
            else:
                node = SubUnit.NodeItem("opposite", self.client)  # 调用上面的函数获取对应

            node.setMessage(msg)
            widget = node.getWidget()
            item = node.getItem()

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

        for img in imgNames:
            path = self.client.filetrans.copyIntoTemp(img)
            self.client.filetrans.putFilePath(path)

            dataDic = dict(msgType=Protocol.SENDGROUPMESSAGE,
                           account=self.ownerAccount, target=self.targetAccount, message=path, form=MessageFormat.IMAGE)
            self.client.sendMessage(dataDic)

    def setGroupMembers(self, dict):
        if self.groupMemberList.count() > 0:
            for i in range(self.groupMemberList.count()-1, -1, -1):
                self.groupMemberList.removeItemWidget(
                    self.groupMemberList.takeItem(i))

        for group in dict.get("members"):
            item = SubUnit.GroupMembersItem(
                group, self.client, self)  # 创建QListWidgetItem对象
            item.setSizeHint(QSize(75, 50))  # 设置QListWidgetItem大小
            widget = item.getItemWidget()  # 调用上面的函数获取对应

            self.groupMemberList.addItem(item)  # 添加item
            self.groupMemberList.setItemWidget(item, widget)  # 为item设置widget
            #self.friendsNodes.append(item)

    def quitGroup(self):
        self.widget.close()
        if self.isMaster:
            dataDict = dict(msgType=Protocol.DELETEGROUP, account=self.ownerAccount, target=self.targetAccount)
            self.client.deleteGroup(dataDict)
        else:
            dataDict = dict(msgType=Protocol.DISMISS_GROUP, target=self.targetAccount)
            self.client.dismissGroup(dataDict)

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
        self.confirmButton.clicked.connect(lambda: self.closeWidget(1))
        self.cancelButton.clicked.connect(lambda: self.closeWidget(0))

    def initInfos(self):
        self.accountLabel.setText(self.ownerInfo.get("account"))
        self.passwordEdit.setText(self.ownerInfo.get("password"))
        self.nicknameEdit.setText(self.ownerInfo.get("nickname"))
        self.signatureEdit.setText(self.ownerInfo.get("signature"))

    def uploadHead(self):
        imgName, imgType = QFileDialog.getOpenFileName(
            None, "打开图片", "/home/jiaxv/Pictures", "*.jpg;;*.png;;*.jpeg;;All Files(*)")
        path = self.client.filetrans.copyIntoTemp(imgName, compress=True)
        self.client.filetrans.putFilePath(path)

        dictData = dict(msgType=Protocol.HEADSCUL,
                        account=self.ownerInfo.get("account"), filepath=path)

        self.client.updateHead(dictData)

    def closeWidget(self, flag):
        if flag == 1:
            QMessageBox.information(None, "成功", "保存成功", QMessageBox.Yes)
        self.form.close()


class SetGroupEvent(QObject):
    resultSignal = QtCore.pyqtSignal(int)

    def __init__(self, form, client, ownerinfo, groupList) -> None:
        super(SetGroupEvent, self).__init__()
        self.form = form
        self.client = client
        self.ownerinfo = ownerinfo
        self.groupList = groupList
        self.initComponent()
        self.initEvent()

    def initComponent(self):
        self.groupNameEdit = self.form.findChild(QLineEdit, "groupnameEdit")
        self.pictureButton = self.form.findChild(QPushButton, "pictureButton")
        self.confirmButton = self.form.findChild(QPushButton, "confirmButton")
        self.cancelButton = self.form.findChild(QPushButton, "cancelButton")

    def initEvent(self):
        self.pictureButton.clicked.connect(lambda: self.uploadHead())
        self.confirmButton.clicked.connect(lambda: self.sendRequest())
        self.cancelButton.clicked.connect(lambda: self.closeWidget())
        self.resultSignal.connect(self.resultCallBack)

    def uploadHead(self):
        imgName, imgType = QFileDialog.getOpenFileName(
            None, "打开图片", "/home/jiaxv/Pictures", "*.jpg;;*.png;;*.jpeg;;All Files(*)")
        self.imagePath = imgName

    def sendRequest(self):
        path = self.client.filetrans.copyIntoTemp(
            self.imagePath, compress=True)
        self.client.filetrans.putFilePath(path)

        dictData = dict(msgType=Protocol.SETGROUP,
                        account=self.ownerinfo.get("account"), picpath=path, groupname=self.groupNameEdit.text())

        self.client.setGroup(dictData, self)

    def resultCallBack(self, code):
        if code == 1000:
            self.groupList.getGroupNodes()
            QMessageBox.information(None, "成功", "创建成功", QMessageBox.Yes)
        else:
            QMessageBox.warning(None, "失败", "创建错误", QMessageBox.Yes)
        self.form.close()

    def closeWidget(self):
        self.form.close()
