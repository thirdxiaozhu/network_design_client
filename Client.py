from dataclasses import dataclass
import imp
import json
from queue import Queue
import socket
from PyQt5.QtWidgets import *
import select
import Protocol
import os
import FileTrans 
import time


class Client:
    def __init__(self):
        self.p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.epoll_fd = select.epoll()
        self.filetrans = FileTrans.FileSocket()
        self.addresses = {}
        self.datalist = {}
        self.chatClasses = {}

    #用一个子线程处理epoll
    def initiateServer(self):
        while True:
            # epoll 进行 fd 扫描的地方 -- 未指定超时时间则为阻塞等待
            epoll_list = self.epoll_fd.poll()
            for fd, events in epoll_list:
                print(fd, "===>", events)
                # 若为监听 fd 被激活
                if select.EPOLLIN & events:
                    self.receiveEvent()
                elif select.EPOLLOUT & events:
                    self.writeEvent()
                elif select.EPOLLHUP & events:
                    self.hupEvent(fd)
                else:
                    # 其他 epoll 事件不进行处理
                    continue

    def connectEvent(self, fd):
        self.epoll_fd.register(
            fd, select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
        pass

    def receiveEvent(self):
        data = self.p.recv(8192)
        self.handleReceived(data)

    def writeEvent(self):
        sendLen = 0
        while True:
            print(self.datalist)
            sendLen += self.p.send(
                (self.datalist[sendLen:]).encode())
            if sendLen == len(self.datalist.encode()):
                break
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLET | select.EPOLLERR | select.EPOLLHUP)

    def hupEvent(self, fd):
        pass

    def handleReceived(self, datas):
        print(datas)
        dict = json.loads(datas)
        numbers = {
            3: self.addFriend,
            4: self.searchFriendEvent,
            5: self.messageRecordEvent,
            6: self.getNewMessage,
            10: self.broadcastLogin,
        }

        method = numbers.get(dict.get("msgType"))
        if method:
            method(dict)

    #利用普通传输处理连接，如果成功那么再启用epoll
    def setupConnection(self, data, loginClass):
        self.loginClass = loginClass
        self.p.connect(('49.232.147.37', 8080))

        self.p.send(self.jsonProcessing(data).encode())
        dict = self.p.recv(1024)
        self.loginEvent(json.loads(dict))

    def loginEvent(self, dict):
        self.ownerAccount = dict.get("account")
        self.loginClass.startUpFriendList.emit(dict)

    def searchFriendEvent(self, dict):
        self.friendListClass.startUpFriendNodes.emit(dict)

    def messageRecordEvent(self, dict):
        if dict.get("code") == 1000:
            #if self.chatClass
            sender = dict.get("messages")[0].get("sender")
            recipient = dict.get("messages")[0].get("recipient")
            targetAccount = sender if self.ownerAccount == recipient else recipient

            self.chatClasses.get(targetAccount).getMessage.emit(dict)

    def getNewMessage(self, dict):
        print(dict)
        self.messageRecordEvent(dict)


    def searchFriend(self, data, friendListClass):
        self.friendListClass = friendListClass
        self.datalist = self.jsonProcessing(data)
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def getMessageRecord(self, data, chatClass):
        target = data.get("target")
        if not self.chatClasses.__contains__(target):
            self.chatClasses[target] = chatClass

        self.datalist = self.jsonProcessing(data)
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def closeChatWindow(self, data):
        target = data.get("target")
        self.chatClasses.pop(target)

        self.datalist = self.jsonProcessing(data)
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def sendMessage(self, data):
        self.datalist = self.jsonProcessing(data)
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def registConnection(self, data):
        self.p.connect(('49.232.147.37', 8080))
        self.p.send(self.jsonProcessing(data).encode("utf-8"))
        msg = self.p.recv(1024)
        self.p.close()

        msg = json.loads(msg.decode("utf-8"))

        return msg.get("code")

    def sendFile(self, fileLine):
        pass

    def setLogout(self, data):
        self.datalist = self.jsonProcessing(data)
        self.p.send(self.datalist.encode())
        #关闭文件传输socket
        self.filetrans.closeTrans()
        time.sleep(1)
        os._exit(0)

    def addFriend(self, data):
        self.p.send(self.jsonProcessing(data).encode("utf-8"))
        msg = self.p.recv(1024)
        msg = json.loads(msg.decode("utf-8"))

        return msg.get("code")

    def getChatRecord(self, data):
        self.p.send(self.jsonProcessing(data).encode("utf-8"))
        msg = self.p.recv(1024)
        msg = json.loads(msg.decode("utf-8"))

        return msg

    def broadcastLogin(self, dict):
        self.friendListClass.broadcastLoginSignal.emit(dict)

    def registFileNo(self):
        try:
            self.epoll_fd.register(
                self.p.fileno(), select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
        except Exception as e:
            print(e)

    def __del__(self):
        self.p.close()

    def jsonProcessing(self, data):
        return json.dumps(data, cls=Protocol.DateEncoder)
