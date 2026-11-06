from datetime import date
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ...extensions import db
from ...models import Task, now
bp=Blueprint('tracking',__name__,url_prefix='/api')
STATUSES={'pending','in_progress','completed'}

@bp.patch('/tasks/<int:task_id>/status')
@login_required
def status(task_id):
    task=Task.query.filter_by(id=task_id,user_id=current_user.id).first()
    if not task:return jsonify(error='Not found'),404
    value=(request.get_json(silent=True) or {}).get('status')
    if value not in STATUSES:return jsonify(error='Invalid status'),400
    task.status=value
    task.completed_at=now() if value=='completed' else None
    db.session.commit();return jsonify(task=task.to_dict())

@bp.get('/tracking/upcoming')
@login_required
def upcoming():
    tasks=Task.query.filter(Task.user_id==current_user.id,Task.status!='completed',Task.due_date>=date.today()).order_by(Task.due_date).all()
    return jsonify(tasks=[t.to_dict() for t in tasks])

@bp.get('/tracking/overdue')
@login_required
def overdue():
    tasks=Task.query.filter(Task.user_id==current_user.id,Task.status!='completed',Task.due_date<date.today()).order_by(Task.due_date).all()
    return jsonify(tasks=[t.to_dict() for t in tasks])

@bp.get('/tracking/calendar')
@login_required
def calendar():
    tasks=Task.query.filter(Task.user_id==current_user.id,Task.due_date.isnot(None)).order_by(Task.due_date).all()
    return jsonify(tasks=[t.to_dict() for t in tasks])
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from ...extensions import db
from ...models import User
bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.post('/register')
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get('name','')).strip()
    email = str(data.get('email','')).strip().lower()
    password = str(data.get('password',''))
    if not name or '@' not in email or len(password) < 8:
        return jsonify(error='Name, valid email, and password (8+ characters) required'), 400
    if User.query.filter_by(email=email).first(): return jsonify(error='Email already registered'), 409
    user = User(name=name,email=email)
    user.set_password(password)
    db.session.add(user); db.session.commit()
    login_user(user)
    return jsonify(user=user.to_dict()), 201

@bp.post('/login')
def login():
    data = request.get_json(silent=True) or {}
    user = User.query.filter_by(email=str(data.get('email','')).strip().lower()).first()
    if not user or not user.check_password(str(data.get('password',''))):
        return jsonify(error='Invalid email or password'), 401
    login_user(user)
    return jsonify(user=user.to_dict())

@bp.post('/logout')
@login_required
def logout():
    logout_user(); return jsonify(message='Logged out')

@bp.get('/me')
@login_required
def me(): return jsonify(user=current_user.to_dict())

@bp.patch('/profile')
@login_required
def profile():
    data = request.get_json(silent=True) or {}
    name = str(data.get('name','')).strip()
    if not name: return jsonify(error='Name required'),400
    current_user.name = name; db.session.commit()
    return jsonify(user=current_user.to_dict())
