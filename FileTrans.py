from pickletools import optimize
from queue import Queue
import socket
from PIL import Image
import os
import struct
import Protocol
import shutil


class FileSocket:
    def __init__(self) -> None:
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ("49.232.147.37", 8081)
        self.waitFile = []
        self.process = {}
        self.filequeue = Queue()

    def start(self, fd):
        self.clientSocket.connect(self.address)
        self.sendThread = Protocol.KThread(target=self.initSendTask, args=(fd,))
        self.recvThread = Protocol.KThread(target=self.initRecvTask)
        self.sendThread.start()
        self.recvThread.start()

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
                print('file new name is {0}, filesize if {1}'.format(
                    str(fn), filesize))
                recvd_size = 0  # 定义已接收文件的大小
                # 存储在该脚本所在目录下面
                dir = str(fn).split("/")
                path = '/'.join(dir[:-1])
                if not os.path.exists(path):
                    os.mkdir(path)                       # 创建路径

                fp = open('./' + str(fn), 'wb')
                print('start receiving...')
                self.process[fn] = 0
                # 将分批次传输的二进制流依次写入到文件
                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = self.clientSocket.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = self.clientSocket.recv(filesize - recvd_size)
                        recvd_size = filesize
                    fp.write(data)
                    self.process[fn] = round(recvd_size/filesize, 4)
                #传输完成后fn加入完成队列，等待操作
                self.waitFile.append(fn)
                fp.close()
                print("传输完成")

    def initSendTask(self, fd):
        self.clientSocket.send(str(fd).encode())
        while True:
            print("阻塞")
            path = self.filequeue.get()
            print(path)
            if path == "close":
                self.clientSocket.send(path.encode())
                break
            if os.path.isfile(path):
                try:
                    fp = open(path, "rb")
                    bytes = fp.read()

                    fhead = struct.pack(
                        '128sl', path.encode('utf-8'), len(bytes))
                    self.clientSocket.send(fhead)

                    chunks, chunk_size = len(bytes), 1024
                    list = [bytes[i:i+chunk_size]
                            for i in range(0, chunks, chunk_size)]
                    for i in list:
                        print(len(i))
                        self.clientSocket.send(i)
                except Exception as e:
                    print(e)
                    break


    def putFilePath(self, path):
        self.filequeue.put(path)
        print(self.filequeue.qsize())

    def copyImgIntoTemp(self, path, compress=False):
        img = Image.open(path, mode="r")
        unique_hash = hash(str(img))

        if compress:
            if img.format == "PNG":
                img = img.convert("RGB")
                img.format = "JPEG"
            newFileName = "temp/%s.%s" % (unique_hash, img.format)
            img.save(newFileName, quality = 10, optimize=True)
        else:
            newFileName = "temp/%s.%s" % (unique_hash, img.format)
            img.save(newFileName)

        return newFileName

    def copyFileIntoTemp(self, path, groupid = None):
        if groupid:
            dstpath = "temp/%s/" % groupid
            #dstpath = "temp/"
        else:
            dstpath = "temp/"
        if not os.path.isfile(path):
            print ("%s not exist!"%(path))
        else:
            fpath,fname=os.path.split(path)             # 分离文件名和路径
            if not os.path.exists(dstpath):
                os.makedirs(dstpath)                       # 创建路径
            shutil.copy(path, dstpath + fname)          # 复制文件

        return dstpath + fname

    def fileIsRecived(self, path):
        if path in self.waitFile:
            self.waitFile.remove(path)
            return True
        else:
            return False

    def getFileProcess(self, path):
        return self.process.get(path)


    def closeTrans(self, type):
        if not type:
            self.sendThread.kill()
            self.recvThread.kill()
            self.clientSocket.shutdown(2)
            self.putFilePath("close")
            self.clientSocket.close()
