from flask import g
from kazoo.client import KazooClient,KazooState
from flaskr.db import get_db

zk=None

def get_zk():
    global zk
    if zk==None:
        connect()
        return zk
    else:
        if zk.state==KazooState.CONNECTED:
            return zk
        else:
            connect()
            return zk

def connect():
    global zk 
    db=get_db()
    nodes = db.execute(
            'SELECT value FROM config where key="nodes"'
        ).fetchone()
    if nodes is not None:
        #localhost:2181
        zk=KazooClient(hosts=nodes[0],timeout=2.0)
        zk.start()

def close_zk(e=None):
    if zk is not None:
        zk.stop()
