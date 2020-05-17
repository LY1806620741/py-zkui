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

@bp.route('/command', methods=['GET'])
@api_need_login
def command():
    ls=request.args.get("ls")
    if (ls is not None):
        return str(get_zk().get_children(ls))
    # return 'false'