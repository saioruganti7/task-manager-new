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
