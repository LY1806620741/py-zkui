from flask import (
    Blueprint, request
)
from flaskr.auth import api_need_login
from flaskr.db import get_db

bp = Blueprint('config', __name__, url_prefix='/config')


@bp.route('/node', methods=('GET', 'POST'))
@api_need_login
def ZKnode():
    if (request.method=="GET"):
        db = get_db()
        nodes = db.execute(
            'SELECT value FROM config where key="nodes"'
        ).fetchone()
        if nodes is not None:
            return nodes[0]
        else:
            return ''
    elif (request.method == 'POST'):
        #curl -X POST localhost:5000/config/node -d "nodes='1.1.1.1:1'&nodes='2.2.2.2:2'"
        #axios
        data=request.get_json(silent=True)
        if 'nodes' in data:
            db = get_db()
            db.execute(
                'REPLACE INTO config (key, value) VALUES ("nodes",?)',(",".join(data['nodes']),)
            )
            db.commit()
            return '',200
        else:
            return '',400