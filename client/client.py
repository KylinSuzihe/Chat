import tkinter
import socket
import threading
import time

ip = '127.0.0.1'
port = 8080
ck = None 
class Chat:
    def __init__(self, friendName):
        self.__friendName = friendName
        # t = threading.Thread(target=self.getInfo)
        # t.start()
        self.__msg = ''

    def getInfo(self):
        print('client getInfo……')
        # while True:
        data = ck.recv(1024)#用于接受服务器发送的信息
        massage = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'
        massage += data.decode('utf-8')
        self.__msg = massage
        return self.__msg
    
    def sendMail(self, sendStr):     
        send = str(self.__friendName) + ":" + sendStr + "\n"
        ck.send(send.encode('utf-8'))
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'+'我：\n' + sendStr +'\n'

    def gethistory(self):
        print('Get history')
        ck.send(('gh:' + self.__friendName).encode('utf-8'))
        print('-------', self.__friendName)
        data = ck.recv(1024).decode('utf-8')
        print('history:', data)
        return data

  
class Friend:
    def __init__(self, userName):
        self.__userName = userName
        self.__friends = []

    def addfriend(self, friendName):
        if friendName in self.__friends:
            return '该好友已存在'
        ck.send(('ad:' + friendName).encode('utf-8'))
        err = ck.recv(1024).decode('utf-8')
        return err

    def getFriends(self):
        print('client: getFriends')
        ck.send('gf'.encode('utf-8'))
        self.__friends = ck.recv(1024).decode('utf-8').split(':')
        print(self.__friends)
        return self.__friends
    
    def isFriend(self, friendName):
        return friendName in self.__friends

class Index:
    def __init__(self):
        self.connectServer()

    # 建立连接
    def connectServer(self):
        global ck
        clie = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socked所准守ipv4相关协议
        clie.connect((ip, int(port)))#连接服务器
        ck = clie
        # t = threading.Thread(target=Chat.getInfo)
        # t.start()

    # 登录
    def logIn(self, user, password):
        print('To LogIn……')
        # 信息读入
        ck.send((user + ':' + password).encode('utf-8'))
        msg = ck.recv(1024).decode('utf-8').split(':')
        return msg


