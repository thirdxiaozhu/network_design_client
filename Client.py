from copyreg import pickle
import json
from multiprocessing.connection import wait
import socket
from PyQt5.QtWidgets import *


class Client:
    def __init__(self):
        self.p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setupConnection(self, data):
        self.p.connect(('49.232.147.37', 8080))
        self.p.send(self.jsonProcessing(data).encode("utf-8"))
        msg = self.p.recv(1024)
        print(msg)
        msg = json.loads(msg.decode("utf-8"))
        return msg

    def registConnection(self, data):
        self.p.connect(('49.232.147.37', 8080))
        self.p.send(self.jsonProcessing(data).encode("utf-8"))
        msg = self.p.recv(1024)
        self.p.close()

        msg = json.loads(msg.decode("utf-8"))

        return msg.get("code")


    def addFriend(self, data):
        self.p.send(self.jsonProcessing(data).encode("utf-8"))
        msg = self.p.recv(1024)
        msg = json.loads(msg.decode("utf-8"))

        return msg.get("code")

    def searchFriend(self, data):
        self.p.send(self.jsonProcessing(data).encode("utf-8"))
        msg = self.p.recv(1024)
        msg = json.loads(msg.decode("utf-8"))

        return msg

    def getChatRecord(self, data):
        self.p.send(self.jsonProcessing(data).encode("utf-8"))
        msg = self.p.recv(1024)
        msg = json.loads(msg.decode("utf-8"))

        return msg

    def __del__(self):
        self.p.close()

    def jsonProcessing(self, data):
        return json.dumps(data)
