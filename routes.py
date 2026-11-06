from datetime import date
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ...extensions import db
from ...models import Task
bp = Blueprint('tasks',__name__,url_prefix='/api/tasks')
PRIORITIES={'low','medium','high'}

def owned(task_id): return Task.query.filter_by(id=task_id,user_id=current_user.id).first()

def validate(data,task):
    if 'title' in data:
        title=str(data['title']).strip()
        if not title or len(title)>200: return 'Title must contain 1–200 characters'
        task.title=title
    if 'description' in data: task.description=str(data['description'] or '')
    if 'priority' in data:
        if data['priority'] not in PRIORITIES: return 'Invalid priority'
        task.priority=data['priority']
    if 'due_date' in data:
        try: task.due_date=date.fromisoformat(data['due_date']) if data['due_date'] else None
        except (ValueError,TypeError): return 'Use YYYY-MM-DD for due_date'
    return None

@bp.get('')
@login_required
def list_tasks():
    q=Task.query.filter_by(user_id=current_user.id)
    search=request.args.get('search','').strip()
    if search: q=q.filter(Task.title.ilike(f'%{search}%'))
    return jsonify(tasks=[t.to_dict() for t in q.order_by(Task.created_at.desc()).all()])

@bp.post('')
@login_required
def create_task():
    data=request.get_json(silent=True) or {}
    task=Task(user_id=current_user.id,title='')
    error=validate(data,task)
    if error or not task.title: return jsonify(error=error or 'Title required'),400
    db.session.add(task);db.session.commit();return jsonify(task=task.to_dict()),201

@bp.get('/<int:task_id>')
@login_required
def get_task(task_id):
    task=owned(task_id)
    return (jsonify(task=task.to_dict()) if task else (jsonify(error='Not found'),404))

@bp.patch('/<int:task_id>')
@login_required
def update_task(task_id):
    task=owned(task_id)
    if not task: return jsonify(error='Not found'),404
    error=validate(request.get_json(silent=True) or {},task)
    if error: return jsonify(error=error),400
    db.session.commit();return jsonify(task=task.to_dict())

@bp.delete('/<int:task_id>')
@login_required
def delete_task(task_id):
    task=owned(task_id)
    if not task: return jsonify(error='Not found'),404
    db.session.delete(task);db.session.commit();return '',204
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
