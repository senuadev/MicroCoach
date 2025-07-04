from flask import render_template, session, redirect, url_for, flash
from supabase import Client
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
    
    # Fetch counts
    lessons_completed = supabase.client.table('progress').select('lesson_id', count='exact').eq('user_id', user['id']).eq('status', 'completed').execute().count or 0
    total_lessons = supabase.client.table('lessons').select('id', count='exact').execute().count or 0

    # Achievements and points
    achievements_resp = supabase.client.table('achievements').select('*').eq('user_id', user['id']).order('created_at', desc=True).execute()
    achievements_data = achievements_resp.data or []
    total_points = sum(a['points'] for a in achievements_data)

    # Completion rate
    completion_rate = int((lessons_completed / total_lessons) * 100) if total_lessons else 0

    # Recent lessons
    recent_lessons_resp = supabase.client.table('progress')\
        .select('lesson_id, timestamp')\
        .eq('user_id', user['id'])\
        .order('timestamp', desc=True)\
        .limit(5)\
        .execute()
    
    recent_lessons = []
    for rec in (recent_lessons_resp.data or []):
        try:
            lesson = supabase.client.table('lessons')\
                .select('title')\
                .eq('id', rec['lesson_id'])\
                .single()\
                .execute()
            if hasattr(lesson, 'data') and lesson.data:
                recent_lessons.append({
                    'title': lesson.data.get('title', 'Untitled Lesson'),
                    'duration': '—',
                    'status': 'Completed',
                    'timestamp': rec.get('timestamp')
                })
        except Exception as e:
            print(f"Error fetching lesson {rec.get('lesson_id')}: {str(e)}")
            continue

    stats = {
        'total_points': total_points,
        'recent_achievements': achievements_data[:3],
        'lessons_completed': lessons_completed,  
        'total_lessons': total_lessons,
        'day_streak': 0,
        'completion_rate': completion_rate,
        'achievements_earned': len(achievements_data),
        'recent_lessons': recent_lessons
    }
    return render_template('dashboard/index.html', stats=stats)

@dashboard_bp.route('/progress')
@login_required
def view_progress():
    user = session['user']
    
    # Get all lessons with progress
    lessons = supabase.client.table('lessons').select('*').order('id').execute()
    progress = supabase.client.table('progress').select('*').eq('user_id', user['id']).execute()
    
    # Create a dictionary of lesson_id to progress
    progress_map = {int(p['lesson_id']): p for p in progress.data}
    
    print("lessons", lessons.data)
    print("progress", progress.data)
    print("progress_map", progress_map)
    # Calculate completion stats
    completed_lessons = [p for p in progress.data if p.get('status') == 'completed']
    in_progress = [p for p in progress.data if p.get('status') == 'in_progress']
    
    stats = {
        'total_lessons': len(lessons.data),
        'completed': len(completed_lessons),
        'in_progress': len(in_progress),
        'completion_rate': int((len(completed_lessons) / len(lessons.data) * 100)) if lessons.data else 0
    }
    
    return render_template('dashboard/progress.html', 
                         lessons=lessons.data, 
                         progress=progress_map,
                         stats=stats)

@dashboard_bp.route('/achievements')
@login_required
def view_achievements():
    user = session['user']
    
    # Get all achievements
    achievements = supabase.client.table('achievements') \
        .select('*') \
        .eq('user_id', user['id']) \
        .order('created_at', desc=True) \
        .execute()
    
    # Group achievements by category
    achievements_by_category = {}
    for ach in achievements.data:
        category = ach.get('category', 'General')
        if category not in achievements_by_category:
            achievements_by_category[category] = []
        achievements_by_category[category].append(ach)
    
    # Calculate stats
    total_points = sum(a['points'] for a in achievements.data) if achievements.data else 0
    
    return render_template('dashboard/achievements.html',
                         achievements_by_category=achievements_by_category,
                         total_achievements=len(achievements.data) if achievements.data else 0,
                         total_points=total_points)