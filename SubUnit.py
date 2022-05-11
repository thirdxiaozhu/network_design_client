import imp
import os
from imageWidget import Ui_Form as imageWidget
from PIL import Image
from Protocol import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *


class NodeItem(QtWidgets.QListWidgetItem):
    html = '<div align=%s> <font color=%s>%s   </font><font color=%s>( %s )<br></font> <font color=\"#000000\">%s</font></div>'

    def __init__(self, flag, client, imageSingal) -> None:
        super(NodeItem, self).__init__()
        self.client = client
        self.imageSingal = imageSingal

        self.initComponents()
        if flag == "own":
            self.widget = self.ownWidget()
        else:
            self.widget = self.oppositeWidget()

    def initComponents(self):
        self.horizontalLayoutWidget = QtWidgets.QWidget()
        self.friend_photo = ""
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 60, 501, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.friendphoto = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.friendphoto.setObjectName("friendphoto")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.messageText = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.messageText.setMinimumSize(QtCore.QSize(300, 50))
        self.messageText.setMaximumSize(QtCore.QSize(300, 1000))
        self.messageText.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.messageText.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.messageText.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.messageText.setObjectName("messageText")
        self.spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.messageText.setStyleSheet("background-color:transparent;")
        self.messageText.setFrameStyle(QFrame.NoFrame)
        #self.horizontalLayoutWidget.setStyleSheet("border: 1px solid black;")
        self.messageText.mouseDoubleClickEvent = self.doubleClickEvent
        self.verticalLayout.addWidget(self.messageText)
        self.fileProcessBar = QtWidgets.QProgressBar(self.horizontalLayoutWidget)
        self.fileProcessBar.setProperty("value", 0)
        self.fileProcessBar.setObjectName("fileProcessBar")
        self.verticalLayout.addWidget(self.fileProcessBar)
        self.fileProcessBar.hide()



        #self.imageSingal.connect(self.fileIsReceived)

    def oppositeWidget(self):
        self.horizontalLayout.addWidget(self.friendphoto)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.addItem(self.spacerItem)
        self.color = "#0000FF"
        self.align = "left"

    def ownWidget(self):
        self.horizontalLayout.addItem(self.spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.addWidget(self.friendphoto)
        self.color = "#00CC00"
        self.align = "right"

    def setMessage(self, msg):
        self.msg = msg
        self.form = msg.get("form")
        itemheight = self.getWidget().findChild(
            QTextEdit, "messageText").document().size().height() * 2 + 10
        if self.form == MessageFormat.NORMAL:
            message = (self.html % (self.align, self.color, msg.get("sender"),
                                    self.color, msg.get("time"), msg.get("message")))
            self.setSizeHint(QSize(500, int(itemheight))
                                  )  # 设置QListWidgetItem大小

        elif self.form == MessageFormat.IMAGE:
            #获取图片大小，并根据qtextedit大小缩放
            self.imgPath = msg.get("message")
            if not os.path.exists(self.imgPath):
                self.client.getFile(self.imgPath)
                #文件接收线程
                WaitFileThreading(
                    self.client, self.imageSingal, self.imgPath, self)

                message = (self.html % (self.align, self.color, msg.get("sender"),
                                        self.color, msg.get("time"), ""))
            else:
                self.img = Image.open(self.imgPath)

                currentWidth = self.img.width
                if currentWidth > 300:
                    currentHeight = self.img.height * 300/self.img.width
                    currentWidth = 300
                else:
                    currentHeight = self.img.height

                #html标签根据width自适应大小
                imgDiv = "<img src=%s width=%s/>" % (
                    self.imgPath, currentWidth)
                message = (self.html % (self.align, self.color, msg.get("sender"),
                                        self.color, msg.get("time"), imgDiv))

                self.messageText.setMinimumHeight(
                    int(self.messageText.height() + currentHeight))
                self.messageText.setMaximumHeight(
                    int(self.messageText.height() + currentHeight))
                # 设置QListWidgetItem大小
                self.setSizeHint(QSize(500, int(currentHeight)))

        elif self.form == MessageFormat.FILE:
            self.filePath = msg.get("message")
            self.filename = self.filePath.split("/")[-1]
            innermsg = "<font color='red'>文件,请右键保存   </font>"
            message = (self.html % (self.align, self.color, msg.get("sender"),
                                    self.color, msg.get("time"), innermsg + self.filename))
            self.setSizeHint(QSize(500, int(itemheight)))  # 设置QListWidgetItem大小
            #self.fileProcessBar.show()

        self.messageText.append(message)

    def doubleClickEvent(self, event):
        class ImageClass:
            def __init__(self, form, imgPath, img) -> None:
                jpg = QtGui.QPixmap(imgPath).scaled(
                    img.width, img.height)
                imageLabel = form.findChild(QLabel, "imageLabel")
                imageLabel.setPixmap(jpg)

                imageLabel.setMinimumWidth(img.width)
                imageLabel.setMinimumHeight(img.height)

                form.resize(img.width, img.height)

        if self.form == MessageFormat.IMAGE:
            form = QDialog()
            ui = imageWidget()
            ui.setupUi(form)
            ImageClass(form, self.imgPath, self.img)
            form.show()
            form.exec_()

    def getWidget(self):
        return self.horizontalLayoutWidget


class EmojiTab:
    def __init__(self, widget, chatWindow) -> None:
        self.widget = widget
        self.chatWindow = chatWindow
        self.widget.setWindowTitle("emoji")
        self.table = widget.findChild(QtWidgets.QTableWidget, "emojitable")
        self.table.itemClicked.connect(lambda: self.itemClick())

    def itemClick(self):
        self.chatWindow.messageEditer.moveCursor(QTextCursor.End)
        self.chatWindow.messageEditer.insertPlainText(
            self.table.currentItem().text())


class FriendListItem(QtWidgets.QListWidgetItem):

    def __init__(self, data, client, signal) -> None:
        super(FriendListItem, self).__init__()
        self.client = client
        self.signal = signal
        self.friend_name = data['nickname']
        self.friend_photo = ""
        self.friend_signature = data['signature']
        self.friend_account = data['account_2'] if data.__contains__(
            'account_2') else data['account_1']
        self.friend_isonline = data['isonline']
        self.friend_headscul = data['headscul']

    def getItemWidget(self):
        # 总Widget
        self.widget = QWidget()
        # 总体横向布局

        self.headsculLabel = QLabel()  # 头像显示
        self.headsculLabel.setFixedSize(60, 60)
        #如果缓存中不存在这张图片文件，向服务器索取该文件
        if not os.path.exists(self.friend_headscul):
            if self.friend_headscul != "":
                self.client.getFile(self.friend_headscul)
                #文件接收线程
                WaitFileThreading(self.client, self.signal,
                                  self.friend_headscul, self.headsculLabel)
            self.friend_headscul = "picture/default_headscul.jpg"
        jpg = QtGui.QPixmap(self.friend_headscul).scaled(
            self.headsculLabel.width(), self.headsculLabel.height())
        self.headsculLabel.setPixmap(jpg)

        if self.friend_isonline:
            color = "green"
        else:
            color = "red"
        nameLabel = QLabel(
            "<font color=%s face='黑体' size=4>%s<font>" % (color, self.friend_name))
        nameLabel.setObjectName("nameLabel")

        accountLabel = QLabel("( " + self.friend_account + " )")
        accountLabel.setObjectName("accountLabel")

        layout_main = QHBoxLayout()
        layout_right = QVBoxLayout()
        layout_right_up = QHBoxLayout()  # 右下的横向布局
        layout_right_down = QHBoxLayout()  # 右下的横向布局

        # 按照从左到右, 从上到下布局添加
        layout_main.addWidget(self.headsculLabel)  # 最左边的头像
        layout_main.addLayout(layout_right)  # 右边的布局

        layout_right_up.addWidget(nameLabel)
        layout_right_up.addWidget(accountLabel)
        layout_right.addLayout(layout_right_up)  # 右边的纵向布局

        layout_right_down.addWidget(QLabel(self.friend_signature))
        layout_right.addLayout(layout_right_down)  # 右下角横向布局

        self.widget.setLayout(layout_main)  # 布局给wight

        return self.widget  # 返回wight

    def changeLoginState(self, flag):
        self.friend_isonline = flag
        label = self.widget.findChild(QLabel, "nameLabel")
        if flag == Status.ONLINE:
            color = "green"
        elif flag == Status.BUSY:
            color = "blue"
        elif flag == Status.LEAVE:
            color = "pink"
        else:
            color = "red"

        label.setText("<font color=%s face='黑体' size=4>%s<font>" %
                      (color, self.friend_name))

    #改变label的图片
    def fileIsReceived(self, path, label):
        #self.changeOwnInfo(headscul=path)
        jpg = QtGui.QPixmap(path).scaled(
            label.width(), label.height())
        label.setPixmap(jpg)

    def getHeadSculLabel(self):
        return self.headsculLabel


class GroupListItem(QtWidgets.QListWidgetItem):

    def __init__(self, data, client, signal) -> None:
        super(GroupListItem, self).__init__()
        self.client = client
        self.signal = signal
        self.group_name = data['groupname']
        self.group_photo = ""
        self.group_id = data['groupid']
        self.group_headscul = data['groupscal']
        self.group_master = data['master']

    def getItemWidget(self):
        # 总Widget
        self.widget = QWidget()
        # 总体横向布局

        self.headsculLabel = QLabel()  # 头像显示
        self.headsculLabel.setFixedSize(60, 60)
        #如果缓存中不存在这张图片文件，向服务器索取该文件
        if not os.path.exists(self.group_headscul):
            if self.group_headscul != "":
                self.client.getFile(self.group_headscul)
                #文件接收线程
                WaitFileThreading(self.client, self.signal,
                                  self.group_headscul, self.headsculLabel)
            self.group_headscul = "picture/default_headscul.jpg"
        jpg = QtGui.QPixmap(self.group_headscul).scaled(
            self.headsculLabel.width(), self.headsculLabel.height())
        self.headsculLabel.setPixmap(jpg)
        nameLabel = QLabel(
            "<font color='black' face='黑体' size=4>%s<font>" % self.group_name)
        nameLabel.setObjectName("nameLabel")

        accountLabel = QLabel("( " + self.group_id + " )")
        accountLabel.setObjectName("accountLabel")

        layout_main = QHBoxLayout()
        layout_right = QVBoxLayout()
        layout_right_up = QHBoxLayout()  # 右下的横向布局
        layout_right_down = QHBoxLayout()  # 右下的横向布局

        # 按照从左到右, 从上到下布局添加
        layout_main.addWidget(self.headsculLabel)  # 最左边的头像
        layout_main.addLayout(layout_right)  # 右边的布局

        layout_right_up.addWidget(nameLabel)
        layout_right_up.addWidget(accountLabel)
        layout_right.addLayout(layout_right_up)  # 右边的纵向布局

        #layout_right_down.addWidget(QLabel(self.friend_signature))
        #layout_right.addLayout(layout_right_down)  # 右下角横向布局

        self.widget.setLayout(layout_main)  # 布局给wight

        return self.widget  # 返回wight

    #改变label的图片

    def fileIsReceived(self, path, label):
        #self.changeOwnInfo(headscul=path)
        jpg = QtGui.QPixmap(path).scaled(
            label.width(), label.height())
        label.setPixmap(jpg)

    def getHeadSculLabel(self):
        return self.headsculLabel


class GroupMembersItem(QtWidgets.QListWidgetItem):

    def __init__(self, data, client, groupchatwindow) -> None:
        super(GroupMembersItem, self).__init__()
        self.client = client
        self.groupchatwindow = groupchatwindow
        self.member_name = data['nickname']
        self.member_photo = ""
        self.member_account = data['account']
        self.member_isonline = data['isonline']
        #self.friend_headscul = data['headscul']

    def getItemWidget(self):
        # 总Widget
        self.widget = QWidget()
        # 总体横向布局

        self.headsculLabel = QLabel()  # 头像显示
        self.headsculLabel.setFixedSize(60, 60)
        ##如果缓存中不存在这张图片文件，向服务器索取该文件
        #if not os.path.exists(self.friend_headscul):
        #    if self.friend_headscul != "":
        #        self.client.getFile(self.friend_headscul)
        #        #文件接收线程
        #        WaitFileThreading(self.client, self.signal, self.friend_headscul, self.headsculLabel)
        #    self.friend_headscul = "picture/default_headscul.jpg"
        #jpg = QtGui.QPixmap(self.friend_headscul).scaled(
        #    self.headsculLabel.width(), self.headsculLabel.height())
        #self.headsculLabel.setPixmap(jpg)

        if self.member_isonline:
            color = "green"
        else:
            color = "black"
        if self.groupchatwindow.groupMaster == self.member_account:
            color = "red"

        nameLabel = QLabel(
            "<font color=%s face='黑体' size=4>%s<font>" % (color, self.member_name))
        nameLabel.setObjectName("nameLabel")

        accountLabel = QLabel("( " + self.member_account + " )")
        accountLabel.setObjectName("accountLabel")

        layout_main = QHBoxLayout()
        layout_right = QVBoxLayout()
        layout_right_up = QHBoxLayout()  # 右下的横向布局
        #layout_right_down = QHBoxLayout()  # 右下的横向布局

        # 按照从左到右, 从上到下布局添加
        layout_main.addLayout(layout_right)  # 右边的布局

        layout_right_up.addWidget(nameLabel)
        layout_right_up.addWidget(accountLabel)
        layout_right.addLayout(layout_right_up)  # 右边的纵向布局

        self.widget.setLayout(layout_main)  # 布局给wight

        return self.widget  # 返回wight

    def changeLoginState(self, flag):
        label = self.widget.findChild(QLabel, "nameLabel")
        if flag:
            color = "green"
        else:
            color = "black"
        if self.groupchatwindow.groupMaster == self.member_account:
            color = "red"

        label.setText("<font color=%s face='黑体' size=4>%s<font>" %
                      (color, self.member_name))

    #改变label的图片
    def fileIsReceived(self, path, label):
        #self.changeOwnInfo(headscul=path)
        jpg = QtGui.QPixmap(path).scaled(
            label.width(), label.height())
        label.setPixmap(jpg)

    def getHeadSculLabel(self):
        return self.headsculLabel


class AdminListItem(QtWidgets.QListWidgetItem):

    def __init__(self, account, client, signal) -> None:
        super(AdminListItem, self).__init__()
        self.client = client
        self.signal = signal
        self.account = account

    def getItemWidget(self):
        # 总Widget
        self.widget = QWidget()
        # 总体横向布局

        checkBox = QCheckBox()
        checkBox.setObjectName("checkbox")

        accountLabel = QLabel(self.account)
        accountLabel.setObjectName("accountLabel")

        print(accountLabel.text())

        layout_main = QHBoxLayout()

        # 按照从左到右, 从上到下布局添加
        layout_main.addWidget(accountLabel)  # 最左边的头像
        layout_main.addWidget(checkBox)  # 最左边的头像
        self.widget.setLayout(layout_main)  # 布局给wight

        return self.widget  # 返回wight

    #改变label的图片

    def fileIsReceived(self, path, label):
        #self.changeOwnInfo(headscul=path)
        jpg = QtGui.QPixmap(path).scaled(
            label.width(), label.height())
        label.setPixmap(jpg)

    def getHeadSculLabel(self):
        return self.headsculLabel

