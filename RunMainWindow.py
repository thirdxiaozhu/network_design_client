import sys
import Ui_MainForm
from Windows import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def main():
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainForm.Ui_MainWindow()
    ui.setupUi(mainWindow)
    LoginEvent(mainWindow, ui)
    mainWindow.setWindowTitle("登录")
    mainWindow.show()
    app.exec_()
    sys.exit()

if __name__ == "__main__":
    main()