import functools
from flask import (
    Blueprint, render_template
)
from flaskr.auth import login_required

bp = Blueprint('index', __name__, url_prefix='/',static_folder="templates")

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    return bp.send_static_file('index.html')