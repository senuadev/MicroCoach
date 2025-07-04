from flask import render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash  # For local hashing if needed
from . import auth_bp
from ..extensions import supabase


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form.get('username')

        sb = supabase.client
        try:
            response = sb.auth.sign_up({
                'email': email,
                'password': password,
                'options': {
                    'data': {'username': username}
                }
            })
            # Check if response contains user data
            if hasattr(response, 'user') and response.user:
                flash('Registration successful. Please check your email to confirm.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Registration failed - no user data returned', 'danger')
        except Exception as e:
            flash(f'Registration error: {str(e)}', 'danger')
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sb = supabase.client
        try:
            response = sb.auth.sign_in_with_password({
                'email': email,
                'password': password,
            })
            if hasattr(response, 'session') and hasattr(response, 'user'):
                session['user'] = response.user.dict()  # Convert user object to dict
                session['access_token'] = response.session.access_token
                flash('Logged in successfully', 'success')
                return redirect(url_for('dashboard.index'))
            else:
                flash('Login failed - invalid response from server', 'danger')
        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    access_token = session.get('access_token')
    if access_token:
        try:
            supabase.client.auth.sign_out()
        except Exception:
            pass
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))
