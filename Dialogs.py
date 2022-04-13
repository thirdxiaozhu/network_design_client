from Protocol import Protocol
from PyQt5 import QtCore, QtGui, QtWidgets

class ChatDialog(QtWidgets.QDialog):
    """对QDialog类重写，实现一些功能"""

    targetAccount=""
    def closeEvent(self, event):
        dataDic = dict(msgType=Protocol.closeWindow,
                       target=self.targetAccount)
        self.client.closeChatWindow(dataDic)