# routes facing the clients (dashboard, airport info)

from flask import Blueprint, render_template

from database.db import get_db
from routes import login_required

bp = Blueprint('client', __name__)


@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('client/dashboard.html')


@bp.route('/info')
def info():
    db = get_db()
    rows = db.execute('SELECT key, content, content_type FROM airport_content').fetchall()
    content = {row['key']: row for row in rows}
    return render_template('client/info.html', content=content)