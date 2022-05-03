import tkinter
import threading
import client
import tkinter.messagebox

class Chat_w:
    def __init__(self, friendName, win):
        self.chat = client.Chat(friendName)
        self.friendName = friendName
        self.win = tkinter.Toplevel(win)
        self.send = tkinter.Variable()
        self.text = tkinter.Text(self.win, height=10, width=40)

    def sendMail(self):
        msg = self.chat.sendMail(self.send.get())
        self.text.insert(tkinter.INSERT, msg)

    def gethistory(self):
        msg = self.chat.gethistory()
        print(msg)
        self.text.insert(tkinter.INSERT, msg)
        return

    def getInfo(self):
        print('getInfo……')
        while True:
            msg = self.chat.getInfo()
            print(msg)
            self.text.insert(tkinter.INSERT, msg)

    def window(self):
        print('Chat Window')
        self.win.title(self.friendName)
        self.win.geometry("400x300+300+200")
        self.text.grid(row=4, column=1)
        labelesend = tkinter.Label(self.win, text="发送的消息").grid(row=5, column=0)
        entrySend = tkinter.Entry(self.win, textvariable=self.send).grid(row=5, column=1)
        button2 = tkinter.Button(self.win, text="发送", command=self.sendMail).grid(row=6, column=2)
        self.gethistory()
        # self.getInfo()
        t = threading.Thread(target=self.getInfo)
        t.start()
        self.win.mainloop()

class Friend_w:
    def __init__(self, userName, win):
        self.__friend = client.Friend(userName)
        self.__userName = userName
        self.__friends = []
        self.__win = tkinter.Toplevel(win)
        self.__friendName = tkinter.Variable()
        self.__j = 0
        self.__name = tkinter.Variable()

    def chat(self):
        print('chat with friend……')
        if self.__friend.isFriend(self.__friendName.get()):
            chat = Chat_w(self.__friendName.get(), self.__win)
            chat.window()
        else:
            tkinter.messagebox.showerror('错误！', '好友昵称错误!')

    def group(self):
        print('chat in group')
        chat = Chat_w('群聊', self.__win)
        chat.window()

    def getFriends(self):
        print('get friend……')
        self.__friends = self.__friend.getFriends()

    def addFriend(self):
        print('add friend……')
        err = self.__friend.addfriend(self.__name.get())
        tkinter.messagebox.showinfo('提示', err, parent = self.__win)
        if err == '添加成功！':
            self.draw()

    def draw(self):
        print('draw friend window……')
        self.getFriends()
        self.__j = 0
        for i in self.__friends:
            self.__j = self.__j + 1
            labeltext= tkinter.Label(self.__win, text=i).grid(row=self.__j, column=0)
        labelUse = tkinter.Label(self.__win, text="好友昵称：").grid(row=self.__j + 1, column=0)
        entryUser = tkinter.Entry(self.__win, textvariable=self.__friendName).grid(row=self.__j + 1, column=1) 
        button = tkinter.Button(self.__win, text="聊天", command=self.chat).grid(row=self.__j + 1, column=3)
        button = tkinter.Button(self.__win, text="群聊", command=self.group).grid(row=self.__j + 2, column=1)
        labelUse = tkinter.Label(self.__win, text="昵称：").grid(row=self.__j + 3, column=0)
        entryUser = tkinter.Entry(self.__win, textvariable=self.__name).grid(row=self.__j + 3, column=1) 
        button = tkinter.Button(self.__win, text="添加好友", command=self.addFriend).grid(row=self.__j + 3, column=3)
        
    def friendWindow(self):
        self.__win.title("好友列表")
        self.__win.geometry("400x300+300+200")
        self.draw()
        self.__win.mainloop()

class Index:
    def __init__(self):
        # 窗口
        self.__index = client.Index()
        self.__win = tkinter.Tk()
        self.__user = tkinter.Variable()
        self.__password = tkinter.Variable()

    def logIn(self):
        msg = self.__index.logIn(self.__user.get(), self.__password.get())
        self.errSend(msg[1])
        if msg[0] == '1':
            friend = Friend_w(self.__user.get(), self.__win)
            friend.friendWindow()
   
    # 发送提示信息
    def errSend(self, err):
        tkinter.messagebox.showwarning('提示', err, parent = self.__win)
        # self.errBox.insert(tkinter.INSERT, err)

    def loginwindow(self):
        self.__win.title("登录")
        self.__win.geometry("400x300+300+200")
        labelUse = tkinter.Label(self.__win, text="userName").grid(row=2, column=0)
        entryUser = tkinter.Entry(self.__win, textvariable=self.__user).grid(row=2, column=1)
        labelPassword = tkinter.Label(self.__win, text="password").grid(row=3, column=0)
        entryPassword = tkinter.Entry(self.__win, textvariable=self.__password).grid(row=3, column=1)
        button = tkinter.Button(self.__win, text="登录", command=self.logIn).grid(row=4, column=1)
        self.__win.mainloop()
index = Index()
index.loginwindow()

