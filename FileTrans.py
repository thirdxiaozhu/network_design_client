from queue import Queue
import socket
from PIL import Image
import os
import struct
import Protocol

class FileSocket:
    def __init__(self) -> None:
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ("49.232.147.37", 8081)
        self.filequeue = Queue()


    def start(self):
        self.clientSocket.connect(self.address)
        thread = Protocol.KThread(target=self.initTask)
        thread.start()

    def initTask(self):
        #imgName = "/home/jiaxv/Pictures/Untitled.png"
        while True:
            print("阻塞")
            imgName = self.filequeue.get()
            if imgName == "close":
                self.clientSocket.send(imgName.encode())
                print(imgName.encode())
                break
            if os.path.isfile(imgName):
                try:
                    # 定义文件头信息，包含文件名和文件大小
                    img = Image.open(imgName, mode="r")
                    unique_hash = hash(str(img))
                    newFileName = "temp/%s.%s" % (unique_hash, img.format)
                    img.save(newFileName)

                    fp = open(newFileName, "rb")
                    bytes = fp.read()

                    fhead = struct.pack('128sl', newFileName.encode('utf-8'), len(bytes))
                    self.clientSocket.send(fhead)

                    chunks, chunk_size = len(bytes), 1024
                    list = [bytes[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
                    for i in list:
                        print(len(i))
                        self.clientSocket.send(i)
                except Exception as e:
                    print(e)
                    break
                
        self.clientSocket.shutdown(2)
        self.clientSocket.close()
        print("连接已断开")

    def putFilePath(self, path):
        self.filequeue.put(path)
        print(self.filequeue.qsize())

    def closeTrans(self):
        self.putFilePath("close")
