import tkinter
import socket, threading
import sys
sys.path.append("d:\\Suzihe\\VSCode\\python\\chatting")
import mysql.mysql as mysql

win = tkinter.Tk()  # 创建主窗口
win.title('服务器')
win.geometry("400x300+200+20")
users = {}#用户字典，也可以连接数据库

def logIn(userName, password):
    exist, userList = mysql.getUserByName(userName)
    if exist == 1:
        if userList[0][2] == password:
            return 1, '1:登陆成功！\n'
        else:
            return 0, '0:用户名或密码错误！\n'
    else:
        if mysql.insertUser(userName, password):
            return 1, '1:登陆成功！\n'
        else:
            return 0, '0:注册失败！\n'

def toLogIn(connect):
    print('LogIn……')
    userName = ''
    while 1:
        loginData = connect.recv(1024).decode('utf-8').split(':')
        userName = loginData[0]
        password = loginData[1]
        b, msg = logIn(userName, password)
        connect.send(msg.encode('utf-8'))
        if b:
            break
    return userName

def getFriens(connect, userName):
    print('getFriends')
    friends = mysql.getFriends(userName)
    msg = ""
    for i in friends:
        msg += i[0]
        msg += ':'
    print('msg:', msg)
    connect.send(msg.encode('utf-8'))

def getHistory(connect, userName, friendName):
    print('Get History……')
    if friendName == '群聊':
        connect.send(('欢迎加入群聊！\n').encode('utf-8'))
        return
    hisList = mysql.getHistory(friendName, userName, 0)
    msg = '历史记录：\n'
    for i in hisList:
        strr = str(i[1]) + '\n' + friendName + ':\n' + i[0] + '\n'
        msg += strr
    connect.send(msg.encode('utf-8'))

def addFriend(connect, userName, friend):
    row, flist = mysql.getUserByName(friend)
    if row == 0:
        connect.send('该用户不存在！'.encode('utf-8'))
        return
    ok = mysql.addFriend(userName, friend)
    if ok:
        connect.send('添加成功！'.encode('utf-8'))
    else:
        connect.send('添加失败！'.encode('utf-8'))

def run(connect, addrss):
    userName = toLogIn(connect)
    users[userName] = connect 
    while True:
        rData = connect.recv(1024).decode("utf-8")
        infolist = rData.split(":")

        if infolist[0] == 'ad':
            addFriend(connect, userName, infolist[1])
            continue
        elif infolist[0] == 'gf':
            getFriens(connect, userName)
            continue
        elif infolist[0] == 'gh':
            getHistory(connect, userName, infolist[1])
            continue

        b = 0
        if infolist[0] in users:
            users[infolist[0]].send((userName + ":\n" + infolist[1]).encode("utf-8"))
            b = 1
        elif infolist[0] == '群聊':
            for i in users:
                if i == userName:
                    continue
                users[i].send((userName + ":\n" + infolist[1]).encode("utf-8"))
            b = 1
        mysql.saveHistory(userName, infolist[0], infolist[1], b)
            
#界面启动按钮连接的函数
def startSever():
    #启用一个线程开启服务器
    s = threading.Thread(target=start) 
    s.start()
#开启线程
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
def start():
    # socket嵌套字TCP的ipv4和相关协议
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #绑定ip和端口号
    server.bind(('127.0.0.1', 8080)) 
    #设置监听和连接的最大的数量
    server.listen(30) 
    #服务器启动信息显示在信息窗口中
    printStr = "服务器启动成功！\n" 
    text.insert(tkinter.INSERT, printStr) 
    #模拟服务器要一直运行所以使用死循环
    while True: 
    #接受所连接的客户端的信息
        connect, addrss = server.accept()
        #每连接一个客户端就开启一个线程
        t = threading.Thread(target=run, args=(connect, addrss))
        t.start()

button = tkinter.Button(win, text="启动", command=startSever).grid(row=5, column=1)
text = tkinter.Text(win, height=15, width=40)
labeltext = tkinter.Label(win, text='连接消息').grid(row=3, column=0)
text.grid(row=3, column=1)

win.mainloop()