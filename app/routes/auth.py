from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import User, db
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        is_notary = 'is_notary' in request.form

        #input validation
        if not email or not username or not password:
            flash('Please fill out all fields', 'error')
            return redirect(url_for('auth.register'))
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(email=email, username=username, is_notary=is_notary)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')   
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('document.dashboard'))
        flash('Invalid email or password', 'error') 
        return redirect(url_for('auth.login'))
    return render_template('login.html')
    
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!')
    return redirect(url_for('auth.login')) 
