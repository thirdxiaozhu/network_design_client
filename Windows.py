from cgi import test
import Register
import List
import json
from Protocol import Protocol
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import *
from Client import Client
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets


#登录窗口
class LoginEvent:
    def __init__(self, mainWindow, ui):
        self.mainWindow = mainWindow
        self.ui = ui
        self.loginButton = self.mainWindow.findChild(QPushButton, "loginButton")
        self.account = self.mainWindow.findChild(QLineEdit, "accountEdit")
        self.password = self.mainWindow.findChild(QLineEdit, "passwordEdit")
        self.registButton = self.mainWindow.findChild(QPushButton, "registButton")
        self.reinitUi()
        self.initEvent()
    
    def reinitUi(self):
        self.ui.label.setFixedSize(150, 150)

    def initEvent(self):
        self.loginButton.clicked.connect(lambda:self.Login())
        self.registButton.clicked.connect(lambda:self.Regist())

    def Login(self):
        dataDic = dict(msgType = Protocol.Login, account = self.account.text(), password = self.password.text())
        print(dataDic)
        client = Client()
        msg = client.setupConnection(dataDic)
        if msg.get("code") == 1000:
            self.mainWindow.hide()            #如果没有self.form.show()这一句，关闭Demo1界面后就会关闭程序
            widget = QDialog()
            listUi = List.Ui_Form()
            listUi.setupUi(widget)
            FriendsList(widget, msg, client)
            widget.show()
            widget.exec_()
            self.mainWindow.show()
        else:
            QMessageBox.warning(self.mainWindow,"警告","用户名或密码错误",QMessageBox.Yes | QMessageBox.No)
            

    def Regist(self):
        self.mainWindow.hide()            #如果没有self.form.show()这一句，关闭Demo1界面后就会关闭程序
        form = QDialog()
        ui = Register.Ui_Form()
        ui.setupUi(form)
        RegisterEvent(self.mainWindow, form)
        form.show()
        form.exec_()
        self.mainWindow.show()


    def initComponent(self):
        pass


    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(None, "打开图片", "/home/jiaxv/Pictures", "*.jpg;;*.png;;*.jpeg;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.ui.label.width(), self.ui.label.height())
        self.ui.label.setPixmap(jpg)


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
            dataDic = dict(msgType = Protocol.Regist, id = self.id.text(), password = self.password.text(), nickname = self.nickname.text())
            client = Client()
            res = client.registConnection(dataDic)
            if res == 1000:
                QMessageBox.information(self.ui,"成功","添加成功",QMessageBox.Yes)
                self.cancleRegist()
            else:
                QMessageBox.warning(self.ui,"警告","账号已被注册",QMessageBox.Yes)
        else:
            QMessageBox.warning(self.ui,"警告","密码不一致",QMessageBox.Yes)

    def cancleRegist(self):
        self.ui.exec_()
        self.ui.close()
        self.father.show()

class FriendsList:
    def __init__(self, form, msg, client):
        self.ownerInfo = msg
        self.client = client
        self.form = form
        self.listWidget = form.findChild(QListWidget, "FriendsList")
        self.testButton = form.findChild(QPushButton, "infoButton")
        self.addFriendButton = form.findChild(QPushButton, "addFriendBtn")
        self.nicknameLabel = form.findChild(QLabel, "nicknameLabel")
        self.signatureLabel = form.findChild(QLabel, "signatureLabel")
        self.nicknameLabel.setText(self.ownerInfo.get("nickname"))
        self.signatureLabel.setText(self.ownerInfo.get("signature"))
        self.testButton.clicked.connect(lambda: self.deal())
        self.addFriendButton.clicked.connect(lambda: self.addFriend())

    def deal(self):
        print("deal")
        all_data = json.loads('[{"ship_name":"\u80e1\u5fb7","ship_country":"E\u56fd","ship_star":"5","ship_index":"1","ship_photo":"icon/1.png","ship_type":"\u6218\u5de1"},{"ship_name":"\u6d4b\u8bd5","ship_country":"E\u56fd","ship_star":"5","ship_index":"1","ship_photo":"icon/2.png","ship_type":"\u6218\u5de1"},{"ship_name":"\u6d4b\u8bd52","ship_country":"E\u56fd","ship_star":"5","ship_index":"1","ship_photo":"icon/3.png","ship_type":"\u6218\u5de1"},{"ship_name":"\u6d4b\u8bd53","ship_country":"E\u56fd","ship_star":"5","ship_index":"1","ship_photo":"icon/4.png","ship_type":"\u6218\u5de1"}]')

        for ship_data in all_data:
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setSizeHint(QSize(200, 50))  # 设置QListWidgetItem大小
            widget = self.get_item_wight(ship_data)  # 调用上面的函数获取对应
            self.listWidget.addItem(item)  # 添加item
            self.listWidget.setItemWidget(item, widget)  # 为item设置widget

    def get_item_wight(self,data):
        # 读取属性
        ship_name = data['ship_name']
        ship_photo = data['ship_photo']
        ship_type = data['ship_type']
        # 总Widget
        widget = QWidget()
        # 总体横向布局
        layout_main = QHBoxLayout()
        map_l = QLabel()  # 头像显示
        map_l.setFixedSize(40, 25)
        maps = QPixmap(ship_photo).scaled(40, 25)
        map_l.setPixmap(maps)
        # 右边的纵向布局
        layout_right = QVBoxLayout()
        # 右下的的横向布局
        layout_right_down = QHBoxLayout()  # 右下的横向布局
        layout_right_down.addWidget(QLabel(ship_type))
        # 按照从左到右, 从上到下布局添加
        layout_main.addWidget(map_l)  # 最左边的头像
        layout_right.addWidget(QLabel(ship_name))  # 右边的纵向布局
        layout_right.addLayout(layout_right_down)  # 右下角横向布局
        layout_main.addLayout(layout_right)  # 右边的布局
        widget.setLayout(layout_main)  # 布局给wight
        return widget  # 返回wight

    def addFriend(self):
        text, ok = QInputDialog().getText(QWidget(), '添加好友', '输入好友账号:')
        if text and ok:
            dataDic = dict(msgType = Protocol.addFriend, account = self.ownerInfo.get("account"), target = text)
            code = self.client.addFriend(dataDic)
            print(code)
            if code == 1000:
                QMessageBox.information(None,"成功","添加成功",QMessageBox.Yes)
            elif code == 1001:
                QMessageBox.warning(None ,"警告","用户不存在",QMessageBox.Yes)
            elif code == 1002:
                QMessageBox.warning(None ,"警告","你们已经成为好友",QMessageBox.Yes )

                


