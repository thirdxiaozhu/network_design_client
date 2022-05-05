import imp
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
import GroupFileWindow
import AdminWidget
from Protocol import *
from PyQt5.QtWidgets import *
from Client import Client
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets
from PIL import Image


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
        if msg.get("code") == 1000 and msg.get("type") == 0:

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
            self.setLogout()  # 退出登录

        elif msg.get("code") == 1000 and msg.get("type") == 1:
            print("This is admin")
            self.mainWindow.hide()
            widget = QDialog()
            adminUi = AdminWidget.Ui_Form()
            adminUi.setupUi(widget)
            #FriendsList(widget, msg, self.client)
            widget.show()
            widget.exec_()
            self.setLogout(type=1)  # 退出登录
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

    def setLogout(self, type = None):
        dataDic = dict(msgType=Protocol.LOGOUT,
                       account=self.account, type=type if type else 0)
        self.client.setLogout(dataDic, type)

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
    headsculSignal = QtCore.pyqtSignal(str, QPushButton)
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
        self.friendChatWidgets = {}
        self.groupChatWidgets = {}
        self.initComponent()
        self.initEvent()
        self.initInfos()

    #双击node打开对应聊天窗口

    def friendDoubleClicked(self):
        item = self.friendListWidget.selectedItems()[0]
        widget = self.friendListWidget.itemWidget(item)
        #从好友列表node中截取账号，有待修改
        targetAccount = widget.findChild(QLabel, "accountLabel").text()[2:-2]
        if self.friendChatWidgets.__contains__(targetAccount):
            self.friendChatWidgets.get(targetAccount).raise_()
        else:
            widget = Dialogs.ChatDialog()
            chatWindow = ChatWindow.Ui_Form()
            chatWindow.setupUi(widget)
            Chat(widget, self.ownerInfo.get("account"), targetAccount, self.client)
            widget.setWindowTitle(Status.status.get(item.friend_isonline))
            self.friendChatWidgets[targetAccount] = widget
            widget.show()
            widget.exec_()
            #关闭窗口后，取消widget的键值对
            self.friendChatWidgets.pop(targetAccount)

    def groupDoubleClicked(self):
        item = self.groupListWidget.selectedItems()[0]
        widget = self.groupListWidget.itemWidget(item)
        targetAccount = widget.findChild(QLabel, "accountLabel").text()[2:-2]
        if self.groupChatWidgets.__contains__(targetAccount):
            self.groupChatWidgets.get(targetAccount).raise_()
        else:
            widget = Dialogs.GroupChatDialog()
            chatWindow = GroupChatWindow.Ui_Form()
            chatWindow.setupUi(widget)
            GroupChat(widget, self.ownerInfo.get(
                "account"), targetAccount, self.client, item.group_master)
            self.groupChatWidgets[targetAccount] = widget
            widget.show()
            widget.exec_()
            self.groupChatWidgets.pop(targetAccount)

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
                #更改标题栏对应好友状态
                if self.friendChatWidgets.__contains__(item.friend_account):
                    self.friendChatWidgets.get(item.friend_account).setWindowTitle(Status.status.get(dict.get("flag")))

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
                            self.client, self.headsculSignal, headscul, self.infoButton)
                    headscul = "picture/default_headscul.jpg"

                self.infoButton.setStyleSheet("QPushButton{border-image: url(%s)}" % headscul)  # 设置背景图片，设置后一直存在

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

    #改变label的图片
    def headsculReceived(self, path, infoButton):
        infoButton.setStyleSheet("QPushButton{border-image: url(%s)}" % path)  # 设置背景图片，设置后一直存在
        
    def statusChange(self):
        msg = dict(msgType = Protocol.CHANGE_STATUS, account=self.ownerInfo.get("account"), status = self.statusBox.currentIndex()+1)
        self.client.changeStatus(msg)

    def initComponent(self):
        self.form.setWindowTitle("列表")
        self.friendListWidget = self.form.findChild(QListWidget, "FriendsList")
        self.groupListWidget = self.form.findChild(QListWidget, "GroupList")
        self.infoButton = self.form.findChild(QPushButton, "infoButton")
        self.addFriendButton = self.form.findChild(QPushButton, "addFriendBtn")
        self.addGroupButton = self.form.findChild(QPushButton, "addGroupBtn")
        self.setGroupButton = self.form.findChild(QPushButton, "setGroupBtn")
        self.nicknameLabel = self.form.findChild(QLabel, "nicknameLabel")
        self.signatureLabel = self.form.findChild(QLabel, "signatureLabel")
        self.statusBox = self.form.findChild(QComboBox, "statusComboBox")
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
        self.headsculSignal.connect(self.headsculReceived)
        self.addFriendSignal.connect(self.addFriendCallBack)
        self.addGroupSignal.connect(self.addGroupCallBack)
        self.deleteFriendSignal.connect(self.deleteFriendCallBack)
        self.deleteGroupSignal.connect(self.deleteGroupCallBack)
        self.dismissGroupSignal.connect(self.dismissGroupCallBack)
        self.statusBox.currentIndexChanged.connect(lambda: self.statusChange())

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
    imageSingal = QtCore.pyqtSignal(str, QTextEdit)
    fileReceiveSignal = QtCore.pyqtSignal(str, float, QtWidgets.QProgressBar)

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
        self.fileButton = self.widget.findChild(QPushButton, "fileButton")
        self.pictureButton = self.widget.findChild(
            QPushButton, "pictureButton")

        self.widget.targetAccount = self.targetAccount
        self.widget.client = self.client

        self.messageReceiver.setContextMenuPolicy(Qt.CustomContextMenu)
        self.messageReceiver.customContextMenuRequested.connect(
            self.itemCustomRightMenu)

    def initEvent(self):
        self.getMessage.connect(self.messageCallBack)
        self.imageSingal.connect(self.fileIsReceived)
        self.fileReceiveSignal.connect(self.fileReceiving)
        self.sendButton.clicked.connect(lambda: self.sendMessage())
        self.emojiWidget.clicked.connect(lambda: self.setupEmojiWidget())
        self.pictureButton.clicked.connect(lambda: self.chooseImg())
        self.fileButton.clicked.connect(lambda: self.chooseFile())

    #发送消息
    def sendMessage(self):
        dataDic = dict(msgType=Protocol.sendMessage,
                       account=self.ownerAccount, target=self.targetAccount, message=self.messageEditer.toPlainText(), form=MessageFormat.NORMAL)

        self.client.sendMessage(dataDic)
        self.messageEditer.clear()

    def messageCallBack(self, dict):
        for msg in dict.get("messages"):
            if msg.get("sender") == self.ownerAccount:
                item = SubUnit.NodeItem("own", self.client, self.imageSingal)  # 调用上面的函数获取对应
            else:
                item = SubUnit.NodeItem("opposite", self.client, self.imageSingal)  # 调用上面的函数获取对应

            item.setMessage(msg)
            widget = item.getWidget()

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
            path = self.client.filetrans.copyImgIntoTemp(img)
            print(path)
            self.client.filetrans.putFilePath(path)

            dataDic = dict(msgType=Protocol.sendMessage,
                           account=self.ownerAccount, target=self.targetAccount, message=path, form=MessageFormat.IMAGE)
            self.client.sendMessage(dataDic)

    def chooseFile(self):
        FileNames, type = QFileDialog.getOpenFileNames(
            None, "选择文件", os.environ["HOME"], "All Files(*)")
        print(FileNames)

        for filepath in FileNames:
            path = self.client.filetrans.copyFileIntoTemp(filepath)
            self.client.filetrans.putFilePath(path)

            dataDic = dict(msgType=Protocol.sendMessage,
                           account=self.ownerAccount, target=self.targetAccount, message=path, form=MessageFormat.FILE)
            self.client.sendMessage(dataDic)

    def startFileReceive(self):
        item = self.messageReceiver.selectedItems()[0]
        item.fileProcessBar.show()
        self.client.getFile(item.filePath)

        WaitFileThreading(self.client, self.fileReceiveSignal,
                          item.filePath, item.fileProcessBar, form=MessageFormat.FILE)

    def fileReceiving(self, path, process, processBar):
        processBar.setValue(int(process*100))
        print("process", process)

    def itemCustomRightMenu(self, pos):
        menu = QtWidgets.QMenu()
        receiveFileAction = QAction(u'接收文件', self)
        receiveFileAction.triggered.connect(self.startFileReceive)

        item = self.messageReceiver.selectedItems()[0]
        #menu.addAction(receiveFileAction)
        if item.form == MessageFormat.FILE:
            menu.addAction(receiveFileAction)

        menu.exec_(self.messageReceiver.mapToGlobal(pos))

    #改变label的图片
    def fileIsReceived(self, path, msgitem):
        msgitem.img = Image.open(path)

        currentWidth = msgitem.img.width
        if currentWidth > 300:
            currentHeight = msgitem.img.height * 300/msgitem.img.width
            currentWidth = 300
        else:
            currentHeight = msgitem.img.height

        #html标签根据width自适应大小
        imgDiv = "<img src=%s width=%s/>" % (path, currentWidth)
        msgitem.messageText.clear()
        message = (msgitem.html % (msgitem.align, msgitem.color, msgitem.msg.get("sender"),
                                msgitem.color, msgitem.msg.get("time"), imgDiv))

        msgitem.messageText.setMinimumHeight(
            msgitem.messageText.height() + currentHeight)
        msgitem.setSizeHint(QSize(500, currentHeight))  # 设置QListWidgetItem大小
        msgitem.messageText.append(message)


