import sys
import Ui_MainForm
import Register
import json
from Protocol import Protocol
from Windows import *
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import *
from Client import Client
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets


def main():
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainForm.Ui_MainWindow()
    ui.setupUi(mainWindow)
    LoginEvent(mainWindow, ui)
    mainWindow.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()