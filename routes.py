from collections import Counter
from datetime import date, timedelta
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from ...models import Task
bp=Blueprint('dashboard',__name__,url_prefix='/api/dashboard')

def mine():return Task.query.filter_by(user_id=current_user.id).all()

@bp.get('/summary')
@login_required
def summary():
    tasks=mine(); counts=Counter(t.status for t in tasks);total=len(tasks)
    overdue=sum(bool(t.due_date and t.due_date<date.today() and t.status!='completed') for t in tasks)
    return jsonify(total=total,pending=counts['pending'],in_progress=counts['in_progress'],completed=counts['completed'],overdue=overdue,completion_percentage=round(100*counts['completed']/total,1) if total else 0)

@bp.get('/priorities')
@login_required
def priorities():return jsonify(counts=dict(Counter(t.priority for t in mine())))

@bp.get('/weekly')
@login_required
def weekly():
    today=date.today();days=[today-timedelta(days=i) for i in range(6,-1,-1)];tasks=mine()
    return jsonify(days=[{'date':day.isoformat(),'completed':sum(bool(t.completed_at and t.completed_at.date()==day) for t in tasks)} for day in days])

@bp.get('/recent')
@login_required
def recent():
    tasks=sorted(mine(),key=lambda t:t.updated_at,reverse=True)[:5]
    return jsonify(tasks=[t.to_dict() for t in tasks])
