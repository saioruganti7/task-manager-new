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
