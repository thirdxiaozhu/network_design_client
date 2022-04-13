from http import client
from pydoc import cli
import FileTrans

client = FileTrans.FileSocket()
client.start()

while True:
    path = input()
    client.putFilePath(path)