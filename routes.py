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
