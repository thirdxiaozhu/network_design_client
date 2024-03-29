import datetime
import json
import time
from pydoc import cli
import threading
import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class Protocol:
    Login = 1
    Regist = 2
    addFriend = 3
    searchFriend = 4
    getMessageRecord = 5
    sendMessage = 6
    closeFriendWindow = 7
    sendFile = 8
    LOGOUT = 9
    HEADSCUL = 11
    GETFILE = 12
    DELETEFRIEND = 13
    SETGROUP = 14
    GETGROUPS = 15
    DELETEGROUP = 16
    SENDGROUPMESSAGE = 17
    GETGROUPMESSAGERECORD = 18
    CLOSE_GROUP_WINDOW = 19
    GET_GROUP_MEMBERS = 21
    DISMISS_GROUP = 22
    ADD_GROUP = 23
    REQUEST_FILE = 24
    CHANGE_STATUS = 25
    SEND_GROUP_FILE = 26
    GET_GROUP_FILE = 27
    DOWNLOAD_GROUP_FILE = 28
    SAVE_PROFILE = 31


class MessageFormat:
    NORMAL = 1
    IMAGE = 2
    FILE = 3

class Status:
    OFFLINE = 0
    ONLINE = 1
    BUSY = 2
    INVISIBLE = 3
    LEAVE = 4

    status = {
        0: "离线",
        1: "在线",
        2: "忙碌",
        3: "离线",
        4: "离开",
    }



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
    def __init__(self, client, signal, path, widget, form=MessageFormat.IMAGE) -> None:
        self.widget = widget
        if form == MessageFormat.IMAGE:
            threading.Thread(target=self.imgTarget, args=(
                client, signal, path)).start()
        else:
            threading.Thread(target=self.fileTarget, args=(
                client, signal, path)).start()


    def imgTarget(self, client, signal, path):
        while True:
            if client.filetrans.fileIsRecived(path):
                break
        signal.emit(path, self.widget)

    def fileTarget(self, client, signal, path):
        while True:
            process = client.filetrans.getFileProcess(path)
            if process:
                signal.emit(path, process, self.widget)
                if process == 1.0:
                    break

            time.sleep(0.1)