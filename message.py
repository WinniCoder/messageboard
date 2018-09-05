#!/usr/bin/env python
# encoding: utf-8
"""
@author: winnihwu
@software: PyCharm
@time: 2018/8/20 15:47
"""

from flask import Flask, request
import pymysql
import json
import datetime
import sys

app = Flask(__name__)

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '130523',
    'db': 'message_board',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


@app.route('/all_msg')
def get_msgs():
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM msgs ORDER BY date'
            cursor.execute(sql)
            msgs = cursor.fetchall()
        conn.commit()
    finally:
        conn.close()
    count = len(msgs)
    for i in range(count):
        msgs[i]['level'] = i + 1
    result = {'count': count, 'data': msgs}
    return json.dumps(result, default=str)


@app.route('/add_msg', methods=['POST'])
def add_msg():
    # data = {
    #     "author": "yahui",
    #     "body": "message"
    # }
    msg = request.get_json()
    # print(msg)
    # data = json.loads(msg)
    data = msg
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cursor:
            sql1 = "INSERT INTO msgs(body,author,date) VALUES ('%s','%s','%s')" \
                   % (data['body'], data['author'], date)
            print(sql1)
            cursor.execute(sql1)

            sql2 = 'SELECT COUNT(*) as num FROM msgs'
            cursor.execute(sql2)
            count = cursor.fetchone()
            level = count['num']
        conn.commit()
    except:
        ex = sys.exc_info()
        print("Unexpected error:", ex[1])
        conn.rollback()
        result = {
            "status": 1,
            "msg": "add fail",
            "data": data
        }
        return json.dumps(result)
    finally:
        conn.close()
    result = {
        "status": 0,
        "msg": "OK",
        "data": {
            "level": level,
            "date": date
        }
    }
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
