# !/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import time
import hashlib
from flask import Flask, request, abort, Response
from configparser import ConfigParser
from dbutils.pooled_db import PooledDB

app = Flask(__name__)
cp = ConfigParser()
cp.read('/config/restdb.cfg')
POOL = PooledDB(
    creator=pymysql,
    maxconnections=8,
    mincached=2,
    maxcached=4,
    maxshared=1,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    host=cp.get('mysql', 'host'),
    port=int(cp.get('mysql', 'port')),
    user=cp.get('mysql', 'username'),
    password=cp.get('mysql', 'password'),
    database=cp.get('mysql', 'db'),
    charset='utf8'
)
host = cp.get('main', 'host')
port = int(cp.get('main', 'port'))
debug = ("1" == cp.get('main', 'debug'))
mainpw = cp.get('main', 'password')


@app.route('/', methods=['post', 'get'])
def usage():
    abort(Response('https://github.com/RyoLee/restdb'))


@app.route('/ping', methods=['post', 'get'])
def ping():
    return 'pong'


@app.route('/set', methods=['post'])
def setValue():
    conn = POOL.connection()
    cursor = conn.cursor()
    key = request.form.to_dict()["key"]
    value = request.form.to_dict()["value"]
    pw = request.form.to_dict()["password"]
    token = request.form.to_dict()["token"]
    ts = int(time.time())
    count = cursor.execute("select p from data where k=%s", (key))
    if 1 == count:
        p = cursor.fetchone()
        if token in getTokens(p, ts) or token in getTokens(mainpw, ts):
            cursor.execute(
                "update data set v=%s,p=%s where k=%s", (value, pw, key))
            conn.commit()
            cursor.close()
            conn.close()
            return 'Done'
        else:
            cursor.close()
            conn.close()
            abort(403)
    else:
        if token in getTokens(mainpw, ts):
            cursor.execute(
                "insert into data(k,v,p) values(%s,%s,%s)", (key, value, pw))
            conn.commit()
            cursor.close()
            conn.close()
            return 'Done'
        else:
            cursor.close()
            conn.close()
            abort(403)


@app.route('/get', methods=['post'])
def getValue():
    conn = POOL.connection()
    cursor = conn.cursor()
    key = request.form.to_dict()["key"]
    token = request.form.to_dict()["token"]
    ts = int(time.time())
    count = cursor.execute("select v,p from data where k=%s", (key))
    if 1 == count:
        v, p = cursor.fetchone()
        conn.close()
        cursor.close()
        if token in getTokens(p, ts):
            return v
        else:
            abort(403)
    else:
        cursor.close()
        conn.close()
        abort(404)


def getTokens(p, t):
    t0 = t//30-1
    res = []
    for i in range(3):
        m = hashlib.md5()
        m.update(bytes(str(t0+i)+p, encoding='utf-8'))
        tmp = m.hexdigest()
        res.append(tmp)
    return res


if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)
