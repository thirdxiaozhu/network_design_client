from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
class myC(QWidget):
    def __init__(self):
        super().__init__()
        hlay = QHBoxLayout(self)
        hlay.setContentsMargins(0,0,0,0)
        hlay.setSpacing(0)
        self.lable = QLabel("this is lable")
        line = QLineEdit()
        btn = QPushButton("btn")
        hlay.addWidget(self.lable)
        hlay.addWidget(line)
        hlay.addWidget(btn)
        self.setLayout(hlay)
        btn.pressed.connect(self.btnclick)
    def setxy(self,x,y):
        self.x = x
        self.y = y
    def btnclick(self):
        print("xy:",self.x," ",self.y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    list = QListWidget()
    for rown in range(10):
        item = QListWidgetItem()
        wg = myC()
        wg.setxy(rown,0)
        wg.lable.setText(wg.lable.text()+" "+str(rown))
        list.addItem(item)
        list.setItemWidget(item,wg)
    list.show()
    app.exec_()