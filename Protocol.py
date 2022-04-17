import datetime
import json
from pydoc import cli
import threading
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from requests import patch


class Protocol:
    Login = 1
    Regist = 2
    addFriend = 3
    searchFriend = 4
    getMessageRecord = 5
    sendMessage = 6
    closeWindow = 7
    sendFile = 8
    LOGOUT = 9
    HEADSCUL = 11
    GETFILE = 12
    DELETEFRIEND = 13

    def __init__(self) -> None:
        pass


class MessageFormat:
    NORMAL = 1
    IMAGE = 2
    FILE = 3


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, bytes):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class Toast(QtWidgets.QWidget):

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing |
                               QtGui.QPainter.TextAntialiasing)
        rect_line_path = QtGui.QPainterPath()
        rectangle = QtCore.QRectF(0, 0, self.width, self.height)
        rect_line_path.addRoundedRect(
            rectangle, self.height/2, self.height/2, QtCore.Qt.AbsoluteSize)
        painter.fillPath(rect_line_path, QtGui.QColor(self.background_color))

        pen = QtGui.QPen(QtGui.QColor(self.text_color))
        painter.setPen(pen)
        painter.setFont(self.font)
        self.draw_text(painter)

#可停止线程，继承与threading.Thread


class KThread(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


class WaitFileThreading:
    def __init__(self, client, signal, path, label) -> None:
        self.label = label
        threading.Thread(target=self.target, args=(
            client, signal, path)).start()

    def target(self, client, signal, path):
        while True:
            if client.filetrans.fileIsRecived(path):
                break
        signal.emit(path, self.label)
