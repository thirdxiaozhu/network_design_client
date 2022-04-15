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


    def start(self, fd):
        self.clientSocket.connect(self.address)
        sendThread = Protocol.KThread(target=self.initSendTask, args=(fd,))
        recvThread = Protocol.KThread(target=self.initRecvTask)
        sendThread.start()
        recvThread.start()

    def initRecvTask(self):
        while True:
            fileinfo_size = struct.calcsize('128sl')
            # 接收文件名与文件大小信息
            buf = self.clientSocket.recv(fileinfo_size)
            print(buf)
            if buf == "close".encode():
                break
            
            if buf:
                filename, filesize = struct.unpack('128sl', buf)
                print(filesize)
                fn = filename.strip(b'\00')
                fn = fn.decode()
                print ('file new name is {0}, filesize if {1}'.format(str(fn),filesize))
                recvd_size = 0  # 定义已接收文件的大小
                # 存储在该脚本所在目录下面 
                fp = open('./' + str(fn), 'wb')
                print ('start receiving...')
                # 将分批次传输的二进制流依次写入到文件
                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = self.clientSocket.recv(1024)
                        recvd_size += len(data)
                        print(recvd_size)
                    else:
                        data = self.clientSocket.recv(filesize - recvd_size)
                        print(filesize - recvd_size)
                        print(len(data))
                        recvd_size = filesize
                    fp.write(data)
                fp.close()
                print("传输完成")

    def initSendTask(self, fd):
        self.clientSocket.send(str(fd).encode())
        while True:
            print("阻塞")
            path = self.filequeue.get()
            if path == "close":
                self.clientSocket.send(path.encode())
                break
            if os.path.isfile(path):
                try:
                    fp = open(path, "rb")
                    bytes = fp.read()

                    fhead = struct.pack('128sl', path.encode('utf-8'), len(bytes))
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

    def copyIntoTemp(self, path):
        img = Image.open(path, mode="r")
        unique_hash = hash(str(img))
        newFileName = "temp/%s.%s" % (unique_hash, img.format)
        img.save(newFileName)

        return newFileName


    def closeTrans(self):
        self.putFilePath("close")
