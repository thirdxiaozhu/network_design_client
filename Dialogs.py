from Protocol import Protocol
from PyQt5 import QtCore, QtGui, QtWidgets

class ChatDialog(QtWidgets.QDialog):

    targetAccount=""
    def closeEvent(self, event):
        dataDic = dict(msgType=Protocol.closeFriendWindow,
                       target=self.targetAccount)
        self.client.closeChatWindow(dataDic)

class GroupChatDialog(QtWidgets.QDialog):

    targetAccount=""
    def closeEvent(self, event):
        dataDic = dict(msgType=Protocol.CLOSE_GROUP_WINDOW,
                       target=self.targetAccount)
        self.client.closeChatWindow(dataDic)