#聊天窗口


class GroupChat(QObject):
    getMessage = QtCore.pyqtSignal(dict)
    setGroupMembersSignal = QtCore.pyqtSignal(dict)
    imageSingal = QtCore.pyqtSignal(str, QTextEdit)

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
        self.groupFileButton = self.widget.findChild(QPushButton, "groupFileButton")
        self.pictureButton = self.widget.findChild(
            QPushButton, "pictureButton")

        self.widget.targetAccount = self.targetAccount
        self.widget.client = self.client
        if self.isMaster:
            self.quitGroupButton.setText("解散此群")

    def initEvent(self):
        self.getMessage.connect(self.messageCallBack)
        self.imageSingal.connect(self.fileIsReceived)
        self.setGroupMembersSignal.connect(self.setGroupMembers)
        self.sendButton.clicked.connect(lambda: self.sendMessage())
        self.emojiWidget.clicked.connect(lambda: self.setupEmojiWidget())
        self.pictureButton.clicked.connect(lambda: self.chooseImg())
        self.groupFileButton.clicked.connect(lambda: self.setFileWidget())
        self.quitGroupButton.clicked.connect(lambda: self.quitGroup())

        self.groupMemberList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.groupMemberList.customContextMenuRequested.connect(
            self.groupMemberRightMenu)

    def groupMemberRightMenu(self, pos):
        menu = QtWidgets.QMenu()
        removeMemberAction = QAction(u'移除此群', self)
        removeMemberAction.triggered.connect(self.removeMember)

        #menu.addAction(receiveFileAction)
        if self.groupMaster == self.ownerAccount:
            menu.addAction(removeMemberAction)

        menu.exec_(self.groupMemberList.mapToGlobal(pos))

    def removeMember(self):
        item = self.groupMemberList.selectedItems()[0]
        print(item.member_account)

    #发送消息
    def sendMessage(self):
        dataDic = dict(msgType=Protocol.SENDGROUPMESSAGE,
                       account=self.ownerAccount, target=self.targetAccount, message=self.messageEditer.toPlainText(), form=MessageFormat.NORMAL)

        self.client.sendMessage(dataDic)
        self.messageEditer.clear()

    def messageCallBack(self, dict):
        for msg in dict.get("messages"):
            if msg.get("sender") == self.ownerAccount:
                item = SubUnit.NodeItem("own", self.client, self.imageSingal)  # 调用上面的函数获取对应
            else:
                item = SubUnit.NodeItem("opposite", self.client, self.imageSingal)  # 调用上面的函数获取对应

            item.setMessage(msg)
            widget = item.getWidget()

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
            path = self.client.filetrans.copyImgIntoTemp(img)
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

    #改变label的图片
    def fileIsReceived(self, path, msgitem):
        msgitem.img = Image.open(path)

        currentWidth = msgitem.img.width
        if currentWidth > 300:
            currentHeight = msgitem.img.height * 300/msgitem.img.width
            currentWidth = 300
        else:
            currentHeight = msgitem.img.height

        #html标签根据width自适应大小
        imgDiv = "<img src=%s width=%s/>" % (path, currentWidth)
        msgitem.messageText.clear()
        message = (msgitem.html % (msgitem.align, msgitem.color, msgitem.msg.get("sender"),
                                msgitem.color, msgitem.msg.get("time"), imgDiv))

        msgitem.messageText.setMinimumHeight(
            msgitem.messageText.height() + currentHeight)
        msgitem.setSizeHint(QSize(500, currentHeight))  # 设置QListWidgetItem大小
        msgitem.messageText.append(message)

    def setFileWidget(self):
        widget = QDialog()
        fileWindow = GroupFileWindow.Ui_Form()
        fileWindow.setupUi(widget)
        GroupFile(widget, self.ownerAccount, self.targetAccount, self.client)
        widget.show()
        widget.exec_()
        self.client.closeGroupFileWindow(self.targetAccount)
        

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
        path = self.client.filetrans.copyImgIntoTemp(imgName, compress=True)
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
        path = self.client.filetrans.copyImgIntoTemp(
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

class GroupFile(QObject):
    uploadSignal = QtCore.pyqtSignal(dict)
    downloadSignal = QtCore.pyqtSignal(dict)
    getFileSignal = QtCore.pyqtSignal(list)
    fileReceiveSignal = QtCore.pyqtSignal(str, float, QtWidgets.QProgressBar)

    def __init__(self, form, ownerAccount, groupAccount, client) -> None:
        super(GroupFile, self).__init__()
        self.form = form
        self.ownerAccount = ownerAccount
        self.groupAccount = groupAccount
        self.client = client
        self.initComponent()
        self.initEvent()
        self.initFileTable()

    def initComponent(self):
        self.fileTable = self.form.findChild(QTableWidget, "fileTable")
        self.uploadButton = self.form.findChild(QPushButton, "upLoadFileButton")
        self.downloadButton = self.form.findChild(QPushButton, "downloadButton")

        self.fileTable.horizontalHeader().resizeSection(0,10) #设置第一列的宽度
        self.fileTable.horizontalHeader().resizeSection(1,150) 
        self.fileTable.horizontalHeader().resizeSection(2,40) 
        self.fileTable.horizontalHeader().resizeSection(3,120) 
        self.fileTable.horizontalHeader().setSectionResizeMode(4,QHeaderView.Stretch)#设置第五列宽度自动调整，充满屏幕
        self.fileTable.horizontalHeader().setSectionsClickable(False) #可以禁止点击表头的列
        self.fileTable.setEditTriggers(QAbstractItemView.NoEditTriggers) #设置表格不可更改
        self.fileTable.setShowGrid(False)

    def initEvent(self):
        self.uploadSignal.connect(self.uploadCallBack)
        self.downloadSignal.connect(self.downloadCallBack)
        self.getFileSignal.connect(self.initFileTableCallBack)
        self.fileReceiveSignal.connect(self.fileReceiving)
        self.uploadButton.clicked.connect(lambda: self.uploadFiles())
        self.downloadButton.clicked.connect(lambda: self.downloadFiles())

    def initFileTable(self):
        dictData = dict(msgType = Protocol.GET_GROUP_FILE, groupid = self.groupAccount)
        self.client.getGroupFile(dictData, self)

    def initFileTableCallBack(self, files):
        self.fileTable.setRowCount(0)
        self.fileTable.clearContents()
        for file in files:
            self.addTableColumn(file.get("path"), file.get("uploader"), file.get("uploadtime"), file.get("times"))
                              


    def uploadFiles(self):
        FileNames, type = QFileDialog.getOpenFileNames(
            None, "选择文件", os.environ["HOME"], "All Files(*)")
        print(FileNames)

        for filepath in FileNames:
            path = self.client.filetrans.copyFileIntoTemp(filepath, groupid = self.groupAccount)
            self.client.filetrans.putFilePath(path)

            dataDic = dict(msgType=Protocol.SEND_GROUP_FILE,
                           uploader=self.ownerAccount, groupid=self.groupAccount, path=path)
            self.client.sendGroupFile(dataDic, self)

    def uploadCallBack(self, file):
        self.addTableColumn(file.get("path"), file.get("uploader"), file.get("uploadtime"), file.get("times"))

    def downloadFiles(self):
        file_list = []
        for i in range(self.fileTable.rowCount()):
            if self.fileTable.cellWidget(i,0).findChild(QCheckBox, "checkbox").isChecked():
                file_list.append(self.fileTable.cellWidget(i,1).findChild(QLabel, "pathLabel").text())
        
        dataDict = dict(msgType = Protocol.DOWNLOAD_GROUP_FILE, files = file_list, groupid = self.groupAccount)
        self.client.downloadGroupFile(dataDict)

        for file in file_list:
            self.client.getFile(file)
            WaitFileThreading(self.client, self.fileReceiveSignal,
                              file, self.fileTable.cellWidget(i,1).findChild(QProgressBar, "fileProcessBar"), form=MessageFormat.FILE)

    def fileReceiving(self, path, process, processBar):
        processBar.setValue(int(process*100))
        print("process", process)

    def downloadCallBack(self, dict):
        path = dict.get("path")

    def addTableColumn(self, filepath, uploader, uploadtime, times):
        row = self.fileTable.rowCount()
        self.fileTable.setRowCount(row + 1)
        checkBox = QCheckBox()
        checkBox.setObjectName("checkbox")
        c0_layout = QHBoxLayout()
        c0_layout.setAlignment(Qt.AlignCenter)
        c0_layout.addWidget(checkBox)
        c0_widget = QWidget()
        c0_widget.setLayout(c0_layout)


        realPath = QtWidgets.QLabel(filepath)
        realPath.setObjectName("realPath")

        pathLabel = QtWidgets.QLabel(filepath)
        pathLabel.setObjectName("pathLabel")

        fileProcessBar = QtWidgets.QProgressBar()
        fileProcessBar.setProperty("value", 0)
        fileProcessBar.setObjectName("fileProcessBar")

        c1_layout = QVBoxLayout()
        c1_layout.setAlignment(Qt.AlignCenter)
        c1_layout.addWidget(pathLabel)
        c1_layout.addWidget(fileProcessBar)
        c1_widget = QWidget()
        c1_widget.setLayout(c1_layout)

        self.fileTable.setCellWidget(row,0,c0_widget)
        self.fileTable.setCellWidget(row,1,c1_widget)
        self.fileTable.setItem(row,2,QTableWidgetItem(uploader))
        self.fileTable.setItem(row,3,QTableWidgetItem(uploadtime))
        self.fileTable.setItem(row,4,QTableWidgetItem(str(times)))

        self.fileTable.setRowHeight(row, 50)

