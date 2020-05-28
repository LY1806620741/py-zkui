from flask import (
    Blueprint,g,request
)
from flaskr.auth import api_need_login
from flaskr.zk import get_zk

bp = Blueprint('zookeeper', __name__, url_prefix='/zookeeper')

@bp.route('/status', methods=['GET'])
@api_need_login
def status():
    zk=get_zk()
    if zk is None:
        return 'disconnect'
    else:
        return zk.state

def check_command(key):
    return key in request.args and request.args.get(key) is not None

@bp.route('/command', methods=['GET'])
@api_need_login
def command():
    if check_command("ls"):
        return str(get_zk().get_children(request.args.get("ls")))
    elif check_command('get'):
        data,stat =get_zk().get(request.args.get("get"))
        return '['+'"'+request.args.get("get")+'",'+('null' if data is None else '"'+data.decode("utf-8").replace("\"","\\\"")+'"')+','+str(stat._asdict())+']'
    elif check_command('set'):
        kv=request.args.get("set").split("=",1)
        if len(kv)==2:
            print(kv,kv[1].encode())
            return str(get_zk().set(kv[0], kv[1].encode()))
    elif check_command('create'):
        kv=request.args.get("create").split("=",1)
        if len(kv)==2:
            return str(get_zk().create(kv[0], kv[1].encode()))
        else:
            return str(get_zk().create(kv[0]))
    elif check_command('del'):
        get_zk().delete(request.args.get("del"),recursive=True)
        return ''
    return '',500
    # return 'false'