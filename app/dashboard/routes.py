from flask import render_template, session, redirect, url_for, flash
from . import dashboard_bp
from ..extensions import supabase


def login_required(func):
    from functools import wraps

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return decorated_view


# app/dashboard/routes.py
@dashboard_bp.route('/')
@login_required
def index():
    user = session['user']
    
    # Get user's achievements
    achievements = supabase.client.table('achievements') \
        .select('*') \
        .eq('user_id', user['id']) \
        .order('created_at', desc=True) \
        .limit(5) \
        .execute()
    
    # Calculate total points
    total_points = sum(a['points'] for a in achievements.data) if achievements.data else 0
    
    stats = {
        'total_points': total_points,
        'recent_achievements': achievements.data[:3],  # Show only 3 most recent
        'lessons_completed': 5,  # You'll need to calculate this from progress
        'total_lessons': 15,
        'day_streak': 0,
        'completion_rate': 33,
        'achievements_earned': len(achievements.data) if achievements.data else 0,
        'recent_lessons': [
            {'title': '1000 Python Examples', 'duration': '15 min', 'status': 'Completed'},
            {'title': 'Flask Web Development', 'duration': '30 min', 'status': 'In Progress'},
        ]
    }
    return render_template('dashboard/index.html', stats=stats)