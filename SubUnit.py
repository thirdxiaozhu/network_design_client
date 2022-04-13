from turtle import color
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *

class NodeItem:
    def __init__(self, flag) -> None:
        self.horizontalLayoutWidget = QtWidgets.QWidget()
        self.initComponents()
        if flag == "own":
            self.widget = self.ownWidget()
        else:
            self.widget = self.oppositeWidget()

    def initComponents(self):
        self.friend_photo = ""
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 60, 501, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.friendphoto = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.friendphoto.setObjectName("friendphoto")
        self.messageText = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.messageText.setMinimumSize(QtCore.QSize(300, 0))
        self.messageText.setMaximumSize(QtCore.QSize(300, 16777215))
        self.messageText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.messageText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.messageText.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.messageText.setObjectName("messageText")
        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.messageText.setStyleSheet("background-color:transparent;")
        #self.horizontalLayoutWidget.setStyleSheet("border: 1px solid black;")


    def oppositeWidget(self):
        self.horizontalLayout.addWidget(self.friendphoto)
        self.horizontalLayout.addWidget(self.messageText)
        self.horizontalLayout.addItem(self.spacerItem)

    def ownWidget(self):
        self.horizontalLayout.addItem(self.spacerItem)
        self.horizontalLayout.addWidget(self.messageText)
        self.horizontalLayout.addWidget(self.friendphoto)

    def setMessage(self, msg):
        self.messageText.append(msg)

class EmojiTab:
    def __init__(self, widget, chatWindow) -> None:
        self.widget = widget
        self.chatWindow = chatWindow
        self.table = widget.findChild(QtWidgets.QTableWidget, "emojitable")
        self.table.itemClicked.connect(lambda: self.itemClick())

    def itemClick(self):
        self.chatWindow.messageEditer.moveCursor(QTextCursor.End)
        self.chatWindow.messageEditer.insertPlainText(self.table.currentItem().text())

        
class FriendListItem(QtWidgets.QListWidgetItem):
    def __init__(self, data) -> None:
        super(FriendListItem, self).__init__()
        self.friend_name = data['nickname']
        self.friend_photo = ""
        self.friend_signature = data['signature']
        self.friend_account = data['account_2'] if data.__contains__(
            'account_2') else data['account_1']
        self.friend_isonline = data['isonline']

    def getItemWidget(self):
        # 总Widget
        self.widget = QWidget()
        # 总体横向布局
        map_l = QLabel()  # 头像显示
        map_l.setFixedSize(40, 25)
        maps = QPixmap(self.friend_photo).scaled(40, 25)
        map_l.setPixmap(maps)

        if self.friend_isonline:
            color = "green"
        else:
            color = "red"
        nameLabel = QLabel("<font color=%s face='黑体' size=4>%s<font>" % (color, self.friend_name))
        nameLabel.setObjectName("nameLabel")

        accountLabel = QLabel("( " + self.friend_account + " )")
        accountLabel.setObjectName("accountLabel")

        layout_main = QHBoxLayout()
        layout_right = QVBoxLayout()
        layout_right_up = QHBoxLayout()  # 右下的横向布局
        layout_right_down = QHBoxLayout()  # 右下的横向布局

        # 按照从左到右, 从上到下布局添加
        layout_main.addWidget(map_l)  # 最左边的头像
        layout_main.addLayout(layout_right)  # 右边的布局

        layout_right_up.addWidget(nameLabel)
        layout_right_up.addWidget(accountLabel)
        layout_right.addLayout(layout_right_up)  # 右边的纵向布局

        layout_right_down.addWidget(QLabel(self.friend_signature))
        layout_right.addLayout(layout_right_down)  # 右下角横向布局

        self.widget.setLayout(layout_main)  # 布局给wight

        return self.widget  # 返回wight

    def changeLoginState(self, flag):
        label = self.widget.findChild(QLabel, "nameLabel")
        if flag:
            color = "green"
        else:
            color = "red"

        label.setText("<font color=%s face='黑体' size=4>%s<font>" % (color, self.friend_name))

