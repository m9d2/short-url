import uvicorn
from fastapi import FastAPI
import sqlite3
import time
import random
import string
import configparser
from starlette.responses import RedirectResponse

app = FastAPI()
conn = sqlite3.connect('short_url.db', check_same_thread=False)
cf = configparser.ConfigParser()
cf.read("config.ini")
secs = cf.sections()

host = cf.get("Host", "host")


@app.get("/{code}")
def read_root(code: str):
    sql = "select url from short_url where code = '{}'".format(code)
    c = conn.cursor()
    cursor = c.execute(sql).fetchall()
    if cursor.__len__() < 1:
        return {"code": 1001, "message": "The code is invalid"}
    if cursor.__len__() == 1:
        url = cursor[0][0]
        response = RedirectResponse(url=url)
        return response
    else:
        return {"code": 1000, "message": "System error"}


@app.get("/")
def read_root(u: str):
    code = insert(u)
    return {"code": 200, "message": "success", "data": host + code}


@app.get("/sys/init")
def read_root():
    c = conn.cursor()
    sql = "create table short_url (id integer primary key autoincrement not null, code text not null, " \
          "url text not null, create_time text not null, ip_address text)"
    c.execute(sql)
    conn.commit()
    conn.close()
    return {"code": 200, "message": "success"}


def insert(url):
    code = generate_random_str()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c = conn.cursor()
    sql = "insert into short_url (id, code, url, create_time, ip_address) " \
          "values (null, '{}', '{}', '{}', null)".format(code, url, time_str)
    c.execute(sql)
    conn.commit()
    return code


def generate_random_str(length=4):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    while True:
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(length)]
        random_str = ''.join(str_list)
        if checkCode(random_str):
            return random_str


def checkCode(code):
    """
    校验code是否可用
    :param code:
    :return: True: 可用 False: 不可用
    """
    sql = "select id from short_url where code = '{}'".format(code)
    c = conn.cursor()
    c.execute(sql)
    cursor = c.fetchall()
    if cursor.__len__() < 1:
        return True
    return False


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)
