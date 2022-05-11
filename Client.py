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
        self.epoll_fd = select.epoll()
        self.filetrans = FileTrans.FileSocket()
        self.addresses = {}
        self.datalist = Queue()
        self.chatClasses = {}
        self.groupChatClasses = {}
        self.groupFileClasses = {}

    #用一个子线程处理epoll
    def initiateServer(self):
        while True:
            # epoll 进行 fd 扫描的地方 -- 未指定超时时间则为阻塞等待
            epoll_list = self.epoll_fd.poll()
            print(epoll_list)
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
        self.handleReceived(data.decode())

    def writeEvent(self):
        while self.datalist.qsize() > 0:
            sendLen = 0
            while True:
                msg = self.datalist.get()
                print(msg)
                sendLen += self.p.send(
                    (msg[sendLen:]).encode())
                if sendLen == len(msg.encode()):
                    break
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLET | select.EPOLLERR | select.EPOLLHUP)

    def hupEvent(self, fd):
        pass

    def handleReceived(self, datas):
        print(datas, type(datas))
        #防止粘包（多个json串在一个字符串里）
        dec = json.JSONDecoder()
        pos = 0
        while not pos == len(str(datas)):
            dict, json_len = dec.raw_decode(str(datas)[pos:])
            pos += json_len
            #cdict = json.loads(j)
            numbers = {
                3: self.addFriendEvent,
                4: self.searchFriendEvent,
                5: self.messageRecordEvent,
                6: self.getNewMessage,
                10: self.broadcastLogin,
                11: self.updateHeadEvent,
                13: self.deleteFriendEvent,
                14: self.setGroupEvent,
                15: self.getGroupsEvent,
                16: self.deleteGroupEvent,
                18: self.groupMessageRecordEvent,
                20: self.getNewGroupMessage,
                21: self.setGroupMembers,
                22: self.dismissGroupEvent,
                23: self.addGroupEvent,
                26: self.sendGroupFileEvent,
                27: self.getGroupFileEvent,
                28: self.downloadGroupFileEvent,
                29: self.groupLogin,
                30: self.adminUserLoginMessage,
                31: self.saveProfileEvent,
                32: self.initAdminListEvent,
                33: self.adminUserLogoutMessage,
            }

            method = numbers.get(dict.get("msgType"))
            if method:
                method(dict)

    #利用普通传输处理连接，如果成功那么再启用epoll
    def setupConnection(self, data, loginClass):
        self.loginClass = loginClass
        self.p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p.connect(('49.232.147.37', 8080))

        self.p.send(self.jsonProcessing(data).encode())
        dict = self.p.recv(1024)
        self.loginEvent(json.loads(dict))

    def loginEvent(self, dict):
        self.usertype = dict.get("type")
        self.ownerAccount = dict.get("account")
        print(dict)
        self.loginClass.startUpFriendList.emit(dict)

    def registFileNo(self):
        try:
            self.epoll_fd.register(
                self.p.fileno(), select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
        except Exception as e:
            print(e)

    def messageRecordEvent(self, dict):
        if dict.get("code") == 1000:
            sender = dict.get("messages")[0].get("sender")
            recipient = dict.get("messages")[0].get("recipient")
            targetAccount = sender if self.ownerAccount == recipient else recipient

            self.chatClasses.get(targetAccount).getMessage.emit(dict)

    def groupMessageRecordEvent(self, dict):
        if dict.get("code") == 1000:
            groupid = dict.get("messages")[0].get("groupid")
            self.groupChatClasses.get(groupid).getMessage.emit(dict)

    def getNewMessage(self, dict):
        self.messageRecordEvent(dict)

    def getNewGroupMessage(self, dict):
        self.groupMessageRecordEvent(dict)

    def searchFriend(self, data, friendListClass):
        self.friendListClass = friendListClass
        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def searchFriendEvent(self, dict):
        self.friendListClass.startUpFriendNodes.emit(dict)

    def getGroups(self, data):
        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def getMessageRecord(self, data, chatClass):
        target = data.get("target")
        if not self.chatClasses.__contains__(target):
            self.chatClasses[target] = chatClass

        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def getGroupMessageRecord(self, data, groupChatClass):
        target = data.get("target")
        if not self.groupChatClasses.__contains__(target):
            self.groupChatClasses[target] = groupChatClass

        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def getGroupMembers(self, data):
        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def closeChatWindow(self, data):
        target = data.get("target")
        if data.get("msgType") == Protocol.Protocol.closeFriendWindow:
            self.chatClasses.pop(target)
        else:
            self.groupChatClasses.pop(target)

        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def closeGroupFileWindow(self, groupid):
        self.groupFileClasses.pop(groupid)

    def sendMessage(self, data):
        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def registConnection(self, data):
        self.p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p.connect(('49.232.147.37', 8080))
        self.p.send(self.jsonProcessing(data).encode("utf-8"))
        msg = self.p.recv(1024)
        self.p.close()

        msg = json.loads(msg.decode("utf-8"))

        return msg.get("code")

    def sendFile(self, fileLine):
        pass

    def setLogout(self, data, type):
        #self.datalist.put(self.jsonProcessing(data))
        #立即发送
        self.p.send(self.jsonProcessing(data).encode())
        #关闭文件传输socket
        self.filetrans.closeTrans(type)
        time.sleep(1)
        os._exit(0)

    def addFriend(self, data):
        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def addFriendEvent(self, dict):
        print(dict)
        self.friendListClass.addFriendSignal.emit(dict)

    def addGroup(self, data):
        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def addGroupEvent(self, dict):
        print(dict)
        self.friendListClass.addGroupSignal.emit(dict)

    def deleteFriend(self, data):
        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def deleteFriendEvent(self, dict):
        self.friendListClass.deleteFriendSignal.emit(dict)

    def deleteGroup(self, data):
        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def deleteGroupEvent(self, data):
        if data.get("account") == self.friendListClass.ownerInfo.get("account"):
            self.friendListClass.deleteGroupSignal.emit(data)
        else:
            self.groupChatClasses.get(
                data.get("groupid")).removeMemberSignal.emit()

    def dismissGroup(self, data):
        self.datalist.put(self.jsonProcessing(data))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def dismissGroupEvent(self, data):
        self.friendListClass.dismissGroupSignal.emit(data)

    def getChatRecord(self, data):
        self.p.send(self.jsonProcessing(data).encode("utf-8"))
        msg = self.p.recv(1024)
        msg = json.loads(msg.decode("utf-8"))

        return msg

    def broadcastLogin(self, dict):
        self.friendListClass.broadcastLoginSignal.emit(dict)

    def updateHead(self, dict):
        self.datalist.put(self.jsonProcessing(dict))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def updateHeadEvent(self, dict):
        if dict.get("code") == 1000:
            self.friendListClass.changeOwnInfo(headscul=dict.get("filepath"))
            #QMessageBox.information(None, "成功",
            #                        "修改成功", QMessageBox.Yes)
        else:
            QMessageBox.warning(None, "警告",
                                "修改失败", QMessageBox.Yes)

    def getFile(self, filepath):
        dictData = dict(msgType=Protocol.Protocol.GETFILE, filepath=filepath)
        self.datalist.put(self.jsonProcessing(dictData))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def setGroup(self, dict, setgroupclass):
        self.setGroupClass = setgroupclass
        self.datalist.put(self.jsonProcessing(dict))
        print(dict)
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def setGroupMembers(self, dict):
        if dict.get("code") == 1000:
            groupid = dict.get("groupid")
            self.groupChatClasses.get(groupid).setGroupMembersSignal.emit(dict)

    def setGroupEvent(self, dict):
        self.setGroupClass.resultSignal.emit(dict.get("code"))

    def getGroupsEvent(self, dict):
        self.friendListClass.startUpGroupNodes.emit(dict)

    def changeStatus(self, dict):
        self.datalist.put(self.jsonProcessing(dict))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def sendGroupFile(self, dict, groupFileClass):
        self.datalist.put(self.jsonProcessing(dict))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def sendGroupFileEvent(self, dict):
        if dict.get("code") == 1000:
            groupid = dict.get("groupid")
            self.groupFileClasses.get(groupid).uploadSignal.emit(dict)

    def getGroupFile(self, dict, groupFileClass):
        target = dict.get("groupid")
        if not self.groupFileClasses.__contains__(target):
            self.groupFileClasses[target] = groupFileClass

        self.datalist.put(self.jsonProcessing(dict))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def getGroupFileEvent(self, dict):
        target = dict.get("groupid")
        fileClass = self.groupFileClasses.get(target)
        fileClass.getFileSignal.emit(dict.get("files"))

    def downloadGroupFile(self, dict):
        self.datalist.put(self.jsonProcessing(dict))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def downloadGroupFileEvent(self, dict):
        groupid = dict.get("groupid")
        if self.groupFileClasses.__contains__(groupid):
            self.groupFileClasses.get(groupid).downloadSignal.emit(dict)

    def groupLogin(self, dict):
        groupid = dict.get("groupid")
        if self.groupChatClasses.__contains__(groupid):
            groupclass = self.groupChatClasses.get(groupid)
            for count in range(groupclass.groupMemberList.count()):
                item = groupclass.groupMemberList.item(count)
                if item.member_account == dict.get("account"):
                    item.changeLoginState(dict.get("flag"))

    def saveProfile(self, dict, profileClass):
        self.profileClass = profileClass
        self.datalist.put(self.jsonProcessing(dict))
        self.epoll_fd.modify(
            self.p.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def saveProfileEvent(self, dict):
        self.profileClass.resultSignal.emit(dict.get("code"))
        if dict.get("code") == 1000:
            self.friendListClass.changeOwnInfo(nickname=dict.get(
                "nickname"), signature=dict.get("signature"))
            #QMessageBox.information(None, "成功",
            #                        "修改成功", QMessageBox.Yes)
        else:
            QMessageBox.warning(None, "警告",
                                "修改失败", QMessageBox.Yes)

    def setAdminClass(self, adminClass):
        self.adminClass = adminClass

    def adminUserLoginMessage(self, dict):
        if self.usertype:
            self.adminClass.userLoginSignal.emit(dict)

    def adminUserLogoutMessage(self, dict):
        if self.usertype:
            self.adminClass.userLogoutSignal.emit(dict)

    def adminForcedOffline(self):
        self.datalist.put(self.jsonProcessing(
            {"nihao": "fuckyou!!!!!!!!!!!!!!!!"}))
        self.epoll_fd.modify(self.p.fileno(), select.EPOLLIN |
                             select.EPOLLOUT | select.EPOLLERR | select.EPOLLHUP)

    def initAdminListEvent(self, dict):
        self.adminClass.adminLoginSignal.emit(dict)       


    def __del__(self):
        self.p.close()

    def jsonProcessing(self, data):
        return json.dumps(data, cls=Protocol.DateEncoder)
