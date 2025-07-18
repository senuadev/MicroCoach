# app/lessons/routes.py
from flask import render_template, request, jsonify, session, redirect, url_for
from . import lessons_bp
from ..extensions import supabase
from ..dashboard.routes import login_required
import json

@lessons_bp.route('/', methods=['GET'])
@login_required
def list_lessons():
    # Fetch all lessons from the database
    lessons = supabase.client.table('lessons').select('*').execute()
    return render_template('lessons/list.html', lessons=lessons.data)
    
@lessons_bp.route('/<int:lesson_id>', methods=['GET'])
@login_required
def lesson_page(lesson_id):
    # Get lesson data
    lesson = supabase.client.table('lessons').select('*').eq('id', lesson_id).execute()
    if not lesson.data:
        return "Lesson not found", 404
    
    lesson = lesson.data[0]
    return render_template('lessons/lesson.html', 
                         lesson=lesson, 
                         chunks=json.dumps(lesson['content_chunks']),
                         questions=json.dumps(lesson['quiz_questions']))


def award_achievement(user_id, title, description, points):
    """Helper function to award an achievement"""
    supabase.client.table('achievements').insert({
        'user_id': user_id,
        'title': title,
        'description': description,
        'points': points
    }).execute()

@lessons_bp.route('/<int:lesson_id>/progress', methods=['POST'])
@login_required
def update_progress(lesson_id):
    data = request.get_json()
    user_id = session['user']['id']
    chunk_index = data.get('chunk_index')
    is_correct = data.get('is_correct')
    is_completed = data.get('is_completed', False)

    status_value = 'completed' if is_completed else 'in_progress'
    score_value = 100 if is_correct and is_completed else (100 if is_correct else 0)

    # Update progress in Supabase (columns must exist in table)
    supabase.client.table('progress').upsert({
        'user_id': user_id,
        'lesson_id': lesson_id,
        'status': status_value,
        'score': score_value,
        'timestamp': 'now()'
    }, on_conflict='user_id,lesson_id').execute()
    
    # Award points for completing a chunk
    if is_correct:
        award_achievement(
            user_id=user_id,
            title='Lesson Progress',
            description=f'Completed chunk {chunk_index + 1}',
            points=10
        )
    
    # Check if this was the last chunk
    if is_completed:
        # Check if they got 100% on all chunks
        perfect_score = True  # You'll need to implement this check
        if perfect_score:
            award_achievement(
                user_id=user_id,
                title='Perfect Score!',
                description='Scored 100% on a lesson',
                points=20
            )
    
    return jsonify({'success': True})


@lessons_bp.route('/seed-random', methods=['POST'])
@login_required
def seed_random_lessons():
    """Seed at least 10 random lessons for quick testing."""
    import random, uuid, datetime
    lessons = []
    for i in range(10):
        title = f"Random Lesson {uuid.uuid4().hex[:6]}"
        chunks = [
            {
                'content': f'<h3>Chunk {j+1}</h3><p>Placeholder content for {title}.</p>',
                'review_content': 'Review the key concepts.'
            } for j in range(3)
        ]
        questions = [
            {
                'question': f'Question {j+1} for {title}?',
                'options': ['A', 'B', 'C', 'D'],
                'correct_index': random.randint(0, 3),
                'feedback_correct': 'Correct!',
                'feedback_incorrect': 'Try again.'
            } for j in range(3)
        ]
        lessons.append({
            'title': title,
            'content_chunks': chunks,
            'quiz_questions': questions,
            'created_at': datetime.datetime.utcnow().isoformat()
        })
    supabase.client.table('lessons').insert(lessons).execute()
    return jsonify({'inserted': len(lessons)})

# existing sample route
@lessons_bp.route('/create-sample', methods=['GET'])
def create_sample_lesson():
    sample_lesson = {
        'title': 'Introduction to Python',
        'content_chunks': [
            {
                'content': '<h3>Welcome to Python!</h3><p>Python is a high-level, interpreted programming language...</p>',
                'review_content': 'Python is known for its readability and versatility.'
            },
            {
                'content': '<h3>Variables in Python</h3><p>Variables are created when you assign a value to them...</p>',
                'review_content': 'Remember, Python is dynamically typed!'
            }
        ],
        'quiz_questions': [
            {
                'question': 'What type of language is Python?',
                'options': ['Compiled', 'Interpreted', 'Assembly', 'Binary'],
                'correct_index': 1,
                'feedback_correct': 'Great job! Python is an interpreted language.',
                'feedback_incorrect': 'Python code is executed line by line by the interpreter.'
            },
            {
                'question': 'How do you create a variable in Python?',
                'options': ['var x = 5', 'x = 5', 'int x = 5', 'variable x = 5'],
                'correct_index': 1,
                'feedback_correct': 'Correct! No need to declare variable types in Python.',
                'feedback_incorrect': 'In Python, you just use variable_name = value'
            }
        ]
    }
    
    result = supabase.client.table('lessons').insert(sample_lesson).execute()
    return jsonify({'id': result.data[0]['id']})