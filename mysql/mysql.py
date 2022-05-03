from sqlite3 import Row
from unittest import result
import pymysql
import time

conn = pymysql.connect(host='', port=3306, user='', passwd='', database='')
cursor = conn.cursor()

# 根据用户名查询用户
def getUserByName(userName):
    row = cursor.execute('select * from user where name = "%s"' % userName)
    resultList = cursor.fetchall()
    return row, resultList

# 根据用户id查询其好友
def getFriends(userName):
    row = cursor.execute('select user_2 from friend where user_1 = "%s"' % userName)
    resultList = cursor.fetchall()
    return resultList

# 查看消息记录
def getHistory(sendId, acceptId, is_read):
    row = cursor.execute('select content, time from history \
                        where send = "%s" and accept = "%s" and is_read = %s' % (sendId, acceptId, is_read))
    resultList = cursor.fetchall()
    cursor.execute('UPDATE HISTORY SET is_read = 1 WHERE send = "%s" AND accept = "%s"' % (sendId, acceptId))
    conn.commit()
    return resultList

# 加入新用户
def insertUser(userName, password):
    try:
        row = cursor.execute('INSERT INTO USER(NAME, PASSWORD) VALUES("%s", "%s")' % (userName, password))
        conn.commit()
        return 1
    except:
        conn.rollback()
        return 0

def saveHistory(send, accept, msg, is_read):
    try:
        tim = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sql = 'INSERT INTO HISTORY (send, accept, content, TIME, is_read) \
                VALUES ("%s", "%s", "%s", "%s", %s)' % (send, accept, msg, tim, is_read)
        row = cursor.execute(sql)
        conn.commit()
        return 1
    except:
        conn.rollback()
        return 0

def addFriend(user_1, user_2):
    try:
        cursor.execute('INSERT INTO friend(user_1, user_2) VALUES ("%s", "%s")' % (user_1, user_2))
        conn.commit()
        cursor.execute('INSERT INTO friend(user_1, user_2) VALUES ("%s", "%s")' % (user_2, user_1))
        conn.commit()
        return 1
    except:
        conn.rollback()
        return 0